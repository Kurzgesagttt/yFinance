function AnalysisCard({ analysis }) {
  if (!analysis) return null;

  const recClass =
    analysis.recommendation === 'COMPRAR'
      ? 'rec-buy'
      : analysis.recommendation === 'VENDER'
      ? 'rec-sell'
      : 'rec-hold';

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleString('pt-BR');
  };

  return (
    <div className="analysis-card">
      <div className="card-header">
        <div>
          <h3>{analysis.ticker}</h3>
          <span className="card-date">{formatDate(analysis.created_at)}</span>
        </div>
        <div className="card-price">
          {analysis.current_price != null
            ? `R$ ${analysis.current_price.toFixed(2)}`
            : 'N/A'}
        </div>
      </div>

      <div className={`recommendation ${recClass}`}>
        {analysis.recommendation || 'N/A'}
      </div>

      <div className="analysis-text">
        <h4>📊 Análise</h4>
        <pre>{analysis.analysis}</pre>
      </div>

      <div className="card-footer">
        <span className="card-id">ID: #{analysis.id}</span>
      </div>
    </div>
  );
}

export default AnalysisCard;
