from app.crud.client_operations_crud import ClientOperationsManager
from app.crud.clients_crud import ClientsManager
from app.external.s3_storage import RemoteStorage
from app.schemas.clients_schemas import UpdateImages


async def save_files_from_ir(params: UpdateImages):
    """Upload files to db from client IR.\n
    Args:\n
        client_cpf (str): The client cpf.
        files (dict): The files to be uploaded. Ex:
        {
            "rg": {file_name: "imagem.png", file: "image/base64"},,
            "ir_2023": {file_name: "imagem.png", file: "image/base64"},
            "ir_2022": {file_name: "imagem.png", file: "image/base64"},
            "ir_2021": {file_name: "imagem.png", file: "image/base64"},
            "ir_2020": {file_name: "imagem.png", file: "image/base64"},
            "ir_2019": {file_name: "imagem.png", file: "image/base64"},
        }
    """
    client = await ClientsManager().get_client_by("cpf", params.cpf)
    if not client:
        return {"status": "error", "message": "Client not found"}

    client_operations = await ClientOperationsManager().get_client_operations_by(
        "client_id", client.id
    )

    for co in client_operations:
        file = params.files[f"ir_{co.year}"]
        file_name = f"{params.cpf}_{file['file_name']}"

        await RemoteStorage().save_base64(file["file"], file_name)
        await ClientOperationsManager().update(co.id, {"irpf_image": file_name})

    rg = params.files["rg"]
    file_name = f"{params.cpf}_{rg['file_name']}"

    await RemoteStorage().save_base64(rg["file"], file_name)
    await ClientsManager().update(client.id, {"document_file": file_name})

    return {"status": "success"}
