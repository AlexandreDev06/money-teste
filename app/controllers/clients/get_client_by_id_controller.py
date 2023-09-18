from fastapi import Depends

from app.crud.client_operations_crud import ClientOperationsManager
from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token


async def get_client_by_id(client_id: int, _=Depends(validate_token)):
    """Get client information by id.
    Args: client_id (int): The client id.
    """
    client_response = {}

    client = await ClientsManager().get(client_id)
    client_response = client.__dict__
    client_response["client_operations"] = []

    client_operations = await ClientOperationsManager().get_by_client(client_id)
    print(client_response)
    for client_operation in client_operations:
        client_response["client_operations"].append(client_operation.__dict__)

    return {"status": "success", "data": client_response}
