from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token
from app.schemas.clients_schemas import UpdateStage


async def update_stage(data: UpdateStage, _=Depends(validate_token)):
    """Updates the stage of a client in the pipeline.

    Parameters:
        data (UpdateStage): The data object containing the client ID and the new stage name.

    Returns:
        DefaultResponse: The response object with the status of the update operation.
    """
    await ClientsManager().update(data.client_id, {"pipeline_status": data.stage_name})
    return {"status": "Success"}
