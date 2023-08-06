import yaml
import requests

from watchdog.events import FileSystemEventHandler

from .logger import logger
from .dataclasses import Pipeline, RequestData

class Handler(FileSystemEventHandler):
    def __init__(self, generator, catalog_url, *args, **kwargs):
        self.catalog_url = catalog_url
        self.oddrn_generator = generator
        super().__init__(*args, **kwargs)

    def on_created(self, event):
        self.parse_file(event)

    def on_modified(self, event):
        self.parse_file(event)

    def parse_file(self, event):
        if event.src_path.endswith("dvc.yaml"):
            try:
                with open(event.src_path, "r") as stream:
                    data = yaml.safe_load(stream)
                    if data:
                        pipeline = Pipeline.parse_obj(data)

                        request_data = RequestData(
                            data_source_oddrn=self.oddrn_generator.get_datasource_oddrn(),
                            items=RequestData.get_items(self.oddrn_generator, pipeline.stages)
                        )
                        self.send_data(request_data.dict())
            except Exception as e:
                logger.error(f"ERROR: {str(e)}")

    def send_data(self, data: RequestData):
        logger.debug(data)
        try:
            r = requests.post(self.catalog_url, json=data)
            if r.status_code == 200:
                logger.info(f"Data transfer success")
            else:
                logger.error(f"Error on catalog request. Code: {r.status_code}, Message: {r.text}")
        except Exception as e:
            logger.error(f"Error on catalog request. Error: {str(e)}")
