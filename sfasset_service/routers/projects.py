from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header, get_db
from .. import schemas, crud, models
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Project], tags=["projects"])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    name: str | None = None,
    code: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Project)

    if name is not None:
        query = query.filter(models.Project.name == name)

    if code is not None:
        query = query.filter(models.Project.code == code)

    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.Project, tags=["projects"])
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # see which code the project would have
    code = project.name

    # check if the project code already exists
    if db.query(models.Project).filter(models.Project.code == code).first():
        return HTTPException(status_code=400, detail="Project with code already exists")

    db_project = models.Project(**project.model_dump())
    db_project.code = code

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
