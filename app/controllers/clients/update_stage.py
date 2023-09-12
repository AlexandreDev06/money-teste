from app.crud.clients_crud import ClientsManager
from app.schemas import DefaultResponse
from app.schemas.clients_schemas import UpdateStage


async def update_stage(data: UpdateStage) -> DefaultResponse:
    await ClientsManager().update(data.client_id, {"pipeline_status": data.stage_name})
    return {"status": "Success"}
