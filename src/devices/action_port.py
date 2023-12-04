import os
import serial
import struct
from configs.config import Config


def action_barrier(command: str):  # delete
    dev_port = os.environ.get("MIDDLEWARE_DEV_PORT_BARRIER", "/dev/pts/5")
    with serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=5) as serial_port:
        print(serial_port.name, serial_port.is_open)
        serial_port.write(f"{command}\n".encode())
        response = serial_port.readline().decode().split("\n")[0]
        print(response)
        if not response:
            raise ValueError
        return response


def action_com_port(port: str, baudrate: int, rtscts: bool, dsrdtr: bool, timeout: int, command: str):
    with serial.Serial(port, baudrate, rtscts=rtscts, dsrdtr=dsrdtr, timeout=timeout) as serial_port:
        serial_port.write(bytearray(command, 'utf-8'))
        response = serial_port.read(32)
        if not response:
            raise ValueError
        return response
