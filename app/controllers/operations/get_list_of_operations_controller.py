from fastapi import Depends

from app.crud.operations_crud import OperationsManager
from app.helpers.validate_token import validate_token
from app.models.motor_runnings import MotorType


async def get_list_of_operations(stage: MotorType, _=Depends(validate_token)):
    """Retrieves a list of clients based on the provided stage.

    Args:
        stage (13 | 14 | 15): The stage to filter the clients by.
        _ (Depends): The token validation dependency.
    """
    data = await OperationsManager().get_operations_by_stage(stage)
    return {"status": "Success", "data": data}
