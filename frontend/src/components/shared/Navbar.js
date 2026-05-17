import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        SystemReq <span>· EPS SARL</span>
      </Link>
      <div className="navbar-links">
        <Link to="/">Nouvelle analyse</Link>
      </div>
    </nav>
  );
}
