from oddrn import Generator as ODDRNGenerator


class Generator:
    def __init__(self, source, prefix):
        self.generator = ODDRNGenerator(data_source=source, prefix=prefix)

    def get_datasource_oddrn(self) -> str:
        return self.generator.get_base()

    def get_stage_oddrn(self, name: str) -> str:
         return self.generator.get_stage(name)

    def get_dataset_oddrn(self, file_path: str) -> str:
        return self.generator.get_dataset(file_path)