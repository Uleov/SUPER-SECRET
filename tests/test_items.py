import pytest
from fastapi.testclient import TestClient

from app.Main import app
from app.Storage import resetStorage

client = TestClient(app)


@pytest.fixture(autouse=True)
def resetStorageBeforeEachTest():
    resetStorage()


def testCreateItemAndGetIt():
    payload = {'title': 'Milk', 'description': '2L', 'price': 120.5}
    createResp = client.post('/api/items', json=payload)
    assert createResp.status_code == 201

    created = createResp.json()
    assert isinstance(created['id'], int)
    assert created['title'] == payload['title']
    assert created['description'] == payload['description']
    assert created['price'] == payload['price']

    getResp = client.get(f"/api/items/{created['id']}")
    assert getResp.status_code == 200
    assert getResp.json() == created


def testGetItem404():
    resp = client.get('/api/items/999999')
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Item not found'}


def testDeleteItem404():
    resp = client.delete('/api/items/999999')
    assert resp.status_code == 404


@pytest.mark.parametrize(
    'payload',
    [
        {'description': 'no title', 'price': 10.0},
        {'title': 'Bad price', 'description': None, 'price': 0},
        {'title': 'Price as str', 'description': None, 'price': '10'},
    ],
)
def testCreateItemValidation422(payload):
    resp = client.post('/api/items', json=payload)
    assert resp.status_code == 422

