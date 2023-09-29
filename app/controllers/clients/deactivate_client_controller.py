from app.crud.clients_crud import ClientsManager


async def deactivate_client(client_id: int):
    """Deactivate client by id, deleting timeliens, task, notes and client_operations.

    Args:
        client_id (int): Client id.
    """
    try:
        await ClientsManager().deactive_client(client_id)
    except Exception as exe:
        print(exe)
        return {"status": "error", "message": exe}
    
    return {"status": "success", "message": "Client deactivated"}
