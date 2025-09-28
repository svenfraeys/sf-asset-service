from fastapi import APIRouter, Depends

from ..dependencies import get_db
from .. import schemas, crud, models
from sqlalchemy.orm import Session
from fastapi import HTTPException

ENTITY_SEP = "-"
MODEL_SEP = ":"


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

    # see if we can access the project
    project = (
        db.query(models.Project).filter(models.Project.id == entity.project_id).first()
    )

    if not project:
        return HTTPException(status_code=400, detail="could not find project")

    code = project.code + MODEL_SEP + entity.name

    # get the parent if it has one
    if entity.parent_id:
        parent_entity = (
            db.query(models.Entity).filter(models.Entity.id == entity.parent_id).first()
        )

        if not parent_entity:
            return HTTPException(status_code=400, detail="could not find parent entity")

        code = parent_entity.code + ENTITY_SEP + entity.name

    # double check this code does not exist yet
    if db.query(models.Entity).filter(models.Entity.code == code).first():
        return HTTPException(status_code=400, detail="Entity with code already exists")

    # create the model
    db_entity = models.Entity(**entity.model_dump())
    db_entity.project_id = project.id
    db_entity.code = str(code)

    # commit
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity
