import requests
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.configs.settings import settings
from app.exceptions import CredentialsException

LAWTECH_API = settings.lawtech_api
oauth = OAuth2PasswordBearer(tokenUrl=f"{LAWTECH_API}login")


class Admin(BaseModel):
    role: bool
    phone_number: str
    id: int
    name: str
    email: str
    role_money_api: str


async def validate_token(token: str = Depends(oauth)) -> Admin:
    try:
        response = requests.get(
            f"{LAWTECH_API}validate-token",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
    except Exception as e:
        print(e)
        raise e

    if response.status_code == 401:
        raise CredentialsException()

    return response.json()["data"]
