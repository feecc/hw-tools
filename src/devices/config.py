import json


class _Config:
    def __init__(self, path: str):
        self.config = self.parse_config(path)

    def __call__(self, *args, **kwargs) -> dict:
        return self.config

    @staticmethod
    def parse_config(path: str) -> dict:
        with open(path, 'r') as f:
            config = json.loads(f.read())
        return config

    def get_connection_point(self, device: str, number: str) -> str:
        return self.config[device][number]["point"]


Config = _Config("src/devices/config.json")
