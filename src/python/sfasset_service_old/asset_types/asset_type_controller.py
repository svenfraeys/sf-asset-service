from ..models import AssetType
from ..db import session


def create_asset_type(name: str):
    asset_type = AssetType(name=name)
    session.add(asset_type)
    session.commit()
    asset = session.query(AssetType).filter(AssetType.id == asset_type.id).first()
    return asset


def get_asset_types():
    query = session.query(AssetType)
    return query.all()


def get_asset_type(id: int):
    query = session.query(AssetType).filter(AssetType.id == id)
    return query.first()
