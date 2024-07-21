from ..models import Asset, Stream
from ..db import session


def _generate_path(stream, version):
    entity = stream.entity
    project = entity.project

    return f"{project.name}/{stream.name}/v{version}"


def create_asset(name: str, stream_id: int):
    stream = session.query(Stream).filter(Stream.id == stream_id).first()
    if not stream:
        return None
    stream.version_counter += 1
    session.add(stream)
    session.commit()
    path = _generate_path(stream, stream.version_counter)
    asset = Asset(
        name=name, stream_id=stream_id, version=stream.version_counter, path=path
    )
    session.add(asset)
    session.commit()
    asset = session.query(Asset).filter(Asset.id == asset.id).first()
    return asset


def get_assets():
    query = session.query(Asset)
    return query.all()


def update_asset(id: int, name: str = "", path: str = ""):
    query = session.query(Asset).filter(Asset.id == id)
    asset = query.first()
    if name:
        asset.name = name
    if path:
        asset.path = path
    session.add(asset)
    session.commit()


def get_asset(id: int):
    query = session.query(Asset).filter(Asset.id == id)
    return query.first()
