from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_db
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/asset_tags",
    tags=["asset_tags"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.AssetTag], tags=["asset_tags"])
def read_asset_tags(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    asset_id: int = None,
    branch_id: int = None,
    id: int = 0,
    db: Session = Depends(get_db),
):
    items = crud.get_asset_tags(
        db,
        skip=skip,
        limit=limit,
        name=name,
        asset_id=asset_id,
        id=id,
        branch_id=branch_id,
    )
    return items


@router.post("/", response_model=schemas.AssetTag, tags=["asset_tags"])
def create_asset_tag(asset_tag: schemas.AssetTagCreate, db: Session = Depends(get_db)):
    return crud.create_asset_tag(db=db, asset_tag=asset_tag)
