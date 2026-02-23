from sqlalchemy.orm import Session
from app.models.stock_analysis import StockAnalysis
from typing import Optional


def save_analysis(db: Session, data: dict) -> StockAnalysis:
    """Salva uma análise no banco de dados."""
    analysis = StockAnalysis(**data)
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_analyses_by_ticker(db: Session, ticker: str, limit: int = 10) -> list[StockAnalysis]:
    """Busca análises por ticker, ordenadas da mais recente para a mais antiga."""
    return (
        db.query(StockAnalysis)
        .filter(StockAnalysis.ticker == ticker.upper())
        .order_by(StockAnalysis.created_at.desc())
        .limit(limit)
        .all()
    )


def get_all_analyses(db: Session, skip: int = 0, limit: int = 20) -> list[StockAnalysis]:
    """Busca todas as análises com paginação."""
    return (
        db.query(StockAnalysis)
        .order_by(StockAnalysis.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_analyses(db: Session) -> int:
    """Conta total de análises."""
    return db.query(StockAnalysis).count()


def get_analysis_by_id(db: Session, analysis_id: int) -> Optional[StockAnalysis]:
    """Busca análise por ID."""
    return db.query(StockAnalysis).filter(StockAnalysis.id == analysis_id).first()
