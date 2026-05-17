/**
 * pages/SessionPage.js — Suivi du pipeline multi-agents en temps réel
 *
 * Cette page est affichée pendant que les 3 agents travaillent.
 * Elle poll le backend toutes les 2 secondes pour connaître le statut,
 * et redirige automatiquement vers ResultPage quand c'est "done".
 */

import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getSession } from "../services/api";
import "./SessionPage.css";

const STEPS = [
  { key: "collecting",  label: "Collecte des besoins",    desc: "L'agent analyse le formulaire et extrait vos besoins" },
  { key: "analyzing",   label: "Analyse & priorisation",  desc: "Les besoins sont classifiés et hiérarchisés (MoSCoW)" },
  { key: "generating",  label: "Génération du CDC",       desc: "Rédaction du cahier des charges en 10 sections" },
  { key: "done",        label: "CDC prêt",                desc: "Votre cahier des charges est généré avec succès" },
];

const STATUS_TO_STEP = {
  created:    -1,
  collecting:  0,
  analyzing:   1,
  generating:  2,
  done:        3,
  error:      -2,
};

export default function SessionPage() {
  const { sessionId } = useParams();
  const navigate      = useNavigate();

  const [session,  setSession]  = useState(null);
  const [error,    setError]    = useState(null);

  const currentStep = STATUS_TO_STEP[session?.status] ?? -1;

  const poll = useCallback(async () => {
    try {
      const s = await getSession(sessionId);
      setSession(s);

      if (s.status === "done") {
        // Attendre un instant pour que l'animation "done" soit visible
        setTimeout(() => navigate(`/result/${sessionId}`), 1200);
      }

      if (s.status === "error") {
        setError(s.error || "Une erreur s'est produite pendant l'analyse.");
      }
    } catch (err) {
      setError("Impossible de joindre le backend. Vérifie que le serveur est démarré.");
    }
  }, [sessionId, navigate]);

  useEffect(() => {
    // Premier appel immédiat
    poll();

    // Polling toutes les 2 secondes
    const interval = setInterval(poll, 2000);
    return () => clearInterval(interval);
  }, [poll]);

  return (
    <div className="session-page">
      <div className="session-header">
        <h2>Analyse en cours…</h2>
        {session && (
          <p className="session-client">
            Client : <strong>{session.client_name}</strong>
          </p>
        )}
      </div>

      {error ? (
        <div className="session-error">
          <p>{error}</p>
          <button onClick={() => navigate("/")} className="btn-back">
            Recommencer
          </button>
        </div>
      ) : (
        <div className="steps-container">
          {STEPS.map((step, idx) => {
            const isDone   = currentStep > idx;
            const isActive = currentStep === idx;
            const isPending = currentStep < idx;

            return (
              <div
                key={step.key}
                className={`step-item ${isDone ? "done" : ""} ${isActive ? "active" : ""} ${isPending ? "pending" : ""}`}
              >
                <div className="step-icon-wrap">
                  <div className="step-icon">
                    {isDone ? "✓" : idx + 1}
                  </div>
                  {idx < STEPS.length - 1 && (
                    <div className={`step-line ${isDone ? "done" : ""}`} />
                  )}
                </div>
                <div className="step-content">
                  <p className="step-label">{step.label}</p>
                  <p className="step-desc">{step.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {!error && session?.status !== "done" && (
        <p className="session-hint">
          Les agents IA analysent vos besoins, cela prend environ 30 à 60 secondes…
        </p>
      )}
    </div>
  );
}