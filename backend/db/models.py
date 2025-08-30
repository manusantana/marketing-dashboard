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
    date = Column(Date, index=True, nullable=True)
    customer = Column(String, index=True, nullable=True)
    product = Column(String, index=True, nullable=True)
    amount = Column(Float, nullable=False, default=0.0)
    margin = Column(Float, nullable=False, default=0.0)
    quantity = Column(Integer, nullable=False, default=0)
    batch_id = Column(String(36), index=True, nullable=False)  # <-- NUEVO

# Índice útil para consultas y (si quieres) unicidad lógica
Index("ix_sales_date_customer_product", Sale.date, Sale.customer, Sale.product)

class UploadHistory(Base):
    __tablename__ = "upload_history"
    id = Column(Integer, primary_key=True)
    batch_id = Column(String(36), unique=True, nullable=False, index=True)
    filename = Column(String, nullable=False)
    mode = Column(Enum("append", "replace", name="upload_mode"), nullable=False)
    rows = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    date = Column(Date, index=True)          # T.AñoMes
    customer = Column(String, index=True)    # C.Cliente
    product = Column(String)                 # A.Descripcion
    amount = Column(Float)                   # Venta 💰
    margin = Column(Float)                   # Margen %
    quantity = Column(Integer)               # Cantidad
    batch_id = Column(Integer, ForeignKey("batches.id"), index=True)
    batch = relationship("Batch", back_populates="sales")
