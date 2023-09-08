from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app import exceptions as exe
from app.routes import routers

app = FastAPI(title="Recdin Money Api", version="0.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle data model error
app.exception_handler(RequestValidationError)(exe.validation_exception_handler)
app.exception_handler(exe.ValueNotFound)(exe.value_not_found)
app.exception_handler(exe.CredentialsException)(exe.credentials_invalid_exception)

app.include_router(routers)
