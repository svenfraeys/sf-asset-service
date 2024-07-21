from ..models import Space
from ..db import session


def create_space(name: str = ""):
    space = Space(name=name, code=name)
    session.add(space)
    session.commit()
    space = session.query(Space).filter(Space.id == space.id).first()
    return space


def get_all_spaces(name: str = "", code: str = ""):
    query = session.query(Space)
    if name:
        query = query.filter(Space.name == name)
    if code:
        query = query.filter(Space.code == code)

    return query.all()
