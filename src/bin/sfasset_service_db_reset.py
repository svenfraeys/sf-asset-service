#!/usr/bin/env python
import sys


def main():
    sys.path.append(".")

    from sfasset_service_old.models import Base
    from sfasset_service_old.db import engine

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
