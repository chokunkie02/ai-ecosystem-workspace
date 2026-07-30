from fastapi import APIRouter, Depends
from backend.schemas.item_schema import ItemCreateRequest, ItemResponse
from backend.dependencies.database import get_db

router = APIRouter(prefix="/api/v1/items", tags=["Items Management"])

mock_db = []

@router.post("/", response_model=ItemResponse)
async def create_item(item: ItemCreateRequest, db=Depends(get_db)):
    new_item = ItemResponse(id=len(mock_db) + 1, **item.model_dump())
    mock_db.append(new_item)
    return new_item

@router.get("/", response_model=list[ItemResponse])
async def get_items(db=Depends(get_db)):
    return mock_db
