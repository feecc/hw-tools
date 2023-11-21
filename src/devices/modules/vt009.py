from src.devices.action_port import action_com_port
import struct


class Terminal_VT009:
    def __init__(self, data: dict):
        self.commands = {
            "get": {
                "weight": {"command": "G", "response_format": "float-bytes"},
                "data": {"command": "D", "response_format": "bin-decimal"},
            },
            "set": {},
        }
        self.terminal_id = "0"  # sequence number of terminal, default=0
        self.port = data["point"]
        self.baudrate = 9600
        self.rtscts = True  # enable hardware (RTS/CTS) flow control
        self.dsrdtr = True  # enable hardware (DSR/DTR) flow control
        self.read_timeout = 5

    def contact_device(self, request_type: str, data_type: str):
        command = "W" + self.terminal_id + self.commands[request_type][data_type]["command"] + "1"
        response = action_com_port(
            port=self.port,
            baudrate=self.baudrate,
            rtscts=self.rtscts,
            dsrdtr=self.dsrdtr,
            timeout=self.read_timeout,
            command=command,
        )
        if self.commands[request_type][data_type]["response_format"] == "float-bytes":
            response = struct.unpack("f", response)[0]
        return response
