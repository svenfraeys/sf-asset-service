from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header, get_db
from .. import schemas, crud
from sqlalchemy.orm import Session
from . import conf

router = APIRouter(
    prefix="/asset_versions",
    tags=["asset_versions"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.AssetVersion], tags=["asset_versions"])
def read_asset_versions(
    skip: int = conf.SKIP,
    limit: int = conf.LIMIT,
    name: str = None,
    asset_id: int = None,
    code: str = None,
    id: int = 0,
    db: Session = Depends(get_db),
):
    items = crud.get_asset_versions(
        db, skip=skip, limit=limit, name=name, asset_id=asset_id, code=code, id=id
    )
    return items


@router.post("/", response_model=schemas.AssetVersion, tags=["asset_versions"])
def create_asset_version(
    asset_version: schemas.AssetVersionCreate, db: Session = Depends(get_db)
):
    return crud.create_asset_version(db=db, asset_version=asset_version)


@router.put(
    "/{asset_version_id}", response_model=schemas.AssetVersion, tags=["asset_versions"]
)
def update_asset_version(
    asset_version_id: int,
    asset_version: schemas.AssetVersion,
    db: Session = Depends(get_db),
):
    return crud.update_asset_version(
        db=db, asset_version_id=asset_version_id, asset_version=asset_version
    )


@router.get(
    "/{asset_version_id}", response_model=schemas.AssetVersion, tags=["asset_versions"]
)
def get_asset_version(
    asset_version_id: int,
    db: Session = Depends(get_db),
):
    av = crud.get_asset_version_by_id(db=db, id=asset_version_id)
    if not av:
        raise HTTPException(status_code=404, detail="AssetVersion not found")
    return av
