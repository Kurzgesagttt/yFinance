from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.stock_routes import router as stock_router

# Criar tabelas automaticamente (dev mode)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock AI Analyzer API",
    description="API de análise de ações com inteligência artificial (OpenAI) e persistência em PostgreSQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS - permitir frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(stock_router)


@app.get("/", tags=["Health"])
def root():
    """Health check da API."""
    return {
        "status": "online",
        "message": "Stock AI Analyzer API está rodando!",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    """Verifica se a API e o banco estão funcionando."""
    try:
        from sqlalchemy import text
        from app.database import SessionLocal

        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "api": "ok",
        "database": db_status,
    }
