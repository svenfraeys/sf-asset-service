from sqlalchemy.orm import Session

from . import models, schemas

DATA_ROOT = "C:/sfasset_data"


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_spaces(db: Session, skip: int = 0, limit: int = 100, code: str = ""):
    query = db.query(models.Space)
    if code:
        query = query.filter(models.Space.code == code)
    return query.offset(skip).limit(limit).all()


def create_space(db: Session, space: schemas.SpaceCreate, code=None):
    db_space = models.Space(name=space.name, code=code)
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space


def get_space_by_code(db: Session, code: str):
    return db.query(models.Space).filter(models.Space.code == code).first()


def get_entities(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    space_id: int = None,
    parent_id: int = None,
):
    query = db.query(models.Entity)
    if name:
        query = query.filter(models.Entity.name == name)
    if space_id:
        query = query.filter(models.Entity.space_id == space_id)
    if parent_id:
        query = query.filter(models.Entity.parent_id == parent_id)
    return query.offset(skip).limit(limit).all()


def get_space_by_id(db: Session, id: int):
    return db.query(models.Space).filter(models.Space.id == id).first()


def get_entity_by_id(db: Session, id: int):
    return db.query(models.Entity).filter(models.Entity.id == id).first()


def get_entity_by_code(db: Session, code: str):
    return db.query(models.Entity).filter(models.Entity.code == code).first()


def create_entity(db: Session, entity: schemas.EntityCreate):
    db_entity = models.Entity(**entity.dict())

    if entity.parent_id:
        parent_entity = get_entity_by_id(db, entity.parent_id)
        code = parent_entity.code + ":" + entity.name
        entity.space_id = parent_entity.space_id
    else:
        space = get_space_by_id(db, entity.space_id)
        code = space.code + "-" + entity.name

    if get_entity_by_code(db, code):
        raise RuntimeError("Entity with code already exists")

    if db_entity.parent_id == 0:
        db_entity.parent_id = None

    if db_entity.space_id == 0:
        db_entity.space_id = None

    db_entity.code = code

    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity


def get_asset_by_id(db: Session, id: int):
    return db.query(models.Asset).filter(models.Asset.id == id).first()


def get_assets(db: Session, code: str = "", skip: int = 0, limit: int = 100):
    query = db.query(models.Asset)
    if code:
        query = query.filter(models.Asset.code == code)

    return query.offset(skip).limit(limit).all()


def get_asset_versions(
    db: Session, skip: int = 0, limit: int = 100, name: str = None, asset_id: int = None
):
    query = db.query(models.AssetVersion)
    if name:
        query = query.filter(models.AssetVersion.name == name)
    if asset_id:
        query = query.filter(models.AssetVersion.asset_id == asset_id)
    return query.offset(skip).limit(limit).all()


def get_asset_by_code(db: Session, code: str):
    return db.query(models.Asset).filter(models.Asset.code == code).first()


def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.dict())

    entity = get_entity_by_id(db, asset.entity_id)
    code = entity.code + "-" + asset.name

    if get_asset_by_code(db, code):
        raise RuntimeError("Asset with code already exists")

    db_asset.code = code

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


def get_asset_version_by_code(db: Session, code: str):
    return (
        db.query(models.AssetVersion).filter(models.AssetVersion.code == code).first()
    )


def get_asset_versions(
    db: Session, skip: int = 0, limit: int = 100, name: str = None, asset_id: int = None
):
    query = db.query(models.AssetVersion)
    if name:
        query = query.filter(models.AssetVersion.name == name)
    if asset_id:
        query = query.filter(models.AssetVersion.asset_id == asset_id)

    return query.offset(skip).limit(limit).all()


def create_asset_version(db: Session, asset_version: schemas.AssetVersionCreate):
    db_asset_version = models.AssetVersion(**asset_version.dict())

    asset = get_asset_by_id(db, asset_version.asset_id)

    total_asset_versions = len(asset.asset_versions)
    total_asset_versions += 1
    db_asset_version.version = total_asset_versions
    code = asset.code + "@" + str(total_asset_versions)

    if get_asset_version_by_code(db, code):
        raise RuntimeError("AssetVersion with code already exists")

    db_asset_version.code = code
    db_asset_version.name = str(total_asset_versions)
    entity_names = []
    entity = get_entity_by_id(db, asset.entity_id)
    space = get_space_by_id(db, entity.space_id)
    while entity:
        entity_names.append(entity.name)
        entity = get_entity_by_id(db, entity.parent_id)
    entity_names.reverse()
    entities_dirs = "/".join(entity_names)
    db_asset_version.rel_data_dir = (
        f"{space.code}/{entities_dirs}/{asset.name}/v{total_asset_versions}"
    )
    db_asset_version.data_dir = DATA_ROOT + "/" + db_asset_version.rel_data_dir

    db.add(db_asset_version)
    db.commit()
    db.refresh(db_asset_version)
    return db_asset_version


def get_asset_files(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: str = None,
    asset_version_id: int = None,
):
    query = db.query(models.AssetFile)
    if name:
        query = query.filter(models.AssetFile.name == name)
    if asset_version_id:
        query = query.filter(models.AssetFile.asset_version_id == asset_version_id)
    return query.offset(skip).limit(limit).all()


def get_asset_version_by_id(db: Session, id: int):
    return db.query(models.AssetVersion).filter(models.AssetVersion.id == id).first()


def create_asset_file(db: Session, asset_file: schemas.AssetFileCreate):
    asset_version = get_asset_version_by_id(db, asset_file.asset_version_id)
    db_asset_file = models.AssetFile(**asset_file.dict())
    db_asset_file.rel_path = asset_file.name
    db_asset_file.path = asset_version.data_dir + "/" + asset_file.name
    db.add(db_asset_file)
    db.commit()
    db.refresh(db_asset_file)
    return db_asset_file
