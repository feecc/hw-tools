import json
import os


class _Config:
    def __init__(self, path: str):
        self.config = self.parse_config(path)

    def __call__(self, *args, **kwargs) -> dict:
        return self.config

    @staticmethod
    def parse_config(path: str) -> dict:
        with open(path, "r") as f:
            config = json.loads(f.read())
        return config

    def get_connection_point(self, device_id: int) -> str:
        return self.config[device_id]["point"]

    def get_device_name(self, device_id: int) -> str:
        return self.config[device_id]["name"]

    def get_device(self, device_id: int) -> dict:
        return self.config[device_id]


Config = _Config(os.environ.get("CONFIG_PATH", "configs/devices.json"))
