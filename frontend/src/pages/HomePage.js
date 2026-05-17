/**
 * pages/HomePage.js — Page d'accueil de SystemReq
 *
 * Affiche l'en-tête et le formulaire ClientForm.
 * Quand le formulaire est soumis, redirige vers SessionPage.
 */

import React from "react";
import { useNavigate } from "react-router-dom";
import ClientForm from "../components/forms/ClientForm";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();

  const handleSessionStarted = (session) => {
    // Redirige vers la page de suivi du pipeline
    navigate(`/session/${session.id}`);
  };

  return (
    <div className="home-page">
      <div className="home-header">
        <h1 className="home-title">SystemReq</h1>
        <p className="home-subtitle">
          Remplissez le formulaire ci-dessous. Nos agents IA analyseront
          vos besoins et généreront automatiquement votre cahier des charges.
        </p>
      </div>

      <ClientForm onSessionStarted={handleSessionStarted} />
    </div>
  );
}