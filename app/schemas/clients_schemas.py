from pydantic import BaseModel

from app.models.clients import ClientPipelineStatus


class UpdateStage(BaseModel):
    """Update stage"""

    client_id: int
    stage_name: ClientPipelineStatus
