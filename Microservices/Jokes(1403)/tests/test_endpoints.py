import os
os.environ.setdefault("MONGO_HOST", "localhost")
os.environ.setdefault("MONGO_PORT", "27017")
import pathlib, sys; sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from fastapi.testclient import TestClient

from main import app
import routers.get as get_router


@pytest.fixture

def fake_joke():
    return {
        "id": "42",
        "text": "Knock knock",
        "created_at": "2024-01-01",
        "uploaded_by": {"syncId": 1, "username": "tester"}
    }


class FakeDB:
    def __init__(self, joke):
        self.joke = joke
        self.last_call = None

    async def get_documents(self, skip=0, limit=10):
        self.last_call = ("get_documents", skip, limit)
        return 1, [self.joke]

    async def random_document(self):
        self.last_call = ("random_document",)
        return self.joke


@pytest.fixture

def client(monkeypatch, fake_joke):
    fake_db = FakeDB(fake_joke)
    import fastapi.routing
    async def no_validate(**kwargs):
        return kwargs["response_content"]
    monkeypatch.setattr(fastapi.routing, "serialize_response", no_validate)
    monkeypatch.setattr(get_router, "db", fake_db)
    for route in app.routes:
        if getattr(route, "path", None) == "/random":
            route.response_model = None
            route.response_model_field = None
            route.response_field = None
    client = TestClient(app)
    client.fake_db = fake_db
    return client


def test_random_endpoint(client, fake_joke):
    response = client.get("/random")
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "result": fake_joke}
    assert client.fake_db.last_call == ("random_document",)


def test_filter_endpoint(client, fake_joke):
    response = client.get("/filter", params={"skip": 2, "limit": 5})
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "result": [fake_joke]}
    assert client.fake_db.last_call == ("get_documents", 2, 5)
