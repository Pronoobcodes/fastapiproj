from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from database.database import engine
from app.routes import manger_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(manger_router)


