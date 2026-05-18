/**
 * pages/LandingPage.js — Page d'accueil SystemReq
 * Thème nuit · bleu brillant · sans section tarifs
 */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";

const FEATURES = [
  {
    icon: "🧠",
    title: "Agent Collecte",
    desc: "Extrait et structure automatiquement les besoins depuis le formulaire client EPS SARL.",
  },
  {
    icon: "📊",
    title: "Agent Analyse",
    desc: "Classifie chaque exigence selon la méthode MoSCoW et détecte les conflits.",
  },
  {
    icon: "📄",
    title: "Agent Génération",
    desc: "Rédige un CDC de 10 sections en français professionnel, prêt à signer.",
  },
  {
    icon: "⬇️",
    title: "Export Word & PDF",
    desc: "Téléchargez votre CDC mis en page en un clic — Word ou PDF.",
  },
  {
    icon: "⚡",
    title: "60 secondes",
    desc: "Du formulaire au CDC complet en moins d'une minute grâce au pipeline parallèle.",
  },
  {
    icon: "🔗",
    title: "API REST",
    desc: "Intégrez SystemReq dans votre propre outil via l'API FastAPI documentée.",
  },
];

const PIPELINE = [
  { n: "1", name: "Formulaire",  desc: "Le client remplit le formulaire EPS SARL" },
  { n: "2", name: "Collecte",    desc: "Extraction et structuration des besoins" },
  { n: "3", name: "Analyse",     desc: "Classification MoSCoW et priorisation" },
  { n: "4", name: "Génération",  desc: "Rédaction du CDC en 10 sections" },
  { n: "5", name: "Export",      desc: "Téléchargement Word & PDF" },
];

