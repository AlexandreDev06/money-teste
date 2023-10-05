from app.crud.clients_crud import ClientsManager
from app.worker.jobs.eligibility import check_eligibility


async def check_eligibility_client(client_id: int):
    """Job that will manage all clients able to be enriched."""
    client = await ClientsManager().get_client_by("id", client_id)
    data = {
        "id": client.id,
        "cpf": client.cpf,
        "birth_date": client.birth_date.strftime("%Y%m%d"),
        "motor_id": None,
    }
    check_eligibility.delay(data)
    return {"status": "Success"}
