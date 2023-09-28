from app.crud.clients_crud import ClientsManager
from app.helpers.cpf import validate_and_clean_cpf
from app.schemas.landing_page import PriorityData


async def selected_data_of_client(client_data: PriorityData):
    """Save the selected data of the client in the database with priority.\n
    Args:\n
        data: Schema of the data to save.
        Field "address" is a dict with the following structure:
            {
                "cep": "00000-000",
                "street": "Rua dos Bobos",
                "house_number": "0, Apto 0",
                "district": "Vila do Chaves",
                "city": "São Paulo",
                "state": "SP"
            }
    """
    cpf = await validate_and_clean_cpf(client_data.cpf)
    client = await ClientsManager().get_client_by("cpf", cpf)

    if not client:
        return {"status": "error", "message": "Cliente não encontrado."}

    await ClientsManager().update(
        client.id,
        {
            "email": [client_data.email],
            "phone": [client_data.phone],
            "street": [client_data.address['street']],
            "cep": [client_data.address['cep']],
            "house_number": [client_data.address['house_number']],
            "district": [client_data.address['district']],
            "city": [client_data.address['city']],
            "state": [client_data.address['state']],
        },
    )
    return {"status": "success"}
