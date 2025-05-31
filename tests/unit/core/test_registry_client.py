import pytest
from create_sparc_py.core.registry_client import RegistryClient, registry_client


def test_registry_client_get(monkeypatch):
    client = RegistryClient()
    result = client.get("/test/path")
    assert result["status"] == "ok"
    assert result["path"] == "/test/path"


def test_registry_client_post(monkeypatch):
    client = RegistryClient()
    data = {"foo": "bar"}
    result = client.post("/test/post", data)
    assert result["status"] == "posted"
    assert result["path"] == "/test/post"
    assert result["data"] == data


def test_registry_client_authenticate(monkeypatch):
    client = RegistryClient()
    creds = {"user": "test", "token": "abc"}
    result = client.authenticate(creds)
    assert result is True
    assert client.authenticated is True
