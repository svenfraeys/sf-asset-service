from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header, get_db
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/asset_versions",
    tags=["asset_versions"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.AssetVersion], tags=["asset_versions"])
def read_asset_versions(
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    asset_id: int = None,
    db: Session = Depends(get_db),
):
    items = crud.get_asset_versions(
        db, skip=skip, limit=limit, name=name, asset_id=asset_id
    )
    return items


@router.post("/", response_model=schemas.AssetVersion, tags=["asset_versions"])
def create_asset_version(
    asset_version: schemas.AssetVersionCreate, db: Session = Depends(get_db)
):
    return crud.create_asset_version(db=db, asset_version=asset_version)
