from sqlalchemy import select

from app.configs.database import DBConnection
from app.models import MotorRunning, Operation
from app.models.motor_runnings import MotorRunningStatus as Mtstatus


class OperationsManager:
    """Clients manager class"""

    async def select_by_name(self, name: str) -> Operation:
        """Selects an operation from the database by name.

        Args:
            name (str): The name of the operation to select.

        Returns:
            Operation: The selected operation.
        """

        with DBConnection() as conn:
            try:
                query = select(Operation).where(Operation.name == name)
                operation = conn.session.scalars(query).first()
                return operation
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def insert(self, operation_name: str) -> Operation:
        """Adds multiple clients to the database.

        Args:
            clients (List[Client]): The list of clients to be added to the database.

        Returns:
            List[Client]: The list of clients added to the database.
        """
        with DBConnection() as conn:
            try:
                operation = Operation(name=operation_name)
                conn.session.add(operation)
                conn.session.commit()
                conn.session.refresh(operation)
                return operation
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def get_operations_by_stage(self, stage_name: str) -> list[Operation]:
        """Retrieves a list of operations associated with a specific stage in the pipeline.

        Args:
            stage_name (str): The name of the stage to filter the operations by.

        Returns:
            List[Operation]: A list of Operation objects representing the retrieved operations.
        """
        with DBConnection() as conn:
            try:
                query = (
                    select(
                        Operation.id,
                        Operation.name,
                        Operation.created_at,
                        MotorRunning.id,
                    )
                    .join(Operation.motor_runnings)
                    .where(
                        MotorRunning.motor_type == stage_name,
                        MotorRunning.status != Mtstatus.FINISHED,
                    )
                    .group_by(Operation.id, MotorRunning.id)
                )
                operations = []
                for col in conn.session.execute(query).all():
                    data = {
                        "id": col[0],
                        "name": col[1],
                        "created_at": col[2],
                        "motor_running_id": col[3],
                    }
                    operations.append(data)

                return operations
            except Exception as exe:
                conn.session.rollback()
                print(exe)
