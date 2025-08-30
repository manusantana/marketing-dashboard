from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


class Batch(Base):
    """Batch grouping for uploaded sales."""

    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sales = relationship("Sale", back_populates="batch", cascade="all, delete-orphan")


class Sale(Base):
    """Individual sale record."""

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    customer = Column(String, index=True)
    product = Column(String)
    amount = Column(Float)
    margin = Column(Float)
    quantity = Column(Integer)
    batch_id = Column(Integer, ForeignKey("batches.id"), index=True)
    batch = relationship("Batch", back_populates="sales")
