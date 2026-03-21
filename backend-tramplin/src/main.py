import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan():
    ...



app: FastAPI = FastAPI(
    lifespan=lifespan
)


