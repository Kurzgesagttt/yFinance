from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StockAnalysisRequest(BaseModel):
    """Schema para requisição de análise."""
    ticker: str


class StockAnalysisResponse(BaseModel):
    """Schema para resposta de análise."""
    id: int
    ticker: str
    current_price: Optional[float] = None
    recommendation: Optional[str] = None
    analysis: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StockAnalysisListResponse(BaseModel):
    """Schema para listagem de análises."""
    total: int
    analyses: list[StockAnalysisResponse]
