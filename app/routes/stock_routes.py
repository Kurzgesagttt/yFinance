from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.stock_service import get_stock_data
from app.services.ai_service import generate_analysis
from app.repositories.stock_repository import (
    save_analysis,
    get_analyses_by_ticker,
    get_all_analyses,
    count_analyses,
    get_analysis_by_id,
)
from app.schemas.stock_schema import StockAnalysisResponse, StockAnalysisListResponse

router = APIRouter(prefix="/api/v1", tags=["Análise de Ações"])


@router.get("/analisar/{ticker}", response_model=StockAnalysisResponse)
def analisar(ticker: str, db: Session = Depends(get_db)):
    """
    Analisa uma ação:
    1. Busca dados atuais via yfinance
    2. Envia para a OpenAI gerar análise
    3. Salva no PostgreSQL
    4. Retorna resultado
    """
    ticker = ticker.upper().strip()

    # 1. Buscar dados da ação
    stock_data = get_stock_data(ticker)
    if not stock_data.get("success"):
        raise HTTPException(
            status_code=404,
            detail=f"Não foi possível buscar dados para o ticker '{ticker}'. Erro: {stock_data.get('error', 'desconhecido')}",
        )

    # 2. Gerar análise com IA
    ai_result = generate_analysis(stock_data)

    # 3. Montar dados para salvar
    db_data = {
        "ticker": ticker,
        "current_price": stock_data.get("current_price"),
        "recommendation": ai_result.get("recommendation"),
        "analysis": ai_result.get("analysis"),
    }

    # 4. Salvar no banco
    saved = save_analysis(db, db_data)

    return saved


@router.get("/historico", response_model=StockAnalysisListResponse)
def historico(
    skip: int = Query(0, ge=0, description="Registros para pular"),
    limit: int = Query(20, ge=1, le=100, description="Quantidade por página"),
    db: Session = Depends(get_db),
):
    """Retorna histórico de todas as análises com paginação."""
    total = count_analyses(db)
    analyses = get_all_analyses(db, skip=skip, limit=limit)
    return StockAnalysisListResponse(total=total, analyses=analyses)


@router.get("/historico/{ticker}", response_model=list[StockAnalysisResponse])
def historico_por_ticker(
    ticker: str,
    limit: int = Query(10, ge=1, le=100, description="Quantidade de registros"),
    db: Session = Depends(get_db),
):
    """Retorna histórico de análises de um ticker específico."""
    ticker = ticker.upper().strip()
    analyses = get_analyses_by_ticker(db, ticker=ticker, limit=limit)
    if not analyses:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhuma análise encontrada para '{ticker}'.",
        )
    return analyses


@router.get("/analise/{analysis_id}", response_model=StockAnalysisResponse)
def buscar_analise(analysis_id: int, db: Session = Depends(get_db)):
    """Busca uma análise específica por ID."""
    analysis = get_analysis_by_id(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Análise não encontrada.")
    return analysis
