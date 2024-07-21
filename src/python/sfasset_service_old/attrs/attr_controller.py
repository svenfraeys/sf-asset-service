from ..models import Asset, Attr
from ..db import session


def create_attr(asset_id: int, name: str):
    asset = session.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise RuntimeError(f"Asset with id {asset_id} not found")

    attr = Attr(name=name, asset_id=asset_id)
    session.add(attr)
    session.commit()
    session.refresh(attr)
    return attr


def get_attr(id: int):
    return session.query(Attr).filter(Attr.id == id).first()


def get_all_attrs(asset_id: int = 0, name: str = ""):
    query = session.query(Attr)
    if asset_id:
        query = query.filter(Attr.asset_id == asset_id)
    if name:
        query = query.filter(Attr.name == name)
    return query.all()


def update_attr(id: int, name: str, value_int: int):
    attr = session.query(Attr).filter(Attr.id == id).first()
    if not attr:
        raise RuntimeError(f"Attr with id {id} not found")
    if name:
        attr.name = name
    if value_int is not None:
        attr.value_int = value_int
    session.add(attr)
    session.commit()
    return attr
