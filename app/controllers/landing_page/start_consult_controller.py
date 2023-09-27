from datetime import datetime
from pdb import set_trace

from app.crud.client_operations_crud import ClientOperationsManager
from app.crud.clients_crud import ClientsManager
from app.helpers.cpf import validate_and_clean_cpf
from app.worker.jobs.enrichment import enrich_one_client


async def start_consult(cpf: str, birth_date: str):
    """Starts a consult.\n
    If the client is not registered, it will be registered in pending_registrations and call enrichment.
    if exists, check if is in flow and return this, if not, do nothing.\n
    Args:\n
        cpf (str): The client's cpf. ex: 111.222.333-44
        birth_date (str): The client's birth_date. ex: 17/10/2000
    """
    try:
        client = await ClientsManager().get_client_by("cpf", cpf)
        cpf = await validate_and_clean_cpf(cpf)
        birth_date = birth_date = datetime.strptime(birth_date, '%d/%m/%Y')

        if not client:  
            client_id = await ClientsManager().insert({
                "cpf": cpf,
                "birth_date": birth_date,
                "source": "LANDING_PAGE",
            })

            date_now = datetime.now().year
            list_clients_operation = []
            for i in range(5):
                list_clients_operation.append(
                    {
                        "client_id": client_id,
                        "year":  date_now - i,
                    }
                )
            await ClientOperationsManager().add_multiple(list_clients_operation)

            enrich_one_client.delay(client_id)
        else:
            if client.pipeline_status in range(17, 23):
                return {"status": "error", "description": "Cliente já está no fluxo."}

            if not client.is_enriched:
                enrich_one_client.delay(client.id)
    except Exception as exe:
        print(exe)
        return {"status": "error", "description": exe}

    return {"status": "success"}
