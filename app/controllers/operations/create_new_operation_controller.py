import io

import pandas
from fastapi import HTTPException, UploadFile

from app.crud.clients_crud import ClientsManager
from app.crud.operations_crud import OperationsManager
from app.schemas import DefaultResponse


async def create_new_operation(file: UploadFile) -> DefaultResponse:
    """Adds clients by uploading a file.

    Args:
        file (UploadFile): The file to be loaded from csv xlsx format.

    Returns:
        DefaultResponse: The response indicating the status of the upload.
    """
    contents = await file.read()

    try:
        if file.filename.endswith("csv"):
            dataframe = pandas.read_csv(io.BytesIO(contents))
        else:
            dataframe = pandas.read_excel(contents)
    except Exception as exe:
        print(exe)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Error",
                "description": "Invalid file format, use CSV or XLSX",
            },
        )

    if not "cpf" in dataframe.columns or not "operation" in dataframe.columns:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Error",
                "description": "column cpf and operation is required",
            },
        )

    list_clients = []
    opr_conn = OperationsManager()

    for _, row in dataframe.iterrows():
        operation_name = row["operation"]
        operation = await opr_conn.select_by_name(operation_name)

        if not operation:
            operation = await opr_conn.insert(operation_name)

        list_clients.append({"cpf": row["cpf"], "operation_id": operation.id})

    await ClientsManager().add_multiple_clients(list_clients)

    return {"status": "success"}
