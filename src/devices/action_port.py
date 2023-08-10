import os
import serial


def action_barrier(command: str):
    dev_port = os.environ.get("MIDDLEWARE_DEV_PORT", "/dev/pts/5")
    with serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=5) as serial_port:
        print(serial_port.name, serial_port.is_open)
        serial_port.write(f"{command}\n".encode())
        response = serial_port.readline().decode().split("\n")[0]
        if not response:
            raise ValueError
        return response


def action_scales(command: str):
    dev_port = os.environ.get("MIDDLEWARE_DEV_PORT", "/dev/pts/10")
    with serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=5) as serial_port:
        print(serial_port.name, serial_port.is_open)
        serial_port.write(f"{command}\n".encode())
        response = serial_port.readline().decode().split("\n")[0]
        if not response:
            raise ValueError
        return response