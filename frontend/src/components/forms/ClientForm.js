/**
 * components/forms/ClientForm.js — Formulaire de saisie client EPS SARL
 *
 * Reproduit le formulaire visible dans la capture d'écran :
 * Nom & Prénom, Email, Téléphone, Site web, Ville, Pays,
 * Budget, Services (checkboxes), Description libre.
 */

import React, { useState } from "react";
import { createSession, runPipeline } from "../../services/api";
import "./ClientForm.css";

const SERVICES_LIST = [
  "Site Vitrine",
  "E-commerce",
  "Shopify",
  "WordPress",
  "App Mobile",
  "SEO",
  "Maintenance",
  "Autre",
];

const PAYS_LIST = [
  "Maroc", "France", "Belgique", "Suisse", "Tunisie",
  "Algérie", "Sénégal", "Côte d'Ivoire", "Canada", "Autre",
];

const INITIAL_FORM = {
  client_name:  "",
  email:        "",
  telephone:    "",
  site_web:     "",
  ville:        "",
  pays:         "",
  budget:       "",
  services:     [],
  description:  "",
  project_name: "",
};

export default function ClientForm({ onSessionStarted }) {
  const [form, setForm]       = useState(INITIAL_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);

  // ── Handlers ────────────────────────────────────────────────────────────────

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleServiceToggle = (service) => {
    setForm((prev) => {
      const already = prev.services.includes(service);
      return {
        ...prev,
        services: already
          ? prev.services.filter((s) => s !== service)
          : [...prev.services, service],
      };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validation minimale
    if (!form.client_name.trim()) return setError("Le nom du client est obligatoire.");
    if (!form.email.trim())       return setError("L'email est obligatoire.");
    if (form.services.length === 0) return setError("Sélectionne au moins un service.");

    setLoading(true);
    try {
      // 1. Créer la session
      const session = await createSession(form);

      // 2. Lancer le pipeline en arrière-plan
      await runPipeline(session.id);

      // 3. Passer à la page de suivi
      onSessionStarted(session);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Erreur lors de la création de la session. Vérifie que le backend est démarré."
      );
    } finally {
      setLoading(false);
    }
  };

  // ── Rendu ────────────────────────────────────────────────────────────────────

  return (
    <form className="client-form" onSubmit={handleSubmit} noValidate>

      {/* Ligne 1 : Nom & Site web */}
      <div className="form-row">
        <div className="form-group">
          <label>Nom &amp; Prénom <span className="required">*</span></label>
          <input
            type="text"
            name="client_name"
            value={form.client_name}
            onChange={handleChange}
            placeholder="Jean Marc"
            required
          />
        </div>
        <div className="form-group">
          <label>Site web (URL)</label>
          <input
            type="url"
            name="site_web"
            value={form.site_web}
            onChange={handleChange}
            placeholder="https://www.example.com"
          />
        </div>
      </div>

      {/* Ligne 2 : Email & Téléphone */}
      <div className="form-row">
        <div className="form-group">
          <label>Email <span className="required">*</span></label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            placeholder="jacques@martin.com"
            required
          />
        </div>
        <div className="form-group">
          <label>Téléphone <span className="required">*</span></label>
          <input
            type="tel"
            name="telephone"
            value={form.telephone}
            onChange={handleChange}
            placeholder="+212 06 00 00 00"
          />
        </div>
      </div>

      {/* Ligne 3 : Ville & Pays */}
      <div className="form-row">
        <div className="form-group">
          <label>Ville</label>
          <input
            type="text"
            name="ville"
            value={form.ville}
            onChange={handleChange}
            placeholder="Casablanca"
          />
        </div>
        <div className="form-group">
          <label>Pays <span className="required">*</span></label>
          <select name="pays" value={form.pays} onChange={handleChange}>
            <option value="">Sélectionner un pays</option>
            {PAYS_LIST.map((p) => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Nom du projet */}
      <div className="form-group full-width">
        <label>Nom du projet</label>
        <input
          type="text"
          name="project_name"
          value={form.project_name}
          onChange={handleChange}
          placeholder="Site vitrine de mon entreprise"
        />
      </div>

      {/* Budget */}
      <div className="form-group full-width">
        <label>Budget du projet (EUR) <span className="required">*</span></label>
        <input
          type="number"
          name="budget"
          value={form.budget}
          onChange={handleChange}
          placeholder="500"
          min="0"
        />
      </div>

      {/* Services */}
      <div className="form-group full-width">
        <label>Services souhaités <span className="required">*</span></label>
        <div className="services-grid">
          {SERVICES_LIST.map((service) => (
            <label
              key={service}
              className={`service-chip ${form.services.includes(service) ? "selected" : ""}`}
            >
              <input
                type="checkbox"
                checked={form.services.includes(service)}
                onChange={() => handleServiceToggle(service)}
              />
              {service}
            </label>
          ))}
        </div>
      </div>

      {/* Description */}
      <div className="form-group full-width">
        <label>Description du projet</label>
        <textarea
          name="description"
          value={form.description}
          onChange={handleChange}
          rows={5}
          placeholder="Décrivez votre projet, vos besoins, vos objectifs, vos contraintes..."
        />
      </div>

      {/* Erreur */}
      {error && <p className="form-error">{error}</p>}

      {/* Submit */}
      <button type="submit" className="btn btn-primary" style={{width:"100%", marginTop:"0.5rem"}} disabled={loading}>
        {loading ? "Analyse en cours…" : "Générer le cahier des charges"}
      </button>

    </form>
  );
}