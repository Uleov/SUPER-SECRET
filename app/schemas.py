from pydantic import BaseModel, Field, StrictFloat


class ItemCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    price: StrictFloat = Field(gt=0)


class ItemOut(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: float
