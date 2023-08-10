import os
import serial

from src.devices.virtual.virtual_scales import virtualscales


def scales_port(port: serial.Serial) -> None:
    print(port.name, port.is_open)
    while True:
        command = port.readline().decode().split("\n")[0]
        print(command)
        match command:
            case "current":
                weight = virtualscales.get_current_weight()
                print(weight)
                port.write(f"{weight}\n".encode())
            case "check":
                weight = virtualscales.check_weight()
                print(weight)
                port.write(f"{weight}\n".encode())
            case _:
                port.write("Unknown command\n".encode())


if __name__ == "__main__":
    dev_port = os.environ.get("BARRIER_DEV_PORT", "/dev/pts/7")
    try:
        with serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True) as serial_port:
            scales_port(serial_port)
    except serial.SerialException:
        print(f"Port {dev_port} is closed or nonexistent.")
    except Exception as e:
        print(f"Got an undefined exception: {e.args}")
