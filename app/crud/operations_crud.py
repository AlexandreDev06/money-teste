from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.configs.database import DBConnection
from app.models import Operation


class OperationsManager:
    """Clients manager class"""

    async def select_by_name(self, name: str) -> Operation:
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
