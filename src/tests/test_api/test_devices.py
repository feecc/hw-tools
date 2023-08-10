import os

import serial
from unittest import mock
import pytest
import threading
import subprocess
from starlette.testclient import TestClient

from src.api.app import app
from src.api.db import Mongo
from src.devices.ports.barrier_port import barrier_port
import src.devices.action_port


@pytest.fixture
def client():
    return TestClient(app=app)


@pytest.fixture(scope="module")
def sockets(request):
    socat_process_barrier = subprocess.Popen(["socat", "-d", "-d", "/dev/pts/4", "/dev/pts/5"])
    socat_process_scales = subprocess.Popen(["socat", "-d", "-d", "pty,raw,echo=0", "pty,raw,echo=0"])

    def finalize():
        socat_process_barrier.terminate()
        socat_process_barrier.wait()
        socat_process_scales.terminate()
        socat_process_scales.wait()

    request.addfinalizer(finalize)
    return socat_process_barrier


@pytest.fixture
def device_barrier():
    test_device = {"name": "TEST", "type": "barrier"}
    inserted = Mongo.devices_collection.insert_one(test_device)
    test_device["_id"] = str(inserted.inserted_id)
    return test_device


@pytest.fixture
def device_scales():
    test_device = {"name": "TEST_2", "type": "scales"}
    inserted = Mongo.sync_db["devices"].insert_one(test_device)
    test_device["_id"] = str(inserted.inserted_id)
    return test_device


@pytest.fixture
def device_test():
    test_device = {"name": "TEST_3", "type": "test"}
    inserted = Mongo.sync_db["devices"].insert_one(test_device)
    test_device["_id"] = str(inserted.inserted_id)
    return test_device


@pytest.fixture(autouse=True)
def clear_mongo():
    Mongo.clear()


#
@pytest.fixture
def barrier_serial_port():
    dev_port = "/dev/pts/4"
    port = serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=5)
    barrier_thread = threading.Thread(target=barrier_port, args=(port,), daemon=True)
    barrier_thread.start()
    yield port
    port.close()
    barrier_thread.join()


@pytest.fixture
def scales_serial_port():
    dev_port = "/dev/pts/9"
    port = serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=5)
    scales_thread = threading.Thread(target=barrier_port, args=(port,), daemon=True)
    scales_thread.start()
    yield port
    port.close()
    scales_thread.join()


class TestDevices:
    def test_get_devices(self, client, device_barrier, device_scales, device_test):
        resp = client.get("/devices")
        assert len(resp.json()) == 3

    @pytest.mark.parametrize("status", ("close", "open"))
    @mock.patch("src.devices.action_port.action_barrier")
    def test_get_device_barrier(self, m_barrier, status, client, device_barrier):
        m_barrier.return_value = status

        device_id = device_barrier["_id"]
        resp = client.get(f"/devices/{device_id}")
        assert resp.status_code == 200
        assert resp.json() == {"data": {"state": status}, **device_barrier}

    @mock.patch("src.devices.action_port.action_scales")
    def test_get_device_scales(self, m_scales, client, device_scales):
        m_scales.return_value = "543.657"

        device_id = device_scales["_id"]
        resp = client.get(f"/devices/{device_id}")
        assert resp.status_code == 200
        assert resp.json() == {"data": {"weight": "543.657"}, **device_scales}

    def test_get_device_unknown(self, client, device_test):
        device_id = device_test["_id"]
        resp = client.get(f"/devices/{device_id}")
        assert resp.status_code == 404

    def test_get_device_closed_ports(self, client, device_barrier, device_scales):
        device_id = device_barrier["_id"]
        resp = client.get(f"/devices/{device_id}")
        assert resp.status_code == 404

        device_id = device_scales["_id"]
        resp = client.get(f"/devices/{device_id}")
        assert resp.status_code == 404

    @pytest.mark.parametrize("status", ("close", "open"))
    @mock.patch("src.devices.action_port.action_barrier")
    def test_action_device_barrier(self, m_barrier, status, client, device_barrier):
        m_barrier.return_value = status

        device_id = device_barrier["_id"]
        resp = client.post(f"/devices/{device_id}")
        assert resp.status_code == 200
        assert resp.json() == {"data": {"state": status}, **device_barrier}

    @mock.patch("src.devices.action_port.action_scales")
    def test_action_device_scales(self, m_scales, client, device_scales):
        m_scales.return_value = "543.657"

        device_id = device_scales["_id"]
        resp = client.get(f"/devices/{device_id}")
        assert resp.status_code == 200
        assert resp.json() == {"data": {"weight": "543.657"}, **device_scales}

    def test_action_device_unknown(self, client, device_test):
        device_id = device_test["_id"]
        resp = client.post(f"/devices/{device_id}")
        assert resp.status_code == 404

    def test_action_closed_ports(self, client, device_barrier, device_scales):
        device_id = device_barrier["_id"]
        resp = client.post(f"/devices/{device_id}")
        assert resp.status_code == 404

        device_id = device_scales["_id"]
        resp = client.post(f"/devices/{device_id}")
        assert resp.status_code == 404
