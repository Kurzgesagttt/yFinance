# Stock AI Analyzer

Aplicação fullstack para análise de ações com inteligência artificial. O backend busca dados de ações em tempo real usando **yfinance**, envia para a **OpenAI (GPT-4o-mini)** gerar uma análise com recomendação (COMPRAR, MANTER ou VENDER) e salva tudo em um banco **PostgreSQL**. O frontend em **React** permite pesquisar ações e visualizar o histórico de análises.

---

## Tecnologias

| Camada   | Stack                                      |
| -------- | ------------------------------------------ |
| Backend  | FastAPI, SQLAlchemy, Alembic, yfinance      |
| IA       | OpenAI API (GPT-4o-mini)                   |
| Banco    | PostgreSQL 15                               |
| Frontend | React, Vite, Axios                          |
| Infra    | Docker, Docker Compose, Nginx               |

---

## Endpoints da API

A API roda na porta `8000` e todos os endpoints de negócio ficam sob o prefixo `/api/v1`.

### `GET /`

**Health check** — Retorna o status da API.

```json
{
  "status": "online",
  "message": "Stock AI Analyzer API está rodando!",
  "docs": "/docs"
}
```

---

### `GET /health`

Verifica se a API **e o banco de dados** estão funcionando.

```json
{
  "api": "ok",
  "database": "connected"
}
```

---

### `GET /api/v1/analisar/{ticker}`

Realiza a análise completa de uma ação. Esse é o endpoint principal da aplicação.

**O que ele faz, passo a passo:**

1. Recebe o código da ação (ex: `AAPL`, `PETR4.SA`)
2. Busca dados atuais da ação via **yfinance** (preço, P/E, setor, etc.)
3. Envia esses dados para a **OpenAI**, que gera uma recomendação (COMPRAR / MANTER / VENDER) e uma análise detalhada
4. Salva a análise no **PostgreSQL**
5. Retorna o resultado completo

**Exemplo de chamada:**

```
GET /api/v1/analisar/AAPL
```

**Resposta:**

```json
{
  "id": 1,
  "ticker": "AAPL",
  "current_price": 178.50,
  "recommendation": "COMPRAR",
  "analysis": "A Apple apresenta fundamentos sólidos com P/E de 28.5...",
  "created_at": "2026-02-22T15:30:00"
}
```

> ⚠️ Esse endpoint pode levar alguns segundos, pois depende da resposta da OpenAI.

---

### `GET /api/v1/historico`

Retorna o **histórico de todas as análises** já realizadas, com paginação.

| Parâmetro | Tipo | Padrão | Descrição                  |
| --------- | ---- | ------ | -------------------------- |
| `skip`    | int  | 0      | Quantos registros pular    |
| `limit`   | int  | 20     | Quantidade por página (máx 100) |

**Exemplo:**

```
GET /api/v1/historico?skip=0&limit=10
```

**Resposta:**

```json
{
  "total": 25,
  "analyses": [
    {
      "id": 1,
      "ticker": "AAPL",
      "current_price": 178.50,
      "recommendation": "COMPRAR",
      "analysis": "...",
      "created_at": "2026-02-22T15:30:00"
    }
  ]
}
```

---

### `GET /api/v1/historico/{ticker}`

Retorna o histórico de análises de **uma ação específica**.

| Parâmetro | Tipo | Padrão | Descrição                  |
| --------- | ---- | ------ | -------------------------- |
| `limit`   | int  | 10     | Quantidade de registros (máx 100) |

**Exemplo:**

```
GET /api/v1/historico/AAPL?limit=5
```

Retorna as últimas 5 análises feitas para a ação AAPL.

---

### `GET /api/v1/analise/{analysis_id}`

Busca **uma análise específica** pelo seu ID.

**Exemplo:**

```
GET /api/v1/analise/1
```

Retorna a análise com `id = 1`. Se não existir, retorna `404`.

---

### Documentação interativa

Com a API rodando, acesse:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Como rodar o projeto localmente

### Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados
- Uma chave de API da [OpenAI](https://platform.openai.com/api-keys)

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/stock-ai-analyzer.git
cd stock-ai-analyzer
```

### 2. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com sua chave da OpenAI:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
DATABASE_URL=postgresql+psycopg2://stockuser:stockpass@localhost:5432/stockdb
OPENAI_API_KEY=sua_chave_da_openai_aqui
```

### 3. Suba os containers com Docker Compose

```bash
docker compose up --build
```

Isso vai subir três serviços:

| Serviço    | Porta | Descrição                      |
| ---------- | ----- | ------------------------------ |
| `db`       | 5432  | Banco de dados PostgreSQL      |
| `api`      | 8000  | Backend FastAPI                |
| `frontend` | 3000  | Frontend React (via Nginx)     |

### 4. Acesse a aplicação

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **API:** [http://localhost:8000](http://localhost:8000)
- **Documentação da API:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Rodando sem Docker (desenvolvimento)

Se preferir rodar sem Docker, você vai precisar de **Python 3.11+**, **Node.js 18+** e um **PostgreSQL** rodando localmente.

#### Backend

```bash
# Crie e ative um ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure o .env (veja passo 2 acima)

# Rode a API
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

#### Frontend

```bash
cd frontend

# Instale as dependências
npm install

# Rode o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em `http://localhost:5173`.

---

## Estrutura do projeto

```
├── app/                    # Backend (FastAPI)
│   ├── main.py             # Ponto de entrada da API
│   ├── config.py           # Variáveis de ambiente
│   ├── database.py         # Conexão com PostgreSQL
│   ├── models/             # Modelos SQLAlchemy
│   ├── schemas/            # Schemas Pydantic (request/response)
│   ├── routes/             # Rotas/endpoints
│   ├── services/           # Lógica de negócio (yfinance, OpenAI)
│   └── repositories/       # Acesso ao banco de dados
├── frontend/               # Frontend (React + Vite)
│   └── src/
│       ├── components/     # Componentes React
│       └── services/       # Chamadas à API
├── alembic/                # Migrações do banco
├── docker-compose.yml      # Orquestração dos containers
├── Dockerfile              # Build do backend
├── requirements.txt        # Dependências Python
└── .env.example            # Modelo de variáveis de ambiente
```
