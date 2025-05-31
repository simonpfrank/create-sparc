import pytest
from create_sparc_py.core.registry_client import RegistryClient


class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


def test_registry_client_get_success(monkeypatch):
    def mock_get(url, headers=None, params=None, timeout=None):
        assert url.endswith("/test/path")
        return DummyResponse({"result": "ok", "url": url})

    monkeypatch.setattr("requests.get", mock_get)
    client = RegistryClient(base_url="https://mock-registry")
    result = client.get("/test/path")
    assert result["result"] == "ok"
    assert "mock-registry" in result["url"]


def test_registry_client_get_error(monkeypatch):
    def mock_get(url, headers=None, params=None, timeout=None):
        raise Exception("Network error")

    monkeypatch.setattr("requests.get", mock_get)
    client = RegistryClient(base_url="https://mock-registry")
    result = client.get("/fail/path")
    assert result["status"] == "error"
    assert "Network error" in result["error"]


def test_registry_client_post_success(monkeypatch):
    def mock_post(url, headers=None, json=None, timeout=None):
        assert url.endswith("/test/post")
        return DummyResponse({"posted": True, "data": json})

    monkeypatch.setattr("requests.post", mock_post)
    client = RegistryClient(base_url="https://mock-registry")
    data = {"foo": "bar"}
    result = client.post("/test/post", data)
    assert result["posted"] is True
    assert result["data"] == data


def test_registry_client_post_error(monkeypatch):
    def mock_post(url, headers=None, json=None, timeout=None):
        raise Exception("Post failed")

    monkeypatch.setattr("requests.post", mock_post)
    client = RegistryClient(base_url="https://mock-registry")
    result = client.post("/fail/post", {"x": 1})
    assert result["status"] == "error"
    assert "Post failed" in result["error"]


def test_registry_client_authenticate_success(monkeypatch):
    def mock_post(url, json=None, timeout=None):
        assert url.endswith("/auth")
        return DummyResponse({"token": "abc123"})

    monkeypatch.setattr("requests.post", mock_post)
    client = RegistryClient(base_url="https://mock-registry")
    creds = {"api_key": "secret"}
    result = client.authenticate(creds)
    assert result is True
    assert client.authenticated is True
    assert client.token == "abc123"


def test_registry_client_authenticate_fail(monkeypatch):
    def mock_post(url, json=None, timeout=None):
        raise Exception("Auth failed")

    monkeypatch.setattr("requests.post", mock_post)
    client = RegistryClient(base_url="https://mock-registry")
    creds = {"api_key": "bad"}
    result = client.authenticate(creds)
    assert result is False
    assert client.authenticated is False


def test_registry_client_mock_get_post():
    client = RegistryClient(mock=True)
    client.set_mock_data("/foo", {"bar": 1})
    assert client.get("/foo")["bar"] == 1
    # Not found
    assert client.get("/notfound")["status"] == "error"
    # Mock post
    result = client.post("/foo", {"baz": 2})
    assert result["mock"] is True
    assert client._mock_data["/foo"] == {"baz": 2}


def test_registry_client_custom_headers(monkeypatch):
    def mock_get(url, headers=None, params=None, timeout=None):
        assert headers["X-Test"] == "yes"
        return DummyResponse({"ok": True})

    monkeypatch.setattr("requests.get", mock_get)
    client = RegistryClient(base_url="https://mock-registry")
    result = client.get("/test", headers={"X-Test": "yes"})
    assert result["ok"] is True


def test_registry_client_error_status_code(monkeypatch):
    class BadResp:
        def raise_for_status(self):
            from requests import HTTPError

            raise HTTPError("Bad", response=type("R", (), {"status_code": 404})())

        def json(self):
            return {}

    def mock_get(url, headers=None, params=None, timeout=None):
        return BadResp()

    monkeypatch.setattr("requests.get", mock_get)
    client = RegistryClient(base_url="https://mock-registry")
    result = client.get("/bad")
    assert result["status"] == "error"
    assert result["code"] == 404


def test_registry_client_edge_cases():
    client = RegistryClient(mock=True)
    # Missing path
    assert client.get("")["status"] == "error"
    # Bad data
    assert client.post("/bad", None)["mock"] is True
