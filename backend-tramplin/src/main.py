import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


async def lifespan():
    ...



app: FastAPI = FastAPI(
    ...
)


