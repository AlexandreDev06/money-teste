from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.configs.settings import settings


class DBConnection:
    """Class to connect to the database"""

    def __init__(self) -> None:
        self.__connection_uri = settings.db_uri
        self.__engine = self.__create_engine()
        self.session: Session = None

    def __enter__(self) -> "DBConnection":
        self.session = Session(self.__engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()

    def __create_engine(self) -> Engine:
        return create_engine(self.__connection_uri)

    def get_engine(self) -> Engine:
        """Returns the engine object associated with the current instance."""
        return self.__engine
