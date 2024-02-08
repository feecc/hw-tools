from src.devices.action_port import action_netping
from fastapi import HTTPException


class Barrier:
    def __init__(self, data: dict):
        self.url = data["point"]
        self.login = data["login"]
        self.password = data["password"]
        self.path = {"post": "/out.cgi?out2=f,1", "get": "/in.cgi"}

    def contact_device(self, request_type: str):
        response = action_netping(
            url=self.url+self.path[request_type],
            login=self.login,
            passwd=self.password
        )
        if 'error' in response:
            raise ValueError(f'Unexpected response {response}')
        return response
