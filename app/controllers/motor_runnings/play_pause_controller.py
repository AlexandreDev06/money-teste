from app.schemas import DefaultResponse
from app.crud.motor_runnings_crud import MotorRunningsManager
from app.models.motor_runnings import MotorRunningStatus as motor_status
from app.helpers.validate_token import Admin, validate_token
from fastapi import Depends
import pdb
from app.worker.jobs.enrichment import call_clients_to_enrich


async def play_pause(
    id: int, current_user: Admin = Depends(validate_token)
) -> DefaultResponse:
    """Play or pause a motor_running and call related services to run.
    Args:
        id (int): motor running id
    """
    motor = await MotorRunningsManager().get(id)
    if not motor:
        return {"status": "error", "message": "Motor running not found"}

    if motor.status in [motor_status.PAUSED, motor_status.FINISHED]:
        await MotorRunningsManager().update(
            {"id": id, "status": motor_status.IN_PROGRESS}
        )
        # Here make a call relationed worker
        call_clients_to_enrich.delay(motor.id)
    else:
        await MotorRunningsManager().update({"id": id, "status": motor_status.PAUSED})

    return {"status": "success"}
