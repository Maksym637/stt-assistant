from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.db_session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    auth0_id = Column(String, unique=True, index=True)
    email = Column(String)

    records = relationship("Record", back_populates="user")
