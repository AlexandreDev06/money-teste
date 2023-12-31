from datetime import datetime

from app.crud.client_operations_crud import ClientOperationsManager
from app.crud.clients_crud import ClientsManager
from app.crud.motor_runnings_crud import MotorRunningsManager
from app.crud.timelines_crud import TimelineManager
from app.external.irpf_situation_service import IrpfSituationService
from app.helpers.run_func_async import run_func_async
from app.models.client_operations import ClientOperationSearchIrpfStatus as Cois
from app.models.clients import ClientPipelineStatus as Cps
from app.models.clients import ClientSearchIrpfStatus as Csis
from app.models.motor_runnings import MotorRunningStatus as Mrs
from app.models.timelines import TimelinePipelineStatus, TimelineSource
from app.worker.celery import app


@app.task(bind=True, name="start_check_eligibility")
@run_func_async()
async def start_check_eligibility(_, motor_id: int):
    """Job that will manage all clients able to be enriched."""
    motor = await MotorRunningsManager().get(motor_id)
    if motor.status == Mrs.PAUSED:
        return "Motor running paused"

    await MotorRunningsManager().update(motor_id, {"status": Mrs.IN_PROGRESS})
    clients = await ClientsManager().get_by_pipeline_and_operation(
        Cps.ELIGIBILITY, motor.operation_id
    )

    for client in clients:
        if client.search_irpf_status == Csis.SUCCESS:
            continue

        data_client = {
            "id": client.id,
            "cpf": client.cpf,
            "birth_date": client.birth_date.strftime("%Y%m%d"),
            "motor_id": motor_id,
        }
        check_eligibility.delay(data_client)
    return "Successfuly called clients to eligibility"


@app.task(bind=True, name="check_eligibility")
@run_func_async()
async def check_eligibility(_, data_client: dict):
    """Job that will manage all clients able to be enriched."""
    date_now = datetime.now().year
    list_clients_operation = []
    client = await ClientsManager().get_with_details(data_client["id"])
    years_eligibility = [co.year for co in client.client_operations]
    print(years_eligibility)

    if data_client["motor_id"]:
        motor = await MotorRunningsManager().get(data_client["motor_id"])

        if motor.status == Mrs.PAUSED:
            return "Motor running paused"

    for i in range(5):
        if date_now - i in years_eligibility:
            continue

        data = {
            "cpf": data_client["cpf"],
            "year": date_now - i,
            "birth_date": data_client["birth_date"],
        }
        client_res = await IrpfSituationService().get_situation(data)
        if client_res:
            list_clients_operation.append(
                {
                    "client_id": data_client["id"],
                    "year": data["year"],
                    "irpf_situation": client_res,
                    "search_irpf_status": Cois.SUCCESS,
                }
            )

    await ClientOperationsManager().add_multiple(list_clients_operation)
    await ClientsManager().update(
        data_client["id"],
        {"search_irpf_status": Csis.SUCCESS, "pipeline_status": Cps.CONTACT},
    )
    await TimelineManager().insert(
        {
            "client_id": data_client["id"],
            "pipeline_status": TimelinePipelineStatus.CONTACT,
            "source": TimelineSource.SPREADSHEET,
        }
    )

    return "Successfuly called clients"
