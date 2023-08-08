import os
import serial

from src.devices.virtual.test_barrier import testbarrier


def barrier_port(port: serial.Serial) -> None:
    print(port.name, port.is_open)
    while True:
        command = port.readline().decode().split("\n")[0]
        print(command)
        match command:
            case "state":
                state = testbarrier.check_state()
                print(state)
                port.write(f"{state}\n".encode())
            case "change":
                state = testbarrier.change_state()
                print(state)
                port.write(f"{state}\n".encode())
            case _:
                port.write("Unknown command\n".encode())


if __name__ == "__main__":
    dev_port = os.environ.get("BARRIER_DEV_PORT", "/dev/pts/4")
    try:
        with serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True) as serial_port:
            barrier_port(serial_port)
    except serial.SerialException:
        print(f"Port {dev_port} is closed or nonexistent.")
    except Exception as e:
        print(f"Got an undefined exception: {e.args}")
