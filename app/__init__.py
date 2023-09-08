from app import exceptions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configs.settings import settings
from app.routes import routers

app = FastAPI(title="Recdin Money Api", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.exception_handler(exceptions.CredentialsException)(exceptions.credentials_invalid_exception)
app.include_router(routers)