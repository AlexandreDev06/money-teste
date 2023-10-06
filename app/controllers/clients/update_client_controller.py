from fastapi import Depends

from app.crud.client_operations_crud import ClientOperationsManager
from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token


async def update_client(id: int, data: dict, _=Depends(validate_token)):
    """Update client"""
    await ClientsManager().update(id, data)

    if data["client_operations"]:
        for co in data["client_operations"]:
            await ClientOperationsManager().update(co["id"], co)

    return {"status": "success", "message": "Updated client"}
