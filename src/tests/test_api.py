from .test_fixture import client
from .data import bank_1


def test_bank(client):
    assert client.get("/api/v1/bank/").json == []
    client.put("/api/v1/bank/", json=bank_1)
    assert len(client.get("/api/v1/bank/").json) == 1
