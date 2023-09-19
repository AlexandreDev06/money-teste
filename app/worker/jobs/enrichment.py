from datetime import datetime

from app.crud.clients_crud import ClientsManager
from app.crud.motor_runnings_crud import MotorRunningsManager
from app.external.volpe_api import Volpe
from app.helpers.run_func_async import run_func_async
from app.models.clients import ClientPipelineStatus
from app.models.motor_runnings import MotorRunningStatus as mts
from app.worker.celery import app


@app.task(bind=True, name="call_clients_to_enrich")
@run_func_async()
async def call_clients_to_enrich(_, motor_id: int):
    """Job that will manage all clients able to be enriched."""
    motor = await MotorRunningsManager().get(motor_id)
    if motor.status == mts.PAUSED:
        return "Motor running paused"

    await MotorRunningsManager().update(motor.id, {"status": mts.IN_PROGRESS})
    clients = await ClientsManager().get_by_pipeline_and_operation(
        ClientPipelineStatus.ENRICHMENT, motor.operation_id
    )

    for client in clients:
        if motor.status == mts.PAUSED:
            return "Motor running paused"

        if client.is_enriched:
            print("Client already enriched")
            continue
        try:
            volpe_data = Volpe().search_cpf_data(client.cpf)
            if not volpe_data:
                raise ValueError("Volpe API instável.")

            full_address = Volpe().search_data_volpe("full_address", volpe_data)
            emails = Volpe().search_data_volpe("email", volpe_data, True)
            phone_numbers = Volpe().search_data_volpe("home_phone", volpe_data, True)

            birth_date = ""
            if "/" in volpe_data["birth_date"]:
                birth_date = datetime.strptime(volpe_data["birth_date"], "%d/%m/%Y")
            elif "-" in volpe_data["birth_date"]:
                birth_date = datetime.strptime(
                    volpe_data["birth_date"], "%Y-%m-%d %H:%M:%S"
                )

            await ClientsManager().update(
                client.id,
                {
                    "is_enriched": True,
                    "name": volpe_data["name"],
                    "street": [full_address["address"]],
                    "house_number": [full_address["address_number"]],
                    "district": [full_address["district"]],
                    "city": [full_address["city"]],
                    "state": [full_address["state"]],
                    "cep": [full_address["cep"]],
                    "email": emails,
                    "phone": phone_numbers,
                    "birth_date": birth_date,
                    "pipeline_status": ClientPipelineStatus.ELIGIBILITY,
                },
            )
        except Exception as e:
            print(f"Cliente id:{client.id}. não foi enriquecido. Error: {e}")

    await MotorRunningsManager().update(motor.id, {"status": mts.FINISHED})
    return "Successfuly called clients to enrich, amount: " + str(len(clients))
