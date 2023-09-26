from app.crud.clients_crud import ClientsManager


async def get_result_client_by_id(client_id: int):
    """Get client for screen negociation by id.
    Args: client_id (int): The client id.
    """
    client = await ClientsManager().get_with_details(client_id)
    data = {
        "name": client.name,
        "email": client.email[0],
        "cpf": client.cpf,
        "phone": client.phone[0],
        "birth_date": client.birth_date.strftime("%d/%m/%Y"),
        "address": client.full_adress,
        "amount_to_receive": 10000.00,
    }
    return {"status": "success", "data": data}
