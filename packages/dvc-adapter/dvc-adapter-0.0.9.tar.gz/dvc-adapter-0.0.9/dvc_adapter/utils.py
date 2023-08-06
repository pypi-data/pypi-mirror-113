from typing import List, Dict, Union

from .oddrn import Generator

def is_list_of_str(data: List) -> bool:
    checked = [True if isinstance(obj, str) else False for obj in data]
    response = all(checked)
    return response

def is_list_of_dicts(data: List) -> bool:
    checked = [True if isinstance(obj, dict) else False for obj in data]
    response = all(checked)
    return response

def get_input_list(generator: Generator, inputs: List) -> List[str]:
    exclude_list = (".py",)
    response = [
        generator.get_dataset_oddrn(source)
        for source in inputs
        if not source.endswith(exclude_list)
    ]
    return response

def get_output_list(generator: Generator, outputs: Union[List[str], List[Dict], Dict]) -> List[str]:
    if isinstance(outputs, Dict):
        response = [generator.get_dataset_oddrn(key) for key in outputs]
    elif is_list_of_dicts(outputs):
        response = [generator.get_dataset_oddrn(source["path"]) for source in outputs]
    elif is_list_of_str(outputs):
        response = [generator.get_dataset_oddrn(source)  for source in outputs]
    else:
        raise ValueError('Wrong output format')
    return response