export default function LandingPage() {
  const navigate  = useNavigate();
  const [step, setStep] = useState(0);

  const runDemo = () => {
    if (step > 0) return;
    setStep(1);
    setTimeout(() => setStep(2), 1200);
    setTimeout(() => setStep(3), 2500);
  };

  return (
    <div className="landing">

      {/* ── BACKGROUND ─────────────────────────────────────────── */}
      <div className="bg-layer">
        <div className="grid-bg" />
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
      </div>

      {/* ── HERO ────────────────────────────────────────────────── */}
      <section className="l-hero">
        <div className="badge-pill anim-fade-up">
          <span className="badge-dot" />
          Propulsé par GPT-4o · Système multi-agents
        </div>

        <h1 className="l-hero-title anim-fade-up anim-delay-1">
          Vos cahiers des charges<br />
          <span className="gradient-text">générés en 60 secondes</span>
        </h1>

        <p className="l-hero-sub anim-fade-up anim-delay-2">
          3 agents IA analysent votre formulaire, classifient les besoins
          et rédigent un CDC professionnel complet — prêt à être signé.
        </p>

        <div className="l-hero-actions anim-fade-up anim-delay-3">
          <button className="btn btn-primary btn-lg" onClick={() => navigate("/new")}>
            Générer mon premier CDC ↗
          </button>
          <button className="btn btn-ghost btn-lg" onClick={() => navigate("/new")}>
            Voir la démo
          </button>
        </div>

        {/* ── DEMO WINDOW ───────────────────────────────────────── */}
        <div className="demo-wrap anim-fade-up anim-delay-4">
          <div className="demo-window">
            <div className="demo-bar">
              <span className="dot dot-r" />
              <span className="dot dot-y" />
              <span className="dot dot-g" />
              <div className="demo-url">localhost:3000 · SystemReq</div>
            </div>

            <div className="demo-body">
              <div className="demo-grid">
                {[["Nom & Prénom","Jean Marc Martin"],["Budget","15 000 €"],
                  ["Email","jean@startup.ma"],["Pays","Maroc"]].map(([l,v]) => (
                  <div className="demo-field" key={l}>
                    <span className="demo-label">{l}</span>
                    <span className="demo-val">{v}</span>
                  </div>
                ))}
              </div>

              <div className="demo-chips">
                {["Site Vitrine","SEO","Maintenance"].map(s => (
                  <span className="demo-chip active" key={s}>{s}</span>
                ))}
                {["E-commerce","App Mobile"].map(s => (
                  <span className="demo-chip" key={s}>{s}</span>
                ))}
              </div>

              <button
                className={`demo-submit ${step > 0 ? "running" : ""} ${step === 3 ? "done" : ""}`}
                onClick={runDemo}
                disabled={step > 0}
              >
                {step === 0 && "Générer le cahier des charges"}
                {step === 1 && "Collecte des besoins…"}
                {step === 2 && "Analyse et génération…"}
                {step === 3 && "✓  CDC généré avec succès !"}
              </button>

              {step > 0 && (
                <div className="demo-steps">
                  <div className={`demo-step ${step >= 1 ? "active" : ""} ${step >= 2 ? "done" : ""}`}>
                    <span className="demo-step-dot" />
                    Agent Collecte — extraction des besoins…
                  </div>
                  <div className={`demo-step ${step >= 2 ? "active" : ""} ${step >= 3 ? "done" : ""}`}>
                    <span className="demo-step-dot" />
                    Agent Analyse — classification MoSCoW…
                  </div>
                  <div className={`demo-step ${step >= 3 ? "done" : ""}`}>
                    <span className="demo-step-dot" />
                    CDC généré — 10 sections · 12 exigences
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS ───────────────────────────────────────────────── */}
      <div className="glow-line" />
      <div className="l-stats">
        {[["60s","Génération moyenne"],["10","Sections rédigées"],["3","Agents IA en pipeline"]].map(([n,l]) => (
          <div className="l-stat" key={l}>
            <div className="l-stat-num gradient-text">{n}</div>
            <div className="l-stat-label">{l}</div>
          </div>
        ))}
      </div>
      <div className="glow-line" />

      {/* ── FEATURES ────────────────────────────────────────────── */}
      <section className="l-features" id="features">
        <div className="l-section-header">
          <div className="section-eyebrow">Fonctionnalités</div>
          <h2 className="section-heading">Tout ce dont vous avez besoin</h2>
          <p className="section-sub">
            Un pipeline complet de l'analyse client à la livraison du document final.
          </p>
        </div>
        <div className="l-features-grid">
          {FEATURES.map((f) => (
            <div className="l-feat-card card" key={f.title}>
              <div className="l-feat-icon">{f.icon}</div>
              <h3 className="l-feat-title">{f.title}</h3>
              <p className="l-feat-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── PIPELINE ────────────────────────────────────────────── */}
      <section className="l-pipeline" id="pipeline">
        <div className="l-section-header">
          <div className="section-eyebrow">Architecture</div>
          <h2 className="section-heading">Pipeline multi-agents</h2>
          <p className="section-sub">
            Chaque agent est spécialisé et communique avec le suivant via l'orchestrateur.
          </p>
        </div>
        <div className="l-pipe-steps">
          {PIPELINE.map((s, i) => (
            <React.Fragment key={s.name}>
              <div className="l-pipe-step">
                <div className="l-pipe-num">{s.n}</div>
                <div className="l-pipe-name">{s.name}</div>
                <div className="l-pipe-desc">{s.desc}</div>
              </div>
              {i < PIPELINE.length - 1 && (
                <div className="l-pipe-arrow">→</div>
              )}
            </React.Fragment>
          ))}
        </div>
      </section>

      {/* ── CTA FINAL ───────────────────────────────────────────── */}
      <section className="l-cta">
        <div className="l-cta-orb" />
        <h2 className="section-heading" style={{ fontSize: "34px", marginBottom: "12px" }}>
          Prêt à automatiser vos CDC ?
        </h2>
        <p className="section-sub" style={{ margin: "0 auto 28px" }}>
          Remplissez le formulaire et recevez votre cahier des charges
          complet en moins d'une minute.
        </p>
        <button className="btn btn-primary btn-lg" onClick={() => navigate("/new")}>
          Lancer SystemReq gratuitement ↗
        </button>
      </section>

    </div>
  );
}