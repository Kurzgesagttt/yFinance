import { useState } from 'react';
import AnalyzeForm from './components/AnalyzeForm';
import AnalysisCard from './components/AnalysisCard';
import HistoryList from './components/HistoryList';
import './App.css';

function App() {
  const [lastAnalysis, setLastAnalysis] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleAnalysisComplete = (result) => {
    setLastAnalysis(result);
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📈 Stock AI Analyzer</h1>
        <p>Análise de ações com inteligência artificial</p>
      </header>

      <main className="app-main">
        <AnalyzeForm onAnalysisComplete={handleAnalysisComplete} />

        {lastAnalysis && (
          <div className="last-analysis">
            <h2>✅ Última Análise</h2>
            <AnalysisCard analysis={lastAnalysis} />
          </div>
        )}

        <hr className="divider" />

        <HistoryList refreshTrigger={refreshTrigger} />
      </main>

      <footer className="app-footer">
        <p>Stock AI Analyzer — FastAPI + PostgreSQL + OpenAI + React</p>
      </footer>
    </div>
  );
}

export default App;
