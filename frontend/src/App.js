/**
 * App.js — Routeur principal SystemReq v2
 *
 * Routes :
 *   /                    → LandingPage (marketing)
 *   /new                 → HomePage (formulaire)
 *   /session/:sessionId  → SessionPage
 *   /result/:sessionId   → ResultPage
 */
import React from "react";
import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import HomePage    from "./pages/HomePage";
import SessionPage from "./pages/SessionPage";
import ResultPage  from "./pages/ResultPage";
import Navbar      from "./components/shared/Navbar";
import "./styles/global.css";

export default function App() {
  return (
    <div className="app">
      {/* Background animé global */}
      <div className="bg-layer">
        <div className="grid-bg" />
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
      </div>

      <Navbar />

      <main>
        <Routes>
          <Route path="/"                   element={<LandingPage />} />
          <Route path="/new"                element={<HomePage />}    />
          <Route path="/session/:sessionId" element={<SessionPage />} />
          <Route path="/result/:sessionId"  element={<ResultPage />}  />
        </Routes>
      </main>
    </div>
  );
}