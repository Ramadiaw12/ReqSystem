<div align="center">

<!-- TITRE ANIMÉ -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=3000&pause=1000&color=0EA5FF&center=true&vCenter=true&repeat=true&width=700&lines=SystemReq+%F0%9F%A4%96;Syst%C3%A8me+Multi-Agents+IA;G%C3%A9n%C3%A9ration+Automatique+de+CDC;EPS+SARL+%7C+Projet+de+Stage" alt="Typing SVG" />

<br/>

<!-- BADGES -->
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/Licence-MIT-22C55E?style=for-the-badge)
![Status](https://img.shields.io/badge/Statut-En%20production-0EA5FF?style=for-the-badge)

<br/>

> **SystemReq** est un système multi-agents basé sur l'intelligence artificielle,
> conçu pour automatiser l'analyse des besoins clients et la génération
> de cahiers des charges préliminaires — développé dans le cadre d'un stage chez **EPS SARL**.

<br/>

<!-- DEMO GIF PLACEHOLDER -->
```
┌─────────────────────────────────────────────┐
│  Formulaire Client  →  3 Agents IA  →  CDC  │
│        60 secondes · Word · PDF              │
└─────────────────────────────────────────────┘
```

</div>

---

## 📋 Table des matières

- [🎯 Présentation](#-présentation)
- [🏗️ Architecture](#️-architecture)
- [🤖 Les 3 Agents IA](#-les-3-agents-ia)
- [🛠️ Stack Technique](#️-stack-technique)
- [📁 Structure du Projet](#-structure-du-projet)
- [⚡ Installation](#-installation)
- [🚀 Lancement](#-lancement)
- [🔌 API Endpoints](#-api-endpoints)
- [📄 Export CDC](#-export-cdc)
- [🖥️ Interface](#️-interface)
- [👩‍💻 Auteure](#-auteure)

---

## 🎯 Présentation

**SystemReq** répond à un problème concret chez EPS SARL : la rédaction manuelle d'un cahier des charges prend entre **3 et 8 heures**. Grâce à un pipeline multi-agents alimenté par GPT-4o, ce temps est ramené à **moins de 60 secondes**.

### ✨ Ce que fait le système

| Étape | Action | Durée |
|-------|--------|-------|
| 📝 Formulaire | Le client remplit ses besoins | ~2 min |
| 🧠 Agent Collecte | Extraction et structuration des besoins | ~15s |
| 📊 Agent Analyse | Classification MoSCoW + priorisation | ~20s |
| 📄 Agent Génération | Rédaction du CDC en 15 sections | ~25s |
| ⬇️ Export | Téléchargement Word + PDF | immédiat |

### 🎓 Contexte académique

> Sujet de stage : *"Conception d'un système multi-agents pour l'automatisation
> de l'analyse des besoins clients et la génération de cahiers des charges
> préliminaires — cas d'EPS SARL"*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND  React JS                       │
│         Formulaire → SessionPage → ResultPage + Export       │
└───────────────────────────┬─────────────────────────────────┘
                            │  API REST (Axios)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND  FastAPI                          │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              ORCHESTRATEUR (Coordinator)             │   │
│   └──────┬──────────────┬──────────────────┬────────────┘   │
│          │              │                  │                 │
│          ▼              ▼                  ▼                 │
│   ┌────────────┐ ┌────────────┐   ┌───────────────┐        │
│   │  Collector │ │  Analyzer  │   │   Generator   │        │
│   │   Agent    │ │   Agent    │   │     Agent     │        │
│   └─────┬──────┘ └─────┬──────┘   └───────┬───────┘        │
│         │              │                  │                 │
│         └──────────────┴──────────────────┘                 │
│                        │                                    │
│                        ▼                                    │
│              ┌──────────────────┐                           │
│              │   LLM Client     │                           │
│              │   (OpenAI GPT-4o)│                           │
│              └──────────────────┘                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   Export DOCX  /  PDF   │
              │  python-docx · ReportLab│
              └─────────────────────────┘
```

---

## 🤖 Les 3 Agents IA

### Agent 1 — CollectorAgent 🧠
> Reçoit les données brutes du formulaire et les transforme en besoins structurés.

- Extrait les besoins **explicites** (ce que le client demande)
- Déduit les besoins **implicites** (ce qui est nécessaire mais non dit)
- Pose des **questions de clarification** si des informations manquent
- Produit un **résumé** du projet compris

### Agent 2 — AnalyzerAgent 📊
> Classifie, priorise et valide chaque besoin.

- Applique la méthode **MoSCoW** (Must / Should / Could / Won't)
- Attribue une priorité : **Haute / Moyenne / Basse**
- Numérote chaque exigence : `EF-001`, `ENF-001`...
- Détecte les **conflits** et **doublons**

### Agent 3 — GeneratorAgent 📄
> Rédige le cahier des charges complet en 15 sections professionnelles.

- Contexte et objectifs du projet
- Technologies cibles avec justification
- Architecture logicielle + arborescence complète
- Exigences fonctionnelles et non-fonctionnelles
- Workflow et pipeline de traitement
- Endpoints API documentés
- Planning prévisionnel + livrables
- Critères d'évaluation + bonus

---

## 🛠️ Stack Technique

### Backend
| Technologie | Version | Rôle |
|-------------|---------|------|
| Python | 3.11+ | Langage principal |
| FastAPI | 0.111 | API REST asynchrone |
| OpenAI SDK | 1.25 | Accès GPT-4o |
| Pydantic | 2.7 | Validation des données |
| python-docx | latest | Export Word |
| ReportLab | 4.4 | Export PDF |
| Uvicorn | 0.29 | Serveur ASGI |

### Frontend
| Technologie | Version | Rôle |
|-------------|---------|------|
| React | 18.3 | Interface utilisateur |
| React Router | 6.23 | Navigation SPA |
| Axios | 1.7 | Appels HTTP |
| Inter (font) | — | Typographie professionnelle |

---

## 📁 Structure du Projet

```
Reqsystem/
|
|-- backend/
|   |-- agents/
|   |   |-- base_agent.py        # Classe abstraite partagée
|   |   |-- collector.py         # Agent 1 : collecte des besoins
|   |   |-- analyzer.py          # Agent 2 : analyse et priorisation
|   |   +-- generator.py         # Agent 3 : génération du CDC
|   |
|   |-- orchestrator/
|   |   +-- coordinator.py       # Pipeline : collecte → analyse → génération
|   |
|   |-- api/
|   |   +-- routes/
|   |       |-- sessions.py      # POST/GET sessions
|   |       +-- cdc.py           # Pipeline + export DOCX/PDF
|   |
|   |-- models/
|   |   |-- session.py           # Schémas Pydantic session
|   |   +-- cdc.py               # Schémas Pydantic CDC
|   |
|   |-- utils/
|   |   |-- llm_client.py        # Client OpenAI centralisé
|   |   |-- docx_exporter.py     # Génération Word professionnel
|   |   +-- pdf_exporter.py      # Génération PDF avec ReportLab
|   |
|   |-- main.py                  # Point d'entrée FastAPI + CORS
|   |-- config.py                # Variables d'environnement
|   |-- requirements.txt
|   +-- .env                     # Clé OpenAI (ne pas committer)
|
|-- frontend/
|   +-- src/
|       |-- pages/
|       |   |-- LandingPage.js   # Page marketing
|       |   |-- HomePage.js      # Formulaire client
|       |   |-- SessionPage.js   # Suivi pipeline temps réel
|       |   +-- ResultPage.js    # Affichage + export CDC
|       |
|       |-- components/
|       |   |-- forms/
|       |   |   +-- ClientForm.js
|       |   |-- viewer/
|       |   |   |-- CDCViewer.js
|       |   |   +-- ExportButtons.js
|       |   +-- shared/
|       |       |-- Navbar.js
|       |       +-- AgentStatus.js
|       |
|       |-- services/
|       |   +-- api.js            # Appels HTTP centralisés
|       |
|       |-- styles/
|       |   |-- tokens.css        # Palette night x blue x white
|       |   +-- global.css        # Styles globaux
|       |
|       |-- App.js
|       +-- index.js
|
+-- README.md
```

---

## ⚡ Installation

### Prérequis
- Python **3.11+**
- Node.js **18+**
- Une clé API **OpenAI** (GPT-4o)

### 1. Cloner le projet

```bash
git clone https://github.com/rdiawane/systemreq.git
cd systemreq
```

### 2. Installer le backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Linux / Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Ouvre `.env` et renseigne ta clé OpenAI :

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o
DATABASE_URL=sqlite:///./systemreq.db
FRONTEND_URL=http://localhost:3000
DEBUG=true
```

### 4. Installer le frontend

```bash
cd ../frontend
npm install
```

---

## 🚀 Lancement

Ouvre **deux terminaux** :

```bash
# Terminal 1 — Backend
cd Reqsystem/backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

```bash
# Terminal 2 — Frontend
cd Reqsystem/frontend
npm start
```

Ouvre ton navigateur sur **http://localhost:3000** 🎉

> 📚 Documentation API interactive : **http://localhost:8000/docs**

---

## 🔌 API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `POST` | `/api/sessions/` | Créer une session depuis le formulaire |
| `GET` | `/api/sessions/{id}` | Statut d'une session (polling) |
| `GET` | `/api/sessions/` | Lister toutes les sessions |
| `POST` | `/api/cdc/{id}/run` | Lancer le pipeline 3 agents |
| `GET` | `/api/cdc/{id}` | Récupérer le CDC généré |
| `GET` | `/api/cdc/{id}/export/docx` | Télécharger en Word (.docx) |
| `GET` | `/api/cdc/{id}/export/pdf` | Télécharger en PDF |
| `GET` | `/health` | Santé de l'API |

---

## 📄 Export CDC

Le CDC généré contient **15 sections** :

```
 1. Contexte et présentation du projet
 2. Objectifs du projet
 3. Technologies cibles
 4. Description fonctionnelle détaillée
 5. Architecture logicielle recommandée
 6. Exigences fonctionnelles (EF-001...)
 7. Exigences non-fonctionnelles (ENF-001...)
 8. Workflow et pipeline de traitement
 9. API et endpoints
10. Contraintes du projet
11. Planning prévisionnel
12. Livrables attendus
13. Critères d'évaluation et résultats attendus
14. Bonus et évolutions possibles
15. Conditions et modalités
```

Disponible en **Word (.docx)** et **PDF** avec :
- Page de garde professionnelle
- Sommaire automatique
- En-tête et pied de page sur chaque page
- Tableau des exigences coloré par priorité
- Page de signatures

---

## 🖥️ Interface

### Page d'accueil (Landing)
- Présentation du système
- Démonstration interactive du pipeline
- Statistiques clés

### Formulaire Client
- Nom, email, téléphone, budget
- Services souhaités (checkboxes)
- Description libre du projet

### Suivi Pipeline
- Progression en temps réel des 3 agents
- Polling automatique toutes les 2 secondes
- Animations de statut

### Page Résultat
- Affichage du CDC par sections
- Tableau des exigences filtrable
- Export Word et PDF en un clic

---

## 👩‍💻 Auteure

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2000&pause=500&color=0EA5FF&center=true&vCenter=true&repeat=true&width=400&lines=DIAWANE+Ramatoulaye;AI+Infra+Engineer+student;Stage+EPS+SARL+%7C+2026" alt="Author" />

| | |
|---|---|
| 👩‍🎓 **Auteure** | DIAWANE Ramatoulaye |
| 📧 **Email** | [rdiawane2001@gmail.com](mailto:rdiawane2001@gmail.com) |
| 🏢 **Entreprise** | EPS SARL |
| 📅 **Année** | 2026 |
| 🎯 **Sujet** | Système multi-agents pour la génération de CDC |

</div>

---

<div align="center">

**SystemReq** — Conçu avec ❤️ par DIAWANE Ramatoulaye · EPS SARL · 2026

![Made with](https://img.shields.io/badge/Made%20with-Python%20%2B%20React-0EA5FF?style=for-the-badge)
![AI Powered](https://img.shields.io/badge/Powered%20by-GPT--4o-412991?style=for-the-badge&logo=openai)

</div>