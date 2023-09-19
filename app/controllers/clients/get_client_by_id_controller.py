from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token


async def get_client_by_id(client_id: int, _=Depends(validate_token)):
    """Get client for screen negociation by id.
    Args: client_id (int): The client id.
    """
    client = await ClientsManager().get_with_details(client_id)
    return {"status": "success", "data": client}
