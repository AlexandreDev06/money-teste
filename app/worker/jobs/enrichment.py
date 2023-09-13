from app.models.motor_runnings import MotorRunningStatus as motor_status
from app.crud.motor_runnings_crud import MotorRunningsManager
from app.crud.clients_crud import ClientsManager
from app.models.clients import Client
from app.models.motor_runnings import MotorRunning
from app.external.volpe_api import Volpe
from app.worker.celery import app
from app.helpers.run_func_async import run_func_async


@app.task(bind=True, name="call_clients_to_enrich")
@run_func_async()
async def call_clients_to_enrich(self, motor_id: int):
    """Job that will manage all clients able to be enriched."""
    motor = await MotorRunningsManager().get(motor_id)
    if motor.status == motor_status.PAUSED:
        return "Motor running paused"

    await MotorRunningsManager().update(
        {"id": motor.id, "status": motor_status.IN_PROGRESS}
    )
    clients = await ClientsManager().get_by_operation(motor.operation_id)
    print(clients)

    for client in clients:
        data_client = {"id": client.id, "is_enriched": client.is_enriched}
        enrich_client.delay(data_client, motor.id)

    return f"Hello"


@app.task(bind=True, name="enrich_client")
@run_func_async()
async def enrich_client(self, client: dict, motor_id: int):
    """Job that will enrich a client and motor data in bd."""
    motor = await MotorRunningsManager().get(motor_id)
    if motor.status == motor_status.PAUSED:
        return "Motor running paused"

    if client["is_enriched"]:
        return "Client already enriched"

    volpe_data = ""
    print(volpe_data)

    return f"Hello"