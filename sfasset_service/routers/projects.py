from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header, get_db
from .. import schemas, crud
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
    name: str = None,
    code: str = None,
    db: Session = Depends(get_db),
):
    items = crud.get_projects(db, skip=skip, limit=limit, name=name, code=code)
    return items


@router.post("/", response_model=schemas.Project, tags=["projects"])
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)
