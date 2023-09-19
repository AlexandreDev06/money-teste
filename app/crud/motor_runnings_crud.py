from sqlalchemy import select, update

from app.configs.database import DBConnection
from app.models import MotorRunning


class MotorRunningsManager:
    """Clients manager class"""

    async def get(self, motor_id: int) -> MotorRunning:
        """Get motor_running from the database."""

        with DBConnection() as conn:
            try:
                query = select(MotorRunning).where(MotorRunning.id == motor_id)
                return conn.session.scalars(query).first()
            except Exception as exe:
                print(exe)

    async def insert(self, data: dict) -> None:
        """Insert motor_running to the database."""

        with DBConnection() as conn:
            try:
                conn.session.add(MotorRunning(**data))
                conn.session.commit()
            except Exception as exe:
                print(exe)
                conn.session.rollback()

    async def update(self, motor_id: int, data: dict) -> None:
        """Update motor_running in the database."""

        with DBConnection() as conn:
            try:
                query = (
                    update(MotorRunning)
                    .where(MotorRunning.id == motor_id)
                    .values(**data)
                )
                conn.session.execute(query)
                conn.session.commit()
            except Exception as exe:
                print(exe)
                conn.session.rollback()

    async def get_by_operation_and_motor_type(
        self, operation_id: int, motor_type: str
    ) -> MotorRunning:
        """Get motor_running from the database."""

        with DBConnection() as conn:
            try:
                return (
                    conn.session.query(MotorRunning)
                    .filter(
                        MotorRunning.operation_id == operation_id,
                        MotorRunning.motor_type == motor_type,
                    )
                    .first()
                )
            except Exception as exe:
                print(exe)
