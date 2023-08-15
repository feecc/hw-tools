from src.api.app import app
from starlette.testclient import TestClient
from src.api.db import Mongo
import threading
import subprocess
import pytest
import os
import serial
from dotenv import load_dotenv

from src.devices.ports.barrier_port import barrier_port
import src.devices.action_port

load_dotenv()

PORT_PATH = "/media/zemljanichka/ubuntudata1/Feecc_test_soft/testsocat/test_stdout"
TEST_PORTS = list()


@pytest.fixture(scope="module")
def client():
    return TestClient(app=app)


@pytest.fixture(scope="module", autouse=True)
def sockets(request):

    socat_process_barrier = subprocess.Popen(["socat", "-d", "-d", "pty,raw,echo=0", "pty,raw,echo=0", "&>", "/media/zemljanichka/ubuntudata1/Feecc_test_soft/testsocat/test_stdout"])
 #   socat_process_scales = subprocess.Popen(["socat", "-d", "-d", "pty,raw,echo=0", "pty,raw,echo=0", "&>>", "/media/zemljanichka/ubuntudata1/Feecc_test_soft/testsocat/test_stdout"])

  #  print("MEOW")

    with open(PORT_PATH) as P:
        ports = P.readlines()
        for port in ports:
            print(port)
            if dev_port := port.find("/dev/pts/"):
                TEST_PORTS.append(port[dev_port: len(port)-1])

    # for port in TEST_PORTS:
    #     print(port)
    os.environ["BARRIER_DEV_PORT"] = TEST_PORTS[0]
    os.environ["MIDDLEWARE_DEV_PORT_BARRIER"] = TEST_PORTS[1]


    def finalize():
        socat_process_barrier.terminate()
        socat_process_barrier.wait()
        # socat_process_scales.terminate()
        # socat_process_scales.wait()

    request.addfinalizer(finalize)
    return socat_process_barrier


@pytest.fixture(scope="module")
def device_barrier():
    test_device = {"name": "TEST", "type": "barrier"}
    inserted = Mongo.devices_collection.insert_one(test_device)
    test_device["_id"] = str(inserted.inserted_id)
    return test_device


@pytest.fixture(scope="module")
def device_scales():
    test_device = {"name": "TEST_2", "type": "scales"}
    inserted = Mongo.sync_db["devices"].insert_one(test_device)
    test_device["_id"] = str(inserted.inserted_id)
    return test_device


@pytest.fixture(scope="module")
def device_test():
    test_device = {"name": "TEST_3", "type": "test"}
    inserted = Mongo.sync_db["devices"].insert_one(test_device)
    test_device["_id"] = str(inserted.inserted_id)
    return test_device


@pytest.fixture(scope="module", autouse=True)
def clear_mongo():
    Mongo.clear()


#
@pytest.fixture(scope="module")
def barrier_serial_port():
    dev_port = os.environ.get("BARRIER_DEV_PORT")
   #  print(TEST_PORTS[0])
   #  dev_port = TEST_PORTS[0]
    print(1)
    print(TEST_PORTS)
    port = serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=5)
    barrier_thread = threading.Thread(target=barrier_port, args=(port,), daemon=True)
    barrier_thread.start()
    yield port
    port.close()
    barrier_thread.join()


@pytest.fixture()
def scales_serial_port():
    dev_port = "/dev/pts/9"
    port = serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=5)
    scales_thread = threading.Thread(target=barrier_port, args=(port,), daemon=True)
    scales_thread.start()
    yield port
    port.close()
    scales_thread.join()
