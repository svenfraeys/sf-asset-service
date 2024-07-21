#!/usr/bin/env python


def main():
    print("reset")
    from sfasset_service import database

    database.Base.metadata.drop_all(bind=database.engine)
    # database.Base.metadata.create_all(bind=database.engine)

    print("done")


if __name__ == "__main__":
    main()
