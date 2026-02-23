import axios from 'axios';

// Em produção (Docker/Nginx) usa URL relativa via proxy
// Em dev local (vite dev server) o proxy está configurado no vite.config.js
const API_BASE = '/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2 min (a IA pode demorar)
});

export const analisarTicker = async (ticker) => {
  const response = await api.get(`/analisar/${ticker}`);
  return response.data;
};

export const getHistorico = async (skip = 0, limit = 20) => {
  const response = await api.get(`/historico`, { params: { skip, limit } });
  return response.data;
};

export const getHistoricoPorTicker = async (ticker, limit = 10) => {
  const response = await api.get(`/historico/${ticker}`, { params: { limit } });
  return response.data;
};

export const getAnalisePorId = async (id) => {
  const response = await api.get(`/analise/${id}`);
  return response.data;
};

export default api;
