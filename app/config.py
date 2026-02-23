import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://stockuser:stockpass@localhost:5432/stockdb")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
