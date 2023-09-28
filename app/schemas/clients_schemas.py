from pydantic import BaseModel

from app.models.clients import ClientPipelineStatus


class UpdateStage(BaseModel):
    """Update stage"""

    client_id: int
    stage_name: ClientPipelineStatus


class UpdateImages(BaseModel):
    """Update images"""

    cpf: str = "string"
    files: dict = {
        "rg": {"file_name": "imagem.png", "file": "image/base64"},
        "ir_2023": {"file_name": "imagem.png", "file": "image/base64"},
        "ir_2022": {"file_name": "imagem.png", "file": "image/base64"},
        "ir_2021": {"file_name": "imagem.png", "file": "image/base64"},
        "ir_2020": {"file_name": "imagem.png", "file": "image/base64"},
        "ir_2019": {"file_name": "imagem.png", "file": "image/base64"},
    }


class WebhookSignedContract(BaseModel):
    """Webhook signed contract"""

    signed_file: str
    name: str
    external_id: str
