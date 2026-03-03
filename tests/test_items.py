import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import reset_storage

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_storage_before_each_test():
    reset_storage()


def test_create_item_and_get_it():
    payload = {'title': 'Milk', 'description': '2L', 'price': 120.5}
    create_resp = client.post('/api/items', json=payload)
    assert create_resp.status_code == 201

    created = create_resp.json()
    assert isinstance(created['id'], int)
    assert created['title'] == payload['title']
    assert created['description'] == payload['description']
    assert created['price'] == payload['price']

    get_resp = client.get(f"/api/items/{created['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json() == created


def test_get_item_404():
    resp = client.get('/api/items/999999')
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Item not found'}


def test_delete_item_404():
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
def test_create_item_validation_422(payload):
    resp = client.post('/api/items', json=payload)
    assert resp.status_code == 422
