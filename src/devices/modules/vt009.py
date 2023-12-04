from src.devices.action_port import action_com_port
import struct
from fastapi import HTTPException


class Terminal_VT009:
    def __init__(self, data: dict):
        self.commands = {
            "get": {
                "weight": {"command": "G", "response_format": "f"},
                "measure": {"command": "F", "response_format": "i"},
            },
            "set": {},
        }
        self.terminal_id = "0"  # sequence number of terminal, default=0
        self.port = data["point"]
        self.baudrate = 9600
        self.rtscts = False  # enable hardware (RTS/CTS) flow control
        self.dsrdtr = False  # enable hardware (DSR/DTR) flow control
        self.read_timeout = 5

    def get_command(self, request_type: str, data_type: str):
        command = "W" + self.terminal_id + self.commands[request_type][data_type]["command"] + "1"
        return command
    def contact_device(self, request_type: str, data_type: str):
        command = self.get_command(request_type=request_type, data_type=data_type)
        response = action_com_port(
            port=self.port,
            baudrate=self.baudrate,
            rtscts=self.rtscts,
            dsrdtr=self.dsrdtr,
            timeout=self.read_timeout,
            command=command,
        )
        response = struct.unpack(self.commands[request_type][data_type]["response_format"], response)[0]
        if response < 10:
            raise ValueError('Unexpected response')
        response = str(round(response, 3)) + "0"
        return response
