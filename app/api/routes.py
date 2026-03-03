from fastapi import APIRouter, HTTPException, Query, Response, status

from app.schemas import ItemCreate, ItemOut
from app.storage import create_item, delete_item, get_item, list_items

router = APIRouter()


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.post('/items', response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(payload: ItemCreate):
    return create_item(payload)


@router.get('/items', response_model=list[ItemOut])
def list_items_endpoint(
    q: str | None = Query(default=None, description='Строка поиска (опционально)'),
    limit: int = Query(default=10, ge=1, le=100, description='Сколько элементов вернуть'),
):
    return list_items(q=q, limit=limit)


@router.get('/items/{item_id}', response_model=ItemOut)
def get_item_endpoint(
    item_id: int,
    q: str | None = Query(default=None, description='Строка поиска (опционально)'),
    limit: int = Query(default=10, ge=1, le=100, description='Сколько элементов вернуть'),
):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item


@router.delete('/items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item_endpoint(item_id: int):
    ok = delete_item(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Item not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
