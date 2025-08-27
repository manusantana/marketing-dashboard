from sqlalchemy import Column, Integer, String, Date, Float
from db.session import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)          # T.AñoMes
    customer = Column(String, index=True)    # C.Cliente
    product = Column(String)                 # A.Descripcion
    amount = Column(Float)                   # Venta 💰
    margin = Column(Float)                   # Margen %
    quantity = Column(Integer)               # Cantidad
