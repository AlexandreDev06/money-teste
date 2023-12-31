from datetime import datetime, timedelta

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import joinedload

from app.configs.database import DBConnection
from app.models import Client, Operation
from app.models.client_operations import ClientOperation
from app.models.clients import ClientPipelineStatus as PipelineStatus
from app.models.notifications import Notification
from app.models.tasks import Task
from app.models.timelines import Timeline, TimelineSource


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

    async def insert(self, client_data: dict) -> None:
        """Insert client."""
        with DBConnection() as conn:
            # insert the client and return the id
            try:
                client = Client(**client_data)
                conn.session.add(client)
                conn.session.commit()
                return client.id
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def get_client_by(self, field: str, value: str) -> Client:
        """Get client by field."""
        with DBConnection() as conn:
            try:
                query = select(Client).where(getattr(Client, field) == value)
                return conn.session.scalars(query).first()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def get_with_details(self, client_id: int) -> Client:
        """Search for a client by id and return the client with its client_operations and timelines.
        Args:
            client_id (int): The client id.
        """
        with DBConnection() as conn:
            try:
                query = (
                    select(Client)
                    .options(
                        joinedload(Client.client_operations),
                        joinedload(Client.timelines),
                    )
                    .where(Client.id == client_id)
                )

                return conn.session.scalars(query).unique().first()
            except Exception as exe:
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

    async def get_pipeline_clients(
        self,
        page: int,
        per_page: int,
        order_by: str,
        order: str,
        source: list[str],
        is_30_days: bool
    ) -> dict:
        """Get all clients by pipeline status with pagination"""
        pipeline_clients = {}
        columns_30_days = ["CONTACT", "WAITING_FILL", "CONTRACT", "WAITING_PAYMENT", "PENDING_DOCS"]

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
                        .outerjoin(Client.operation)
                        .where(Client.pipeline_status == status)
                        .where(Client.source.in_(source))
                        .limit(per_page)
                        .offset((page - 1) * per_page)
                    )
                    query = query.order_by(
                        getattr(Client, order_by).desc()
                        if order == "DESC"
                        else getattr(Client, order_by).asc()
                    )

                    if is_30_days:
                        if not status in columns_30_days:
                            continue

                        query = query.where(
                            Client.updated_at <= datetime.now() - timedelta(days=30)
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
                all_clients = (
                    select(Client)
                    .where(Client.pipeline_status == PipelineStatus.ENTRY)
                    .where(Client.operation_id == operation_id)
                )
                timelines_query = insert(Timeline).values(
                    [
                        {
                            "client_id": client.id,
                            "pipeline_status": "ENRICHMENT",
                            "source": TimelineSource.SPREADSHEET,
                        }
                        for client in conn.session.execute(all_clients).scalars().all()
                    ]
                )

                conn.session.execute(timelines_query)
                conn.session.execute(query)
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def get_pending_clients(self):
        """Get all clients that don't have any pipeline status associated."""
        with DBConnection() as conn:
            try:
                query = (
                    select(Client)
                    .options(joinedload(Client.client_operations))
                    .where(Client.is_active == True)
                    .where(Client.pipeline_status == None)
                    .where(Client.operation_id == None)
                )
                return conn.session.scalars(query).unique().all()
            except Exception as exe:
                conn.session.rollback()
                print(exe)

    async def deactive_client(self, client_id: int):
        """ "Deactivate client by id, deleting timeliens, task, notes and client_operations."""
        with DBConnection() as conn:
            query = (
                update(Client)
                .where(Client.id == client_id)
                .values(is_active=False, pipeline_status=None)
            )
            timeline_query = delete(Timeline).where(Timeline.client_id == client_id)
            co_query = delete(ClientOperation).where(
                ClientOperation.client_id == client_id
            )
            notifications_query = delete(Notification).where(
                Notification.client_id == client_id
            )
            tasks_query = delete(Task).where(Task.client_id == client_id)
            try:
                conn.session.execute(query)
                conn.session.execute(timeline_query)
                conn.session.execute(co_query)
                conn.session.execute(notifications_query)
                conn.session.execute(tasks_query)
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)
