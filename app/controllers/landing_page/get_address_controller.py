from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token


async def get_address(client_id: int, _=Depends(validate_token)):
    """Get client for screen negociation by id.
    Args: client_id (int): The client id.
    """
    list_of_address = []
    client = await ClientsManager().get(client_id)
    for i, street in enumerate(client.street):
        list_of_address.append(
            {
                "street": street,
                "district": client.district[i],
                "house_number": client.house_number[i],
                "city": client.city[i],
                "state": client.state[i],
                "cep": client.cep[i],
            }
        )
    return {"status": "success", "data": list_of_address}
