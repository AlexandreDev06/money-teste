from sqlalchemy import select, text, update

from app.configs.database import DBConnection
from app.models.client_operations import ClientOperation


class ClientOperationsManager:
    """Client operations manager class"""

    async def update(self, id: int, data: dict) -> None:
        """Updates a client operation.

        Args:
            id (int): The client operation id.
            data (dict): The data to be updated.
        """
        with DBConnection() as conn:
            try:
                query = (
                    update(ClientOperation)
                    .where(ClientOperation.id == id)
                    .values(**data)
                )
                conn.session.execute(query)
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def add_multiple(self, data_list: list[dict]) -> None:
        """Adds multiple clients to the database.

        Args:
            clients (List[Client]): The list of clients to be added to the database.
        """
        with DBConnection() as conn:
            try:
                conn.session.add_all([ClientOperation(**data) for data in data_list])
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def get_client_operations_by(
        self, field: str, value: str
    ) -> list[ClientOperation]:
        """Gets a client by a specific field.

        Args:
            field (str): The field to be used in the query.
            value (str): The value to be used in the query.

        Returns:
            Client: The client objects.
        """
        with DBConnection() as conn:
            query = select(ClientOperation).where(
                getattr(ClientOperation, field) == value
            )
            result = conn.session.execute(query).scalars().all()
            return result
