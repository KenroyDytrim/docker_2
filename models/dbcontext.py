from sqlalchemy import Column, String, Integer, Identity, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from enum import Enum

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    hashed_password = Column(String)

class Tags(Enum):
    users = "users"
    companies = "companies"