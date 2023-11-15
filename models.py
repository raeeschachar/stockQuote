from sqlalchemy import Column, String, DateTime, Float, Double, Integer
from database import Base


class PriceData(Base):
    __tablename__ = 'price_data'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    price = Column(Float)
    volume = Column(Double)
    latest_trading_day = Column(DateTime)
    previous_close = Column(Float)
    change = Column(Float)
    change_percentage = Column(String)
