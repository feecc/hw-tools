import os
import serial
import struct
from src.tests.test_devices.virtual.virtual_scales import virtualscales

def check_command(command: str):
    if len(command) != 4:
        return False
    if command[0] != 'W':
        return False
    if command[1] != '0':
        return False
    if command[2] != 'G' and command[2] != 'O':
        return False
    return True


def scales_port(port: serial.Serial) -> None:
    print(port.name, port.is_open)
    while True:
        if not port.readable():
            continue
        command = port.readline().decode()
        if command:
            command = command.split("\n")[0]
        if check_command(command):
            match command[2]:
                case "G":
                    weight = virtualscales.check_weight()
                    resp = struct.pack('f', weight)
                    print(weight)
                    port.write(resp)
                case "O":
                    weight = virtualscales.reset()
                    print(weight)
                    port.write(weight)
        else:
            port.write("Unknown command\n".encode())


if __name__ == "__main__":
    dev_port = os.environ.get("SCALES_DEV_PORT", "/dev/pts/4")
    try:
        with serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True) as serial_port:
            scales_port(serial_port)
    except serial.SerialException:
        print(f"Port {dev_port} is closed or nonexistent.")
    except Exception as e:
        print(f"Got an undefined exception: {e.args}")
