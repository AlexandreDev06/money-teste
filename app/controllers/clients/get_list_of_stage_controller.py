from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token
from app.models.clients import ClientPipelineStatus as Satage


async def get_list_of_clients(stage: Satage, _=Depends(validate_token)):
    """Retrieves a list of clients based on the provided stage.

    Args:
        stage (Satage): The stage to filter the clients by.
        _ (Depends): The token validation dependency.
    """
    data = await ClientsManager().select_by_pipeline_status(stage.name)
    return {"status": "Success", "data": data}
