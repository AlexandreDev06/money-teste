from app.crud.clients_crud import ClientsManager
from app.models.clients import ClientPipelineStatus as Cps
from app.schemas.clients_schemas import WebhookSignedContract


async def webhook_contract_signed(data: WebhookSignedContract):
    """Async function that handles the webhook for when a contract is signed.

    Args:
        data (WebhookSignedContract): The data received from the webhook
        containing information about the signed contract.
    """

    [project, client_id] = data.external_id.split("-")
    if project == "recdinmoney":
        await ClientsManager().update(
            client_id,
            {
                "signed_contract": data.signed_file,
                "pipeline_status": Cps.GENERAL_VERIFICATION,
            },
        )
        return {"status": "Success"}
