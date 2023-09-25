import requests
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.configs.settings import settings
from app.exceptions import CredentialsException

LAWTECH_API = settings.lawtech_api
oauth = OAuth2PasswordBearer(tokenUrl=f"{LAWTECH_API}login")


class Admin(BaseModel):
    """Admin model"""

    role: bool
    phone_number: str
    id: int
    name: str
    email: str
    role_money_api: str


async def validate_token(token: str = Depends(oauth)) -> Admin:
    """Validate the provided token by making an HTTP GET
    request to the LAWTECH_API's 'valid-token' endpoint.

    Args:
        token (str, optional): The token to be validated.
        Defaults to the result of calling the 'oauth' dependency.

    Returns:
        Admin: The validated token's data, returned as a JSON object.
    """
    response = requests.get(
        f"{LAWTECH_API}validate-token",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )

    if response.status_code == 200:
        return response.json()["data"]

    raise CredentialsException()
