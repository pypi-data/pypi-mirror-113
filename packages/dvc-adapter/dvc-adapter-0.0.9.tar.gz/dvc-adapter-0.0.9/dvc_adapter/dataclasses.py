from __future__ import annotations
from typing import Dict, Optional, List, Union
from pydantic import BaseModel, Field
from datetime import datetime

from .oddrn import Generator
from .utils import get_input_list, get_output_list
# Pipeline
class Metric(BaseModel):
    cache: bool


class Stage(BaseModel):
    cmd: str
    deps: Optional[List[str]]
    outs: Optional[Union[List,Dict]]
    params: Optional[List[str]]
    metrics: Optional[List[Dict[str, Metric]]]
    plots: Optional[List[Dict]]
    frozen: Optional[str]
    always_changed: Optional[str]
    meta: Optional[Dict] = {}
    desc: Optional[str]
    live: Optional[Dict]
    wdir: Optional[str] = "."


class Pipeline(BaseModel):
    stages: Dict[str, Stage]
    vars: Optional[List]


# Items for request
class DataTransformer(BaseModel):
    source_code_url: Optional[str]
    sql: Optional[str]
    inputs: List[Union[str, Dict]]
    outputs: List[Union[str, Dict]]

    @classmethod
    def get_transformer(cls, generator: Generator, inputs: Union[List, Dict], outputs: Union[List, Dict]) -> DataTransformer:
        inputs = get_input_list(generator, inputs)
        outputs = get_output_list(generator, outputs)
        response = cls(
            inputs=inputs,
            outputs=outputs
        )
        return response

class RequestItem(BaseModel):
    oddrn: str
    name: str
    description: str = Field(None, alias='desc')
    owner: str = None
    metadata: Optional[Dict] = {}
    updated_at: datetime = datetime.now().isoformat()
    created_at: datetime = datetime.now().isoformat()
    data_transformer: DataTransformer

    @classmethod
    def get_item(cls, generator: Generator, name: str, stage: Stage) -> RequestItem:
        response = cls(
            oddrn=generator.get_stage_oddrn(name),
            name=name,
            data_transformer=DataTransformer.get_transformer(generator, stage.deps, stage.outs),
            metadata={
                "cmd": stage.cmd,
                "wdir": stage.wdir,
                "params": stage.params,
                "metrics": stage.metrics,
                "plots": stage.plots,
                **stage.meta
            },
            **stage.dict()
        )
        return response


class RequestData(BaseModel):
    data_source_oddrn: str
    items: List[RequestItem]

    @staticmethod
    def get_items(generator: Generator, stages: Dict) -> List[RequestItem]:
        response = [RequestItem.get_item(generator, name, stage) for name, stage in stages.items()]
        return response