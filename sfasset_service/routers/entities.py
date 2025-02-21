from fastapi import APIRouter, Depends

from ..dependencies import get_db
from .. import schemas, crud
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/entities",
    tags=["entities"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Entity], tags=["entities"])
def read_entities(
    skip: int = 0,
    limit: int = 100,
    name: str = "",
    code: str = "",
    project_id: int = 0,
    id: int = 0,
    parent_id: int = 0,
    db: Session = Depends(get_db),
):
    items = crud.get_entities(
        db,
        skip=skip,
        limit=limit,
        name=name,
        project_id=project_id,
        parent_id=parent_id,
        code=code,
        id=id,
    )
    return items


@router.post("/", response_model=schemas.Entity, tags=["entities"])
def create_entity(entity: schemas.EntityCreate, db: Session = Depends(get_db)):
    return crud.create_entity(db=db, entity=entity)
