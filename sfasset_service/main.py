from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import (
    items,
    users,
    spaces,
    entities,
    assets,
    assetversions,
    assetfiles,
    projects,
    assetlinks,
)
from . import models
from .database import engine

# to reset on refresh uncheck these lines
# models.Base.metadata.drop_all(bind=engine)
# models.Base.metadata.create_all(bind=engine)


# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()


app.include_router(users.router)
app.include_router(items.router)
app.include_router(assetversions.router)
app.include_router(assetfiles.router)
app.include_router(assetlinks.router)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
app.include_router(spaces.router)
app.include_router(entities.router)
app.include_router(assets.router)
app.include_router(projects.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
