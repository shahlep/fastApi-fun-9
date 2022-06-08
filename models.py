import datetime

from database import Base
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    items = relationship("Items", back_populates="owner")


class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    title = Column(String, unique=True, nullable=False)
    date_posted = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
