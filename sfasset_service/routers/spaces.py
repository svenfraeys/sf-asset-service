from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header, get_db
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/spaces",
    tags=["spaces"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Space], tags=["spaces"])
def read_spaces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    code: str = "",
    name: str = "",
):
    items = crud.get_spaces(db, skip=skip, limit=limit, code=code, name=name)
    return items


@router.post("/", response_model=schemas.Space, tags=["spaces"])
def create_space(space: schemas.SpaceCreate, db: Session = Depends(get_db)):
    db_space = crud.get_space_by_code(db, code=space.name)
    if db_space:
        raise HTTPException(status_code=400, detail="Space code already registered")

    return crud.create_space(db=db, space=space, code=space.name)
