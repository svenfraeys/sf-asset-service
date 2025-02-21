from fastapi import APIRouter, Depends

from ..dependencies import get_db

from ..dependencies import get_token_header
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/asset_files",
    tags=["asset_files"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.AssetFile], tags=["asset_files"])
def read_asset_files(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    asset_version_id: int = 0,
    db: Session = Depends(get_db),
):
    items = crud.get_asset_files(
        db, skip=skip, limit=limit, name=name, asset_version_id=asset_version_id
    )
    return items


@router.post("/", response_model=schemas.AssetFile, tags=["asset_files"])
def create_asset_file(
    asset_file: schemas.AssetFileCreate, db: Session = Depends(get_db)
):
    return crud.create_asset_file(db=db, asset_file=asset_file)
