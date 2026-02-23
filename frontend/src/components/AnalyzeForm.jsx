import { useState } from 'react';
import { analisarTicker } from '../services/api';

function AnalyzeForm({ onAnalysisComplete }) {
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!ticker.trim()) return;

    setLoading(true);
    setError('');

    try {
      const result = await analisarTicker(ticker.trim().toUpperCase());
      onAnalysisComplete(result);
      setTicker('');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Erro ao analisar ticker. Verifique se a API está rodando.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analyze-form">
      <h2>🔍 Analisar Ação</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            placeholder="Digite o ticker (ex: AAPL, PETR4.SA)"
            disabled={loading}
          />
          <button type="submit" disabled={loading || !ticker.trim()}>
            {loading ? '⏳ Analisando...' : '🚀 Analisar'}
          </button>
        </div>
      </form>
      {loading && (
        <div className="loading-bar">
          <div className="loading-bar-inner"></div>
          <p>Buscando dados e gerando análise com IA... isso pode levar alguns segundos.</p>
        </div>
      )}
      {error && <div className="error-msg">❌ {error}</div>}
    </div>
  );
}

export default AnalyzeForm;
