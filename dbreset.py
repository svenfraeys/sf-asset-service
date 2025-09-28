#!/usr/bin/env python
"""
Drop the database and recreate the tables
"""


def main():
    print("Resetting the database")
    from sfasset_service import database

    print("Dropping all tables")
    database.Base.metadata.drop_all(bind=database.engine)
    print("Creating all tables")
    database.Base.metadata.create_all(bind=database.engine)
    print("Done!")


if __name__ == "__main__":
    main()
