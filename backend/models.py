from sqlalchemy import (
    Column,
    String,
    JSON
)

from database import Base


class CachedData(Base):
    __tablename__ = "cached_data"

    file_id = Column(String, primary_key=True, index=True)
    data = Column(JSON, nullable=False)
