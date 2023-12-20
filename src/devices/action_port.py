import os
import serial
import struct
import requests
from configs.config import Config
import requests


def action_netping(url: str, login: str, passwd: str):
    auth = (login, passwd)
    resp = requests.get(url, auth=auth)
    return resp.text


def action_com_port(port: str, baudrate: int, rtscts: bool, dsrdtr: bool, timeout: int, command: str):
    with serial.Serial(port, baudrate, rtscts=rtscts, dsrdtr=dsrdtr, timeout=timeout) as serial_port:
        serial_port.write(bytearray(command, 'utf-8'))
        response = serial_port.read(32)
        if not response:
            raise ValueError
        return response
