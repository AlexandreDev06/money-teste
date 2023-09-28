from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token


async def get_pending_clients(_=Depends(validate_token)):
    """Endpoint that check all clients that don't have any pipeline status associated.
    Returns:
        list: List of clients that don't have any pipeline status associated.
    """
    clients = await ClientsManager().get_pending_clients()
    return {"status": "success", "clients": clients}
