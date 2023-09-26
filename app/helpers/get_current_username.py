import secrets

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.configs.settings import settings as st
from app.exceptions import CredentialsException


def get_current_username(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    """Get current username"""
    correct_username = secrets.compare_digest(credentials.username, st.super_email)
    correct_password = secrets.compare_digest(credentials.password, st.super_password)
    if not (correct_username and correct_password):
        raise CredentialsException("Invalid username or password")
    return credentials.username
