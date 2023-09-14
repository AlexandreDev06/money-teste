from app.configs.database import DBConnection
from app.models import MotorRunning


class MotorRunningsManager:
    """Clients manager class"""

    async def get(self, id: int) -> MotorRunning:
        """Get motor_running from the database."""

        with DBConnection() as conn:
            try:
                return (
                    conn.session.query(MotorRunning)
                    .filter(MotorRunning.id == id)
                    .first()
                )
            except Exception as e:
                print(e)
                conn.session.rollback()

    async def insert(self, data: dict) -> None:
        """Insert motor_running to the database."""

        with DBConnection() as conn:
            try:
                conn.session.add(MotorRunning(**data))
                conn.session.commit()
            except Exception as e:
                print(e)
                conn.session.rollback()

    async def update(self, data: dict) -> MotorRunning:
        """Update motor_running in the database."""

        with DBConnection() as conn:
            try:
                model = conn.session.query(MotorRunning).filter(
                    MotorRunning.id == data["id"]
                )
                model.update(data)
                conn.session.commit()
                return model
            except Exception as e:
                print(e)
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
            except Exception as e:
                print(e)
