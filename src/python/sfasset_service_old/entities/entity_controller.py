from ..models import Entity, Space
from ..db import session


def create_entity(space_id: int, name: str, parent_id: int = 0):
    space = session.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise RuntimeError(f"Space not found with id {space_id}")
    code = f"{space.code}:{name}"
    if parent_id:
        parent = session.query(Entity).filter(Entity.id == parent_id).first()
        if not parent:
            raise RuntimeError(f"Parent entity not found with id {parent_id}")

        parent_code = parent.code
        code = f"{parent_code}:{name}"

    entity = Entity(name=name, space_id=space_id, code=code)

    session.add(entity)
    session.commit()
    entity = session.query(Entity).filter(Entity.id == entity.id).first()
    return entity
