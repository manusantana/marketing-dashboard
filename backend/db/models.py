from sqlalchemy import Column, Integer, String, Float, Date
from .session import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    customer = Column(String, index=True)
    date = Column(Date)
    revenue = Column(Float)
    cost = Column(Float)