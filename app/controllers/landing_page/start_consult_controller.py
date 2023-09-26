from datetime import datetime

from app.crud.clients_crud import ClientsManager
from app.helpers.cpf import validate_and_clean_cpf
from app.worker.jobs.enrichment import enrich_one_client


async def start_consult(cpf: str, birth_date: str):
    """Starts a consult.
    If the client is not registered, it will be registered in pending_registrations and call enrichment.
    if exists, check if is in flow and return this, if not, do nothing.
    Args:
        cpf (str): The client's cpf. ex: 111.222.333-44
        birth_date (str): The client's birth_date. ex: 17/10/2000
    """
    try:
        client = await ClientsManager().get_client_by("cpf", cpf)
        cpf = await validate_and_clean_cpf(cpf)
        birth_date = birth_date = datetime.strptime(birth_date, '%d/%m/%Y')

        if not client:
            client = await ClientsManager().insert({
                "cpf": cpf,
                "birth_date": birth_date,
                "source": "LANDING_PAGE",
            })
            enrich_one_client.delay(client.id)
        else:
            if client.pipeline_status in range(17, 23):
                return {"status": "error", "description": "Cliente já está no fluxo."}

            if not client.is_enriched:
                enrich_one_client.delay(client.id)
    except Exception as exe:
        print(exe)
        return {"status": "error", "description": exe}

    return {"status": "success"}
