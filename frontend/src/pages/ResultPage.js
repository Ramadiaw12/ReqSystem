/**
 * pages/ResultPage.js — Affichage du cahier des charges généré
 *
 * Charge le CDC depuis le backend et l'affiche via CDCViewer.
 * Propose les boutons d'export DOCX et PDF.
 */

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getCDC } from "../services/api";
import CDCViewer from "../components/viewer/CDCViewer";
import ExportButtons from "../components/viewer/ExportButtons";
import "./ResultPage.css";

export default function ResultPage() {
  const { sessionId } = useParams();
  const navigate      = useNavigate();

  const [cdc,     setCdc]     = useState(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getCDC(sessionId);
        setCdc(data);
      } catch (err) {
        const status = err.response?.status;
        if (status === 202) {
          setError("Le CDC est encore en cours de génération. Reviens dans quelques secondes.");
        } else {
          setError(err.response?.data?.detail || "Impossible de charger le CDC.");
        }
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [sessionId]);

  if (loading) {
    return (
      <div className="result-page">
        <p className="result-loading">Chargement du cahier des charges…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-page">
        <div className="result-error">
          <p>{error}</p>
          <button onClick={() => navigate("/")} className="btn-new">
            Nouvelle analyse
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="result-page">
      <div className="result-header">
        <div>
          <h2 className="result-title">
            Cahier des charges — {cdc.project_name}
          </h2>
          <p className="result-meta">
            Client : <strong>{cdc.client_name}</strong>
            {cdc.generated_at && (
              <> · Généré le {new Date(cdc.generated_at).toLocaleDateString("fr-FR")}</>
            )}
          </p>
        </div>
        <div className="result-actions">
          <ExportButtons sessionId={sessionId} />
          <button onClick={() => navigate("/")} className="btn-new">
            + Nouvelle analyse
          </button>
        </div>
      </div>

      <CDCViewer cdc={cdc} />
    </div>
  );
}