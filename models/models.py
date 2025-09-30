from sqlalchemy import Column, Integer, String
from database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String,nullable=False)
    phone = Column(String,nullable=False)