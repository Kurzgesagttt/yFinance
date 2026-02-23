from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime, timezone
from app.database import Base


class StockAnalysis(Base):
    __tablename__ = "stock_analysis"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(20), index=True, nullable=False)
    current_price = Column(Float, nullable=True)
    recommendation = Column(String(50), nullable=True)
    analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<StockAnalysis(id={self.id}, ticker='{self.ticker}', recommendation='{self.recommendation}')>"
