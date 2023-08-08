import os
import serial

from devices.virtual.test_barrier import testbarrier


def barrier_port(port: str) -> None:
    with serial.Serial(port, 9600, rtscts=True, dsrdtr=True) as serial_port:
        print(serial_port.name, serial_port.is_open)
        while True:
            command = serial_port.readline().decode().split("\n")[0]
            print(command)
            match command:
                case "state":
                    state = testbarrier.check_state()
                    print(state)
                    serial_port.write(f"{state}\n".encode())
                case "change":
                    state = testbarrier.change_state()
                    print(state)
                    serial_port.write(f"{state}\n".encode())
                case _:
                    serial_port.write("Unknown command\n".encode())


if __name__ == "__main__":
    dev_port = os.environ.get("BARRIER_DEV_PORT", "/dev/pts/4")
    try:
        barrier_port(dev_port)
    except serial.SerialException:
        print(f"Port {dev_port} is closed or nonexistent.")
    except Exception as e:
        print(f"Got an undefined exception: {e.args}")
