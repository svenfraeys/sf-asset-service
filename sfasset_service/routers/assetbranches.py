from fastapi import APIRouter, Depends

from ..dependencies import get_db
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/asset_branches",
    tags=["asset_branches"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.AssetBranch], tags=["asset_branches"])
def read_asset_branches(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    asset_id: int = 0,
    id: int = 0,
    db: Session = Depends(get_db),
):
    items = crud.get_asset_branches(
        db, skip=skip, limit=limit, name=name, asset_id=asset_id, id=id
    )
    return items


@router.post("/", response_model=schemas.AssetBranch, tags=["asset_branches"])
def create_asset_branch(
    asset_branch: schemas.AssetBranchCreate, db: Session = Depends(get_db)
):
    return crud.create_asset_branch(db=db, asset_branch=asset_branch)
