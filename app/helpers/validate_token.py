from app.configs.settings import settings
from app.exceptions import CredentialsException
import requests
from fastapi.security import OAuth2PasswordBearer
from fastapi.params import Depends
from pydantic import BaseModel

oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
LAWTECH_API = settings.lawtech_api


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
            f"{LAWTECH_API}/valid-token",
            headers={"Authorization": f"Bearer {token}"},
        )
    except Exception as e:
        print(e)
        raise e

    if response.status_code == 401:
        raise CredentialsException()

    return response.json()["data"]
