/**
 * components/viewer/ExportButtons.js — Boutons d'export DOCX et PDF
 *
 * Déclenche le téléchargement du CDC en Word ou PDF
 * en appelant les endpoints du backend.
 */

import React, { useState } from "react";
import { getDocxUrl, getPdfUrl } from "../../services/api";
import "./ExportButtons.css";

export default function ExportButtons({ sessionId }) {
  const [loadingDocx, setLoadingDocx] = useState(false);
  const [loadingPdf,  setLoadingPdf]  = useState(false);
  const [error,       setError]       = useState(null);

  const handleExport = async (type) => {
    setError(null);
    const setLoading = type === "docx" ? setLoadingDocx : setLoadingPdf;
    const url        = type === "docx" ? getDocxUrl(sessionId) : getPdfUrl(sessionId);

    setLoading(true);
    try {
      // Ouvre l'URL dans un nouvel onglet — le navigateur déclenche le download
      const link = document.createElement("a");
      link.href   = url;
      link.target = "_blank";
      link.rel    = "noopener noreferrer";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      setError("Erreur lors de l'export. Vérifie que le backend est démarré.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="export-buttons">
      <button
        className="btn-export btn-docx"
        onClick={() => handleExport("docx")}
        disabled={loadingDocx}
        title="Télécharger en Word (.docx)"
      >
        {loadingDocx ? "…" : "Word (.docx)"}
      </button>

      <button
        className="btn-export btn-pdf"
        onClick={() => handleExport("pdf")}
        disabled={loadingPdf}
        title="Télécharger en PDF"
      >
        {loadingPdf ? "…" : "PDF"}
      </button>

      {error && <p className="export-error">{error}</p>}
    </div>
  );
}