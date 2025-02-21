from fastapi import APIRouter, Depends

from ..dependencies import get_db
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/asset_links",
    tags=["asset_links"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.AssetLink], tags=["asset_links"])
def read_asset_links(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    id: int = 0,
    asset_version_id: int = 0,
    target_asset_version_id: int = 0,
    db: Session = Depends(get_db),
):
    items = crud.get_asset_links(
        db,
        skip=skip,
        limit=limit,
        name=name,
        asset_version_id=asset_version_id,
        id=id,
        target_asset_version_id=target_asset_version_id,
    )
    return items


@router.post("/", response_model=schemas.AssetLink, tags=["asset_links"])
def create_asset_link(
    asset_link: schemas.AssetLinkCreate, db: Session = Depends(get_db)
):
    return crud.create_asset_link(db=db, asset_link=asset_link)
