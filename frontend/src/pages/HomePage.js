import React from "react";
import { useNavigate } from "react-router-dom";
import ClientForm from "../components/forms/ClientForm";

export default function HomePage() {
  const navigate = useNavigate();

  const handleSessionStarted = (session) => {
    navigate(`/session/${session.id}`);
  };

  return (
    <div className="client-form-wrap">
      <div className="client-form-header">
        <h1 className="gradient-text">Nouvelle analyse</h1>
        <p>Remplissez le formulaire — le CDC sera généré en 60 secondes.</p>
      </div>
      <ClientForm onSessionStarted={handleSessionStarted} />
    </div>
  );
}
