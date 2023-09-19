from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.crud.motor_runnings_crud import MotorRunningsManager
from app.helpers.validate_token import validate_token
from app.models.motor_runnings import MotorRunning, MotorRunningStatus, MotorType
from app.worker import call_clients_to_enrich, start_check_eligibility


async def play_pause(
    operation_id: int, motor_type: MotorType, _=Depends(validate_token)
):
    """Play or pause a motor_running and call related services to run.

    Args:
        motor_id (int): motor running id
    """
    motor = await MotorRunningsManager().get_by_operation_and_motor_type(
        operation_id, motor_type
    )

    if motor.status == MotorRunningStatus.IN_PROGRESS:
        await MotorRunningsManager().update(
            motor.id, {"status": MotorRunningStatus.PAUSED}
        )

    else:
        await MotorRunningsManager().update(
            motor.id, {"status": MotorRunningStatus.IN_PROGRESS}
        )
        await __call_function_by_motor_type__(motor)

    return {"status": "success"}


async def __call_function_by_motor_type__(motor: MotorRunning):
    """Method to call workers and other functions by motor type."""
    if motor.motor_type == MotorType.ENTRY:
        await ClientsManager().update_all_to_next_stage(motor.operation_id)
        await MotorRunningsManager().update(
            motor.id, {"status": MotorRunningStatus.FINISHED}
        )
    elif motor.motor_type == MotorType.ENRICHMENT:
        call_clients_to_enrich.delay(motor.id)
    elif motor.motor_type == MotorType.ELIGIBILITY:
        start_check_eligibility.delay(motor.id)
