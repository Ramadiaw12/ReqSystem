/**
 * services/api.js — Client HTTP centralisé pour SystemReq
 *
 * Toutes les requêtes vers le backend passent par ce fichier.
 * Avantages :
 *   - L'URL de base est définie en un seul endroit (.env)
 *   - Gestion des erreurs centralisée
 *   - Facile à mocker pour les tests
 */

import axios from "axios";

// URL du backend — définie dans frontend/.env
// REACT_APP_API_URL=http://localhost:8000
const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 60000, // 60s — le pipeline LLM peut prendre du temps
});

// ── Intercepteur : log les erreurs en développement ──────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      "[API] Erreur :",
      error.response?.status,
      error.response?.data?.detail || error.message
    );
    return Promise.reject(error);
  }
);

// ── Sessions ──────────────────────────────────────────────────────────────────

/**
 * Crée une nouvelle session depuis les données du formulaire.
 * @param {Object} formData - données du formulaire ClientForm
 * @returns {Promise<Object>} session créée { id, status, client_name, ... }
 */
export const createSession = async (formData) => {
  const res = await api.post("/api/sessions/", formData);
  return res.data;
};

/**
 * Récupère l'état actuel d'une session (utilisé pour le polling).
 * @param {string} sessionId
 * @returns {Promise<Object>} { id, status, client_name, ... }
 */
export const getSession = async (sessionId) => {
  const res = await api.get(`/api/sessions/${sessionId}`);
  return res.data;
};

/**
 * Liste toutes les sessions existantes.
 * @returns {Promise<Array>}
 */
export const listSessions = async () => {
  const res = await api.get("/api/sessions/");
  return res.data;
};

// ── Pipeline CDC ──────────────────────────────────────────────────────────────

/**
 * Lance le pipeline 3 agents pour une session.
 * Le backend traite en arrière-plan — on suit via polling sur getSession.
 * @param {string} sessionId
 * @returns {Promise<Object>} { message, session_id }
 */
export const runPipeline = async (sessionId) => {
  const res = await api.post(`/api/cdc/${sessionId}/run`);
  return res.data;
};

/**
 * Récupère le CDC généré une fois le statut "done".
 * @param {string} sessionId
 * @returns {Promise<Object>} CDC complet avec sections, requirements, metadata
 */
export const getCDC = async (sessionId) => {
  const res = await api.get(`/api/cdc/${sessionId}`);
  return res.data;
};

// ── Export documents ──────────────────────────────────────────────────────────

/**
 * Retourne l'URL de téléchargement du CDC en Word.
 * Ouvrir dans une nouvelle fenêtre déclenche le download.
 */
export const getDocxUrl = (sessionId) =>
  `${BASE_URL}/api/cdc/${sessionId}/export/docx`;

/**
 * Retourne l'URL de téléchargement du CDC en PDF.
 */
export const getPdfUrl = (sessionId) =>
  `${BASE_URL}/api/cdc/${sessionId}/export/pdf`;