from sqlalchemy import Column, String, Float, Double, Integer, Date
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
    latest_trading_day = Column(Date)
    previous_close = Column(Float)
    change = Column(Float)
    change_percentage = Column(String)
