from openai import OpenAI
from app.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def generate_analysis(stock_data: dict) -> dict:
    """
    Envia dados da ação para a OpenAI e retorna análise com recomendação.
    """
    prompt = f"""
Você é um analista financeiro especialista. Analise os seguintes dados de uma ação e forneça:

1. Uma recomendação clara: COMPRAR, MANTER ou VENDER
2. Uma análise detalhada justificando sua recomendação

Dados da ação:
- Ticker: {stock_data.get('ticker')}
- Empresa: {stock_data.get('company_name')}
- Preço Atual: {stock_data.get('current_price')} {stock_data.get('currency')}
- Fechamento Anterior: {stock_data.get('previous_close')}
- Market Cap: {stock_data.get('market_cap')}
- Setor: {stock_data.get('sector')}
- Indústria: {stock_data.get('industry')}
- P/E Ratio: {stock_data.get('pe_ratio')}
- Forward P/E: {stock_data.get('forward_pe')}
- Dividend Yield: {stock_data.get('dividend_yield')}
- Máxima 52 semanas: {stock_data.get('fifty_two_week_high')}
- Mínima 52 semanas: {stock_data.get('fifty_two_week_low')}

Responda em formato estruturado:
RECOMENDAÇÃO: [COMPRAR/MANTER/VENDER]
ANÁLISE: [sua análise detalhada aqui]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um analista financeiro especialista."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        response_text = response.choices[0].message.content.strip()

        # Extrair recomendação do texto
        recommendation = "MANTER"  # default
        for keyword in ["COMPRAR", "VENDER", "MANTER"]:
            if keyword in response_text.upper():
                recommendation = keyword
                break

        return {
            "recommendation": recommendation,
            "analysis": response_text,
            "success": True,
        }

    except Exception as e:
        return {
            "recommendation": "ERRO",
            "analysis": f"Erro ao gerar análise: {str(e)}",
            "success": False,
        }
