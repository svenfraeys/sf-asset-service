from ..models import Asset, File
from ..db import session


def get_all_files(asset_id: int = 0, path: str = ""):

    query = session.query(File)
    if asset_id:
        query = query.filter(File.asset_id == asset_id)
    if path:
        query = query.filter(File.path == path)
    return query.all()


def create_file(asset_id: int, path: str):
    asset = session.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise RuntimeError(f"Asset with id {asset_id} not found")

    file = File(path=path, asset_id=asset_id)
    session.add(file)
    session.commit()
    session.refresh(file)
    return file
