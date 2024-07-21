# https://fastapi.tiangolo.com/tutorial/sql-databases/
from fastapi import FastAPI
from .db import session
from .models import Entity, Todo, Space, Asset, Stream
from .assets import asset_controller
from .attrs import attr_controller
from .files import file_controller
from .spaces import space_controller
from .asset_types import asset_type_controller
from .entities import entity_controller

app = FastAPI()


@app.post("/create")
async def create_todo(text: str, is_complete: bool = False):
    todo = Todo(text=text, is_done=is_complete)
    session.add(todo)
    session.commit()
    return {"todo added": todo.text}


@app.get("/")
async def get_all_todos():
    todos_query = session.query(Todo)
    return todos_query.all()


@app.get("/spaces")
async def get_all_spaces(name: str = "", code: str = ""):
    return space_controller.get_all_spaces(name=name, code=code)


@app.post("/spaces")
async def create_space(name: str):
    return space_controller.create_space(name=name)


@app.put("/spaces/{id}")
async def update_space(id: int, name: str = ""):
    query = session.query(Space).filter(Space.id == id)
    space = query.first()
    if name:
        space.name = name
    session.add(space)
    session.commit()


@app.get("/spaces/{id}/entities")
async def get_space_entities(id: int):
    query = session.query(Space).filter(Space.id == id)
    space = query.first()
    session.add(space.entities)
    session.commit()


@app.post("/entities")
async def create_entity(space_id: int, name: str):
    return entity_controller.create_entity(space_id, name)


@app.get("/entities")
async def get_all_entities():
    query = session.query(Entity)
    return query.all()


@app.get("/streams")
async def get_all_streams(entity_id: int = None, name: str = None):
    query = session.query(Stream)
    if entity_id:
        query = query.filter(Stream.entity_id == entity_id)
    if name:
        query = query.filter(Stream.name == name)

    return query.all()


@app.post("/streams")
async def create_stream(entity_id: int, name: str):
    stream = Stream(name=name, entity_id=entity_id)
    session.add(stream)
    session.commit()
    stream = session.query(Stream).filter(Stream.id == stream.id).first()
    return stream


@app.get("/assets")
async def get_all_assets():
    return asset_controller.get_assets()


@app.post("/assets")
async def create_asset(stream_id: int, name: str):
    return asset_controller.create_asset(name, stream_id)


@app.put("/assets/{id}")
async def update_asset(id: int, name: str = "", path: str = ""):
    return asset_controller.update_asset(id, name, path)


@app.get("/assets/{id}")
async def get_asset(id: int):
    return asset_controller.get_asset(id)


@app.post("/attrs")
async def create_attr(asset_id: int, name: str):
    return attr_controller.create_attr(asset_id, name)


@app.get("/attrs")
async def get_all_attrs(asset_id: int = 0, name: str = ""):
    return attr_controller.get_all_attrs(asset_id, name)


@app.put("/attrs/{id}")
async def get_all_attrs(id: int, name: str = "", value_int: int = 0):
    return attr_controller.update_attr(id, name, value_int)


@app.get("/attrs/{id}")
async def get_all_attrs(id: int):
    return attr_controller.get_attr(id)


@app.get("/files")
async def get_all_files(asset_id: int = 0, path: str = ""):
    return file_controller.get_all_files(asset_id=asset_id, path=path)


@app.post("/files")
async def create_file(asset_id: int, path: str):
    return file_controller.create_file(asset_id, path)


@app.get("/asset_types")
async def get_asset_types():
    return asset_type_controller.get_asset_types()


@app.post("/asset_types")
async def create_asset_type(name: str):
    return asset_type_controller.create_asset_type(name)


@app.get("/asset_types/{id}")
async def get_asset_type(id: int):
    return asset_type_controller.get_asset_type(id)


# create all
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
