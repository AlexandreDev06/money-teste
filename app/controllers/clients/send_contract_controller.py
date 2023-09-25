from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.external.zapsign import Zapsign
from app.helpers.validate_token import validate_token


async def send_contract(client_id: int, _=Depends(validate_token)):
    """Send contract to client."""
    client = await ClientsManager().get_with_details(client_id)

    data = {
        "client_id": client_id,
        "name": client.name,
        "cpf": client.cpf,
        "address": client.full_adress,
        "birth_date": client.birth_date.strftime("%d/%m/%Y"),
        "email": client.email,
        "year": "2023",
    }
    await Zapsign().send_contract_zapsign(data)
    return {"status": "success"}
