import yfinance as yf
from typing import Optional


def get_stock_data(ticker: str) -> dict:
    """
    Busca dados atuais de uma ação usando yfinance.
    Retorna dicionário com informações relevantes.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        previous_close = info.get("previousClose")
        market_cap = info.get("marketCap")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        company_name = info.get("shortName") or info.get("longName", ticker)
        currency = info.get("currency", "USD")

        # Dados financeiros
        pe_ratio = info.get("trailingPE")
        forward_pe = info.get("forwardPE")
        dividend_yield = info.get("dividendYield")
        fifty_two_week_high = info.get("fiftyTwoWeekHigh")
        fifty_two_week_low = info.get("fiftyTwoWeekLow")

        return {
            "ticker": ticker.upper(),
            "company_name": company_name,
            "current_price": current_price,
            "previous_close": previous_close,
            "market_cap": market_cap,
            "sector": sector,
            "industry": industry,
            "currency": currency,
            "pe_ratio": pe_ratio,
            "forward_pe": forward_pe,
            "dividend_yield": dividend_yield,
            "fifty_two_week_high": fifty_two_week_high,
            "fifty_two_week_low": fifty_two_week_low,
            "success": True,
        }

    except Exception as e:
        return {
            "ticker": ticker.upper(),
            "error": str(e),
            "success": False,
        }
