import pytest

from app.configs.database import DBConnection


@pytest.mark.skip(reason="Sensive test")
def test_db_connection():
    """Test the database connection"""
    db_connection = DBConnection()
    engine = db_connection.get_engine()
    assert engine is not None
