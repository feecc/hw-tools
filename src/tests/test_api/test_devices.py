import os

import serial
import pytest
from starlette.testclient import TestClient

from src.api.app import app
from src.api.db import Mongo
from src.devices.ports.barrier_port import barrier_port


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def device():
    test_device = {'name': 'TEST', 'type': 'barrier'}
    inserted = Mongo.sync_db['devices'].insert_one(test_device)
    test_device['_id'] = str(inserted.inserted_id)
    return test_device

@pytest.fixture(autouse=True)
def clear_mongo():
    Mongo.clear()


@pytest.fixture
def barrier_serial():
    dev_port = "/dev/pts/4"
    with serial.Serial(dev_port, 9600, rtscts=True, dsrdtr=True, timeout=3) as port:
        yield port
        barrier_port(port)


class TestDevices:
    def test_ok(self, client, device):
        resp = client.get('/devices')
        assert len(resp.json()) == 1

    def test_get_device(self, client, device, barrier_serial):
        device_id = device['_id']
        with barrier_serial:
            resp = client.get(f'/devices/{device_id}')
        assert resp.status_code == 200
        assert resp.json() == {'data': {'state': 'close'}, **device}
