from fastapi import Depends

from app.crud.clients_crud import ClientsManager
from app.helpers.validate_token import validate_token


async def get_pipeline_cards(
    page: int = 1,
    per_page: int = 20,
    order_by: str = "created_at",
    order: str = "ASC",
    source: str = "DIRF,SPREADSHEET,LANDING_PAGE",
    _=Depends(validate_token),
):
    """Get all stages and their clients for use in pipeline view."""
    source = source.split(",")
    clients = await ClientsManager().get_pipeline_clients(
        page, per_page, order_by, order, source
    )
    next = None
    for i in clients:
        if clients[i] and len(clients[i]) == 20:
            next = page + 1

    return {
        "status": "success",
        "pagination": {"prev": max(page - 1, 1), "prox": next},
        "data": clients,
    }
