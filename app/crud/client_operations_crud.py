from sqlalchemy import select, text, update

from app.configs.database import DBConnection
from app.models.client_operations import ClientOperation


class ClientOperationsManager:
    """Client operations manager class"""

    async def get_by_client(self, client_id: int) -> ClientOperation:
        """Get client operation by client id."""
        with DBConnection() as conn:
            try:
                query = select(ClientOperation).where(ClientOperation.client_id == client_id)
                return conn.session.scalars(query).all()
            except Exception as exe:
                conn.session.rollback()
                print(exe)
