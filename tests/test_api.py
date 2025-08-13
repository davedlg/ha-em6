import sys
import types

class DummyResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload

# Insert a dummy requests module so api.py can import it without the real dependency
sys.modules['requests'] = types.SimpleNamespace(
    get=lambda *args, **kwargs: DummyResponse(500),
    codes=types.SimpleNamespace(ok=200),
)

from custom_components.em6.api import em6Api

def test_get_prices_handles_http_error(monkeypatch):
    def fake_get(*args, **kwargs):
        return DummyResponse(500)

    import requests  # this is our dummy module
    monkeypatch.setattr(requests, 'get', fake_get)

    api = em6Api("Somewhere")
    assert api.get_prices() is None
