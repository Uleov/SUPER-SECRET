from fastapi import APIRouter, HTTPException, Query, Response, status

from app.Schemas import ItemCreate, ItemOut
from app.Storage import createItem, deleteItem, getItem, listItems

router = APIRouter()


@router.get('/health')
def health():
    return {'status': 'ok'}


@router.post('/items', response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def createItemEndpoint(payload: ItemCreate):
    return createItem(payload)


@router.get('/items', response_model=list[ItemOut])
def listItemsEndpoint(
    q: str | None = Query(default=None, description='строка поиска'),
    limit: int = Query(default=10, ge=1, le=100, description='сколько элементов вернуть'),
):
    return listItems(q=q, limit=limit)


@router.get('/items/{itemId}', response_model=ItemOut)
def getItemEndpoint(
    itemId: int,
    q: str | None = Query(default=None, description='строка поиска'),
    limit: int = Query(default=10, ge=1, le=100, description='сколько элементов вернуть'),
):
    item = getItem(itemId)
    if item is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return item


@router.delete('/items/{itemId}', status_code=status.HTTP_204_NO_CONTENT)
def deleteItemEndpoint(itemId: int):
    ok = deleteItem(itemId)
    if not ok:
        raise HTTPException(status_code=404, detail='Item not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

