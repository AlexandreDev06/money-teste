from sqlalchemy import select

from app.configs.database import DBConnection
from app.models import Client


class ClientsManager:
    """Clients manager class"""

    async def add_multiple_clients(self, data_clients: list[dict]) -> None:
        """Adds multiple clients to the database.

        Args:
            clients (List[Client]): The list of clients to be added to the database.
        """
        with DBConnection() as conn:
            try:
                conn.session.add_all([Client(**client) for client in data_clients])
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def update(self, client_id: int, data: dict) -> None:
        """Updates the stage of a client in the pipeline."""
        with DBConnection() as conn:
            try:
                conn.session.query(Client).filter(Client.id == client_id).update(data)
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def select_by_pipeline_status(self, pipeline_status: str) -> list[Client]:
        """Retrieve a list of clients based on the pipeline status."""
        with DBConnection() as conn:
            try:
                query = select(Client).where(Client.pipeline_status == pipeline_status)
                return conn.session.scalars(query).all()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def get_by_operation(self, operation_id: int) -> Client:
        """Get all clients by operation id"""
        with DBConnection() as conn:
            try:
                return (
                    conn.session.query(Client)
                    .filter(Client.operation_id == operation_id)
                    .all()
                )
            except Exception as exe:
                conn.session.rollback()
                print(exe)
