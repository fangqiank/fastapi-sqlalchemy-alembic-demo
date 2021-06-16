from typing import List

import uvicorn

from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from db import crud, models, schemas
from db.database import SessionLocal, engine

import databases
from sqlalchemy import engine_from_config, pool

# from logging.config import fileConfig
# from alembic import context


# import datetime

# from db import models
# from db.models import SessionLocal, engine
#from sqlalchemy import engine_from_config, pool
#from pydantic import BaseModel
#from logging.config import fileConfig
#from alembic import context

# from typing import List
# import databases
# import sqlalchemy
# import urllib
# import psycopg2

# DATABASE_URL = 'postgres://fbhvncbw:Ki23owqInLDR_xIUXQj373MJ5KuRI1r8@kashin.db.elephantsql.com/fbhvncbw?sslmode=prefer'

# database = databases.Database(DATABASE_URL)

# metadata = sqlalchemy.MetaData()

# class PollType(enum.Enum):
#     text = 1
#     image =2

# users = sqlalchemy.Table(
#     "users",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("username", sqlalchemy.String(30), nullable=False),
#     sqlalchemy.Column("email", sqlalchemy.String(100), nullable=False),
#     # sqlalchemy.Column("completed", sqlalchemy.Boolean),
# )

# polls = sqlalchemy.Table(
#     "polls",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("title", sqlalchemy.String(255), nullable=False),
#     sqlalchemy.Column("type", sqlalchemy.Enum(PollType), nullable=False),
#     sqlalchemy.Column("is_add_choices_active", sqlalchemy.Boolean),
#     sqlalchemy.Column("is_voting_active", sqlalchemy.Boolean),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False),
# )


# engine = sqlalchemy.create_engine(
#     DATABASE_URL, pool_size=3, max_overflow=0
# )
# metadata.create_all(engine)

# config = context.config
# fileConfig(config.config_file_name)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/polls/", response_model=schemas.Poll)
def create_poll_for_user(
    user_id: int, poll: schemas.PollCreate, db: Session = Depends(get_db)
):
    return crud.create_user_poll(db=db, poll=poll, user_id=user_id)


@app.get("/polls/", response_model=List[schemas.Poll])
def read_poll(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    polls = crud.get_polls(db, skip=skip, limit=limit)
    return polls

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)