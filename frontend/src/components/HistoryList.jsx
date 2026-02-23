import { useState, useEffect } from 'react';
import { getHistorico } from '../services/api';
import AnalysisCard from './AnalysisCard';

function HistoryList({ refreshTrigger }) {
  const [history, setHistory] = useState({ total: 0, analyses: [] });
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const limit = 10;

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const data = await getHistorico(page * limit, limit);
      setHistory(data);
    } catch (err) {
      console.error('Erro ao buscar histórico:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [page, refreshTrigger]);

  const totalPages = Math.ceil(history.total / limit);

  return (
    <div className="history-section">
      <h2>📜 Histórico de Análises ({history.total} total)</h2>

      {loading && <p className="loading-text">Carregando...</p>}

      {!loading && history.analyses.length === 0 && (
        <p className="empty-text">Nenhuma análise encontrada. Faça sua primeira análise acima!</p>
      )}

      <div className="cards-grid">
        {history.analyses.map((item) => (
          <AnalysisCard key={item.id} analysis={item} />
        ))}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button onClick={() => setPage((p) => Math.max(0, p - 1))} disabled={page === 0}>
            ◀ Anterior
          </button>
          <span>
            Página {page + 1} de {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
          >
            Próxima ▶
          </button>
        </div>
      )}
    </div>
  );
}

export default HistoryList;
