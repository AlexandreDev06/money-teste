from app.configs.database import DBConnection
from app.models import Client


class ClientsManager:
    """Clients manager class"""

    async def add_multiple_clients(self, data_clients: list[dict]) -> list[Client]:
        """Adds multiple clients to the database.

        Args:
            clients (List[Client]): The list of clients to be added to the database.

        Returns:
            List[Client]: The list of clients added to the database.
        """
        with DBConnection() as conn:
            try:
                conn.session.add_all([Client(**client) for client in data_clients])
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def update(self, client_id: int, data: dict) -> None:
        with DBConnection() as conn:
            try:
                conn.session.query(Client).filter(Client.id == client_id).update(data)
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)
