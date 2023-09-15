from app.crud.clients_crud import ClientsManager
from app.crud.motor_runnings_crud import MotorRunningsManager
from app.helpers.run_func_async import run_func_async
from app.models.clients import ClientPipelineStatus as Cps
from app.models.motor_runnings import MotorRunningStatus as Mrs
from app.worker.celery import app


@app.task(bind=True, name="check_eligibility")
@run_func_async()
async def check_eligibility(_, motor_id: int):
    """Job that will manage all clients able to be enriched."""
    motor = await MotorRunningsManager().get(motor_id)
    if motor.status == Mrs.PAUSED:
        return "Motor running paused"

    await MotorRunningsManager().update(motor_id, {"status": Mrs.IN_PROGRESS})
    clients = await ClientsManager().get_by_pipeline_and_operation(
        Cps.ENRICHMENT, motor.operation_id
    )
    for client in clients:
        data_client = {
            "id": client.id,
            "cpf": client.cpf,
            "is_enriched": client.is_enriched,
        }
    return "Successfuly called clients to enrich"
