from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from database import engine
from router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(docs_url="/docs", lifespan=lifespan)
app.include_router(router)
