from app.configs.database import DBConnection
from app.models import ClientOperation


class ClientOperationManager:
    """Client Operation manager."""

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
