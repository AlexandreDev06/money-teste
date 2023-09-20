from sqlalchemy import select, text, update

from app.configs.database import DBConnection
from app.models.timelines import Timeline


class TimelineManager:
    """ Timeline manager class """

    async def insert(self, data_timeline: dict):
        """Insert a timeline in the database."""
        with DBConnection() as conn:
            try:
                conn.session.add(Timeline(**data_timeline))
                conn.session.commit()
            except Exception as exe:
                conn.session.rollback()
                print(exe)