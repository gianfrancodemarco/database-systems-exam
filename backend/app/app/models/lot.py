from typing import TYPE_CHECKING

from app.db.base_class import Base
from app.db.custom_types import utcnow
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.oracle import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

if TYPE_CHECKING:
    from .lot import Lot  # noqa: F401

class Lot(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    timestamp_arrival = Column(TIMESTAMP, server_default=utcnow())
    weight = Column(Float, server_default="1") 
    volume = Column(Float, server_default="1")
    ripens_level = Column(Float, server_default="0.5")
    price = Column(Float, server_default="1")
    on_display = Column(Boolean, server_default=expression.false())
    expired = Column(Boolean, server_default=expression.false())

    fruit_id = Column(Integer, ForeignKey("FRUIT.id"))
    fruit = relationship("Fruit", back_populates="lots")
