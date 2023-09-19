from sqlalchemy import select, update

from app.configs.database import DBConnection
from app.models import Client, Operation
from app.models.clients import ClientPipelineStatus as PipelineStatus


class ClientsManager:
    """Clients manager class"""

    async def get(self, client_id: int) -> Client:
        """Get client by id."""
        with DBConnection() as conn:
            try:
                query = select(Client).where(Client.id == client_id)
                return conn.session.scalars(query).first()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

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
                query = update(Client).where(Client.id == client_id).values(**data)
                conn.session.execute(query)
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

    async def get_pipeline_clients(self, page: int, per_page: int = 20) -> dict:
        """Get all clients by pipeline status with pagination"""
        pipeline_clients = {}

        with DBConnection() as conn:
            try:
                pipeline_status = [
                    status.name
                    for status in PipelineStatus
                    if status.name not in ["ENTRY", "ENRICHMENT"]
                ]
                for status in pipeline_status:
                    pipeline_clients[status.lower()] = []
                    query = (
                        select(
                            Client.id,
                            Client.name,
                            Client.cpf,
                            Client.created_at,
                            Operation.name,
                        )
                        .join(Client.operation)
                        .where(Client.pipeline_status == status)
                        .limit(per_page)
                        .offset((page - 1) * per_page)
                    )
                    results = conn.session.execute(query).all()

                    for id, name, cpf, created_at, operation_name in results:
                        pipeline_clients[status.lower()].append(
                            {
                                "id": id,
                                "name": name,
                                "cpf": cpf,
                                "created_at": created_at.strftime("%d/%m/%Y"),
                                "operation_name": operation_name,
                            }
                        )
            except Exception as exe:
                conn.session.rollback()
                print(exe)

        return pipeline_clients

    async def get_by_pipeline_and_operation(
        self, pipeline_status: str, operation_id: int
    ) -> list[Client]:
        """Get all clients by pipeline status and operation id"""
        with DBConnection() as conn:
            try:
                query = (
                    select(Client)
                    .where(Client.pipeline_status == pipeline_status)
                    .where(Client.operation_id == operation_id)
                )
                return conn.session.scalars(query).all()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def update_all_to_next_stage(self, operation_id: int):
        """Update all clients to next stage by pipeline_status"""
        with DBConnection() as conn:
            try:
                query = (
                    update(Client)
                    .where(Client.pipeline_status == PipelineStatus.ENTRY)
                    .where(Client.operation_id == operation_id)
                    .values(pipeline_status=PipelineStatus.ENRICHMENT)
                )
                conn.session.execute(query)
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)
