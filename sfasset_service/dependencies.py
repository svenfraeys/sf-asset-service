import os
from typing import Annotated

from fastapi import Header, HTTPException
from .database import SessionLocal

TOKEN_REQUIRED = False


async def get_token_header(x_token: Annotated[str, Header()]):
    if not TOKEN_REQUIRED:
        return

    if x_token != os.getenv("SECRET_TOKEN", "fake-super-secret-token"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
