from app.Schemas import ItemCreate, ItemOut

nextId: int = 1
itemsStore: dict[int, ItemOut] = {}


def resetStorage() -> None:
    global nextId
    nextId = 1
    itemsStore.clear()


def createItem(data: ItemCreate) -> ItemOut:
    global nextId
    item = ItemOut(id=nextId, title=data.title, description=data.description, price=data.price)
    itemsStore[item.id] = item
    nextId += 1
    return item


def getItem(itemId: int) -> ItemOut | None:
    return itemsStore.get(itemId)


def listItems(q: str | None, limit: int) -> list[ItemOut]:
    allItems = list(itemsStore.values())
    if q:
        allItems = [item for item in allItems if q in item.title]
    return allItems[: max(0, limit)]


def deleteItem(itemId: int) -> bool:
    return itemsStore.pop(itemId, None) is not None

