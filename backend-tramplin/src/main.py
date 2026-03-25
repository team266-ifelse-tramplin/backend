from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from services.opportunity import OpportunityMaster


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.op_master = OpportunityMaster()


app: FastAPI = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.default_host,
        port=settings.default_port,
        reload=settings.server_reload,
    )
