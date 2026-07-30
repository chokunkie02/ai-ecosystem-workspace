from pydantic import BaseModel

class ItemCreateRequest(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

    class Config:
        from_attributes = True
