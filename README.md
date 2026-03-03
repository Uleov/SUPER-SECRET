# FastAPI practicum

Простой учебный проект по FastAPI.

## Что есть
- health check: `GET /api/health`
- создание item: `POST /api/items`
- список item: `GET /api/items`
- один item по id: `GET /api/items/{item_id}`
- удаление item: `DELETE /api/items/{item_id}`

## Как запустить
```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install fastapi uvicorn pytest httpx
uvicorn app.main:app --reload
```

Документация:
- `http://127.0.0.1:8000/docs`

## Как запустить тесты
```bash
py -m pytest -q
```
