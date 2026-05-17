/**
 * App.js — Routeur principal de SystemReq
 *
 * 3 routes :
 *   /                    → HomePage (formulaire)
 *   /session/:sessionId  → SessionPage (suivi pipeline)
 *   /result/:sessionId   → ResultPage (CDC généré)
 */

import React from "react";
import { Routes, Route } from "react-router-dom";
import HomePage    from "./pages/HomePage";
import SessionPage from "./pages/SessionPage";
import ResultPage  from "./pages/ResultPage";
import Navbar      from "./components/shared/Navbar";
import "./App.css";

export default function App() {
  return (
    <div className="app">
      <Navbar />
      <main>
        <Routes>
          <Route path="/"                   element={<HomePage />}    />
          <Route path="/session/:sessionId" element={<SessionPage />} />
          <Route path="/result/:sessionId"  element={<ResultPage />}  />
        </Routes>
      </main>
    </div>
  );
}   