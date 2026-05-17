/**
 * components/viewer/CDCViewer.js — Affichage structuré du cahier des charges
 *
 * Affiche :
 *   - Les statistiques des exigences (haute/moyenne/basse)
 *   - Le résumé du projet
 *   - La navigation par sections (sidebar)
 *   - Le contenu de chaque section
 *   - Le tableau des exigences
 */

import React, { useState } from "react";
import "./CDCViewer.css";

export default function CDCViewer({ cdc }) {
  const [activeSection, setActiveSection] = useState(0);
  const [showReqs, setShowReqs]           = useState(false);

  if (!cdc) return null;

  const { sections = [], requirements = [], stats = {}, summary, questions = [] } = cdc;

  return (
    <div className="cdc-viewer">

      {/* ── Statistiques ───────────────────────────────────────────── */}
      <div className="cdc-stats">
        <div className="stat-card total">
          <span className="stat-number">{requirements.length}</span>
          <span className="stat-label">Exigences totales</span>
        </div>
        <div className="stat-card haute">
          <span className="stat-number">{stats.haute || 0}</span>
          <span className="stat-label">Priorité haute</span>
        </div>
        <div className="stat-card moyenne">
          <span className="stat-number">{stats.moyenne || 0}</span>
          <span className="stat-label">Priorité moyenne</span>
        </div>
        <div className="stat-card basse">
          <span className="stat-number">{stats.basse || 0}</span>
          <span className="stat-label">Priorité basse</span>
        </div>
      </div>

      {/* ── Résumé ─────────────────────────────────────────────────── */}
      {summary && (
        <div className="cdc-summary">
          <p className="summary-label">Résumé du projet</p>
          <p className="summary-text">{summary}</p>
        </div>
      )}

      {/* ── Corps principal : sidebar + contenu ────────────────────── */}
      <div className="cdc-body">

        {/* Sidebar navigation */}
        <aside className="cdc-sidebar">
          <p className="sidebar-title">Sections</p>
          {sections.map((section, idx) => (
            <button
              key={section.id || idx}
              className={`sidebar-item ${activeSection === idx ? "active" : ""}`}
              onClick={() => setActiveSection(idx)}
            >
              {section.title}
            </button>
          ))}

          <hr className="sidebar-divider" />

          <button
            className={`sidebar-item ${showReqs ? "active" : ""}`}
            onClick={() => setShowReqs(!showReqs)}
          >
            Tableau des exigences ({requirements.length})
          </button>
        </aside>

        {/* Contenu principal */}
        <div className="cdc-content">
          {showReqs ? (
            <RequirementsTable requirements={requirements} />
          ) : (
            <SectionPanel section={sections[activeSection]} />
          )}
        </div>
      </div>

      {/* ── Questions de clarification ─────────────────────────────── */}
      {questions.length > 0 && (
        <div className="cdc-questions">
          <p className="questions-label">Questions de clarification</p>
          <ul className="questions-list">
            {questions.map((q, idx) => (
              <li key={idx}>{q}</li>
            ))}
          </ul>
        </div>
      )}

    </div>
  );
}

// ── Sous-composant : section du CDC ──────────────────────────────────────────

function SectionPanel({ section }) {
  if (!section) return <p className="no-section">Sélectionne une section dans le menu.</p>;
  return (
    <div className="section-panel">
      <h2 className="section-title">{section.title}</h2>
      <div className="section-content">
        {section.content.split("\n").map((line, idx) =>
          line.trim() ? <p key={idx}>{line}</p> : <br key={idx} />
        )}
      </div>
    </div>
  );
}

// ── Sous-composant : tableau des exigences ────────────────────────────────────

function RequirementsTable({ requirements }) {
  const priorityClass = (p) => {
    if (p === "Haute")   return "badge-haute";
    if (p === "Moyenne") return "badge-moyenne";
    return "badge-basse";
  };

  return (
    <div className="req-table-wrap">
      <h2 className="section-title">Tableau des exigences</h2>
      <table className="req-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Description</th>
            <th>Catégorie</th>
            <th>Priorité</th>
            <th>MoSCoW</th>
          </tr>
        </thead>
        <tbody>
          {requirements.map((req, idx) => (
            <tr key={req.id || idx}>
              <td className="req-id">{req.id}</td>
              <td className="req-desc">{req.description}</td>
              <td className="req-cat">{req.category}</td>
              <td>
                <span className={`badge ${priorityClass(req.priority)}`}>
                  {req.priority}
                </span>
              </td>
              <td className="req-moscow">{req.moscow}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}