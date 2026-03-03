from app.schemas import ItemCreate, ItemOut

next_id: int = 1
items: dict[int, ItemOut] = {}


def reset_storage() -> None:
    global next_id
    next_id = 1
    items.clear()


def create_item(data: ItemCreate) -> ItemOut:
    global next_id
    item = ItemOut(id=next_id, title=data.title, description=data.description, price=data.price)
    items[item.id] = item
    next_id += 1
    return item


def get_item(item_id: int) -> ItemOut | None:
    return items.get(item_id)


def list_items(q: str | None, limit: int) -> list[ItemOut]:
    all_items = list(items.values())
    if q:
        all_items = [item for item in all_items if q in item.title]
    return all_items[: max(0, limit)]


def delete_item(item_id: int) -> bool:
    return items.pop(item_id, None) is not None
