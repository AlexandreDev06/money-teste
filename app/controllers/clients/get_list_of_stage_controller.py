from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token
from app.models.clients import ClientPipelineStatus as Stage


async def get_list_of_clients(stage: Stage, _=Depends(validate_token)):
    """Retrieves a list of clients based on the provided stage.

    Args:
        stage (Stage): The stage to filter the clients by.
        _ (Depends): The token validation dependency.
    """
    data = await ClientsManager().select_by_pipeline_status(stage.name)
    return {"status": "Success", "data": data}
