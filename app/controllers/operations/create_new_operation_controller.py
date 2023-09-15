import io
import re

import pandas
from fastapi import Depends, HTTPException, UploadFile

from app.crud.clients_crud import ClientsManager
from app.crud.motor_runnings_crud import MotorRunningsManager
from app.crud.operations_crud import OperationsManager
from app.helpers.validate_token import validate_token
from app.models.motor_runnings import MotorRunningStatus, MotorType


async def create_new_operation(file: UploadFile, _=Depends(validate_token)):
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
            await MotorRunningsManager().insert({"operation_id": operation.id})

        list_clients.append(
            {
                "cpf": re.sub(r"[.\-, ]", "", str(row["cpf"])),
                "operation_id": operation.id,
            }
        )

    await ClientsManager().add_multiple_clients(list_clients)

    for stage in MotorType:
        await MotorRunningsManager().insert(
            {
                "status": MotorRunningStatus.FINISHED,
                "motor_type": stage,
                "operation_id": operation.id,
            }
        )

    return {"status": "success"}
