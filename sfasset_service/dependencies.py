from typing import Annotated

from fastapi import Header, HTTPException
from .database import SessionLocal

TOKEN_REQUIRED = False


async def get_token_header(x_token: Annotated[str, Header()]):
    if not TOKEN_REQUIRED:
        return

    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
