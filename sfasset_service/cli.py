import click
from sfasset_service import database
from sfasset_service.crud import create_user
from sfasset_service.schemas import UserCreate


@click.group()
def cli():
    pass


# Not @click so that the group is registered now.
@cli.group()
def session():
    click.echo("Starting session")


@cli.command()
def initdb():
    click.echo("Initialized the database")
    click.echo("Creating all tables")
    database.Base.metadata.create_all(bind=database.engine)
    click.echo("Done!")


@cli.command()
def dropdb():
    click.echo("Dropping the database")
    click.echo("Dropping all table")
    database.Base.metadata.drop_all(bind=database.engine)
    click.echo("Dropped the database")


@cli.command()
def install():
    print("Installing...")
    click.echo("Dropped the database")
    user = create_user(
        db=database.SessionLocal(), user=UserCreate(email="admin", password="admin")
    )
    print("Created user", user)
