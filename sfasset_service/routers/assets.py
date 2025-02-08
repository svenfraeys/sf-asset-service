from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header, get_db
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/assets",
    tags=["assets"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Asset], tags=["assets"])
def read_assets(
    skip: int = 0,
    limit: int = 100,
    code: str = None,
    name: str = None,
    entity_id: int = None,
    project_id: int = None,
    id: int = None,
    db: Session = Depends(get_db),
):
    items = crud.get_assets(
        db,
        skip=skip,
        limit=limit,
        code=code,
        name=name,
        entity_id=entity_id,
        project_id=project_id,
        id=id,
    )
    return items


@router.post("/", response_model=schemas.Asset, tags=["assets"])
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    return crud.create_asset(db=db, asset=asset)
