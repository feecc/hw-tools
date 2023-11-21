import os

from unittest import mock
import pytest

from src.tests import conftest


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

    def test_virtual_ports(self, client, device_barrier, barrier_serial_port):
        device_id = device_barrier["_id"]
        resp = client.get(f"/devices/{device_id}")
        assert resp.status_code == 200
        assert resp.json() == {"data": {"state": "close"}, **device_barrier}
        resp = client.post(f"/devices/{device_id}")
        assert resp.status_code == 200
        assert resp.json() == {"data": {"state": "open"}, **device_barrier}
