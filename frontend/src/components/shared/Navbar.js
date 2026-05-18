/**
 * components/shared/Navbar.js — Navigation SystemReq · thème nuit
 */
import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">
        SystemReq <span>· EPS SARL</span>
      </Link>
      <div className="navbar-links">
        <Link to="/">Accueil</Link>
        <Link to="/new">Nouvelle analyse</Link>
      </div>
      <button
        className="btn btn-primary btn-sm"
        onClick={() => navigate("/new")}
      >
        Démarrer ↗
      </button>
    </nav>
  );
}