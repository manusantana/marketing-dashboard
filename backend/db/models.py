from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sales = relationship("Sale", back_populates="batch", cascade="all, delete-orphan")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)          # T.AñoMes
    customer = Column(String, index=True)    # C.Cliente
    product = Column(String)                 # A.Descripcion
    amount = Column(Float)                   # Venta 💰
    margin = Column(Float)                   # Margen %
    quantity = Column(Integer)               # Cantidad
    batch_id = Column(Integer, ForeignKey("batches.id"), index=True)
    batch = relationship("Batch", back_populates="sales")
