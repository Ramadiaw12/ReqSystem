"""
agents/generator.py — Agent de génération du CDC détaillé

Génère un cahier des charges complet et structuré incluant :
- Contexte et objectifs pédagogiques/professionnels
- Description fonctionnelle détaillée
- Architecture logicielle recommandée
- Technologies cibles
- Exigences techniques
- Workflow/pipeline
- API endpoints
- Contraintes
- Livrables
- Critères d'évaluation
- Bonus possibles
"""

from agents.base_agent import BaseAgent

SYSTEM_PROMPT = """
Tu es un expert senior en ingénierie logicielle et en rédaction de cahiers des charges professionnels.
Tu travailles pour EPS SARL, une agence digitale.

À partir des exigences analysées d'un projet client, génère un cahier des charges COMPLET,
DÉTAILLÉ et STRUCTURÉ, similaire aux cahiers des charges académiques et professionnels de haut niveau.

Le document doit être précis, technique, et inclure TOUTES les sections suivantes.

Réponds UNIQUEMENT en JSON valide avec ce format exact :
{
  "sections": [
    {
      "id": "s1",
      "title": "1. Contexte et présentation du projet",
      "content": "Description détaillée du contexte du projet, du problème à résoudre, et de la valeur ajoutée apportée par la solution. Minimum 5-8 phrases."
    },
    {
      "id": "s2",
      "title": "2. Objectifs du projet",
      "content": "Liste détaillée des objectifs fonctionnels et techniques du projet. Inclure les objectifs mesurables et les résultats attendus concrets."
    },
    {
      "id": "s3",
      "title": "3. Technologies cibles",
      "content": "Liste complète et justifiée des technologies utilisées : Backend (langage, framework, LLM/IA si applicable), Frontend (framework, bibliothèques), Base de données, API, DevOps, outils de test. Justifier chaque choix technologique."
    },
    {
      "id": "s4",
      "title": "4. Description fonctionnelle détaillée",
      "content": "Description complète de toutes les fonctionnalités du système. Inclure les acteurs, les cas d'utilisation principaux, les flux de données, les interactions entre composants. Détailler chaque module ou agent du système."
    },
    {
      "id": "s5",
      "title": "5. Architecture logicielle recommandée",
      "content": "Description détaillée de l'architecture du système. Inclure : la structure des dossiers du projet (arborescence complète), les composants principaux, les patterns architecturaux utilisés (MVC, microservices, multi-agents, etc.), les interactions entre les couches. Exemple d'arborescence :\nprojet/\n├── backend/\n│   ├── agents/\n│   ├── api/\n│   ├── models/\n│   └── utils/\n├── frontend/\n│   └── src/\n└── README.md"
    },
    {
      "id": "s6",
      "title": "6. Exigences fonctionnelles",
      "content": "Liste numérotée et détaillée de toutes les exigences fonctionnelles. Format : EF-001 : [description précise]. Inclure au minimum 8-12 exigences fonctionnelles couvrant toutes les fonctionnalités demandées."
    },
    {
      "id": "s7",
      "title": "7. Exigences non-fonctionnelles et techniques",
      "content": "Exigences de performance (temps de réponse, charge), sécurité (authentification, chiffrement, HTTPS), compatibilité (navigateurs, appareils), maintenabilité (qualité du code, documentation), scalabilité, accessibilité. Format numéroté : ENF-001 : [description]."
    },
    {
      "id": "s8",
      "title": "8. Workflow et pipeline de traitement",
      "content": "Description détaillée du flux de traitement principal du système, étape par étape. Inclure un schéma textuel du workflow (comme un diagramme ASCII), les états intermédiaires, les conditions de transition entre étapes, les points de validation humaine si applicable."
    },
    {
      "id": "s9",
      "title": "9. API et endpoints",
      "content": "Liste complète des endpoints API avec pour chaque endpoint : méthode HTTP, chemin, description, paramètres attendus, format de réponse. Exemple :\nPOST /api/sessions/ — Créer une session\nGET /api/sessions/{id} — Récupérer le statut\nPOST /api/cdc/{id}/run — Lancer le pipeline\nGET /api/cdc/{id} — Récupérer le CDC\nGET /api/cdc/{id}/export/pdf — Exporter en PDF\nGET /api/cdc/{id}/export/docx — Exporter en Word"
    },
    {
      "id": "s10",
      "title": "10. Contraintes du projet",
      "content": "Toutes les contraintes identifiées : contraintes techniques (versions, compatibilité), contraintes métier (délais, budget), contraintes légales (RGPD, confidentialité), contraintes d'utilisation, contraintes d'infrastructure. Chaque contrainte doit être justifiée."
    },
    {
      "id": "s11",
      "title": "11. Planning prévisionnel",
      "content": "Planning détaillé par phases : Phase 1 - Cadrage et conception (durée, livrables), Phase 2 - Développement backend (durée, livrables), Phase 3 - Développement frontend (durée, livrables), Phase 4 - Intégration et tests (durée, livrables), Phase 5 - Déploiement et formation (durée, livrables). Total estimé et jalons clés."
    },
    {
      "id": "s12",
      "title": "12. Livrables attendus",
      "content": "Liste complète et détaillée des livrables du projet : code source complet et documenté, README.md avec instructions d'installation et d'exécution, rapport technique expliquant l'architecture et les choix réalisés, documentation API (Swagger/OpenAPI), jeux de tests et résultats, captures d'écran ou vidéo de démonstration, guide utilisateur."
    },
    {
      "id": "s13",
      "title": "13. Critères d'évaluation et résultats attendus",
      "content": "Critères d'évaluation détaillés avec pondération : Architecture et conception, Qualité du code, Fonctionnalités implémentées, Performance et sécurité, Documentation, Présentation et démonstration. Résultats concrets attendus à la fin du projet."
    },
    {
      "id": "s14",
      "title": "14. Bonus et évolutions possibles",
      "content": "Fonctionnalités optionnelles et améliorations futures possibles : persistance en base de données, authentification JWT, dockerisation, tests unitaires et d'intégration, CI/CD, monitoring, export PDF/Word avancé, historique des sessions, tableau de bord analytique."
    },
    {
      "id": "s15",
      "title": "15. Conditions et modalités",
      "content": "Modalités de paiement (30% à la commande, 40% à la livraison de recette, 30% à la mise en production), propriété intellectuelle, garantie (3 mois après mise en ligne), confidentialité des données, conditions de maintenance."
    }
  ],
  "metadata": {
    "title": "Cahier des charges — [Nom du projet]",
    "client": "Nom du client",
    "agency": "EPS SARL",
    "version": "1.0",
    "status": "Préliminaire",
    "technologies": ["tech1", "tech2", "tech3"]
  }
}

IMPORTANT :
- Chaque section doit être SUBSTANTIELLE (minimum 8-15 phrases ou éléments).
- Sois PRÉCIS et TECHNIQUE — cite des technologies réelles, des versions, des patterns concrets.
- L'architecture logicielle doit inclure une ARBORESCENCE DE FICHIERS complète et réaliste.
- Les exigences doivent être NUMÉROTÉES (EF-001, ENF-001, etc.).
- Le workflow doit inclure un SCHÉMA TEXTUEL avec des flèches (→, ↓, ├──).
- Les API doivent lister les ENDPOINTS COMPLETS avec méthodes HTTP.
- Adapte le contenu AU CONTEXTE EXACT du projet (services choisis, budget, localisation).
"""


class GeneratorAgent(BaseAgent):
    """
    Agent 3 — Génération du cahier des charges complet et détaillé.

    Entrée (payload) :
        requirements : liste d'exigences issues de AnalyzerAgent
        client_name  : nom du client
        project_name : nom du projet
        services     : services sélectionnés
        budget       : budget en EUR
        ville        : ville du client
        pays         : pays du client
        description  : description libre du projet

    Sortie (dict) :
        sections     : 15 sections détaillées du CDC
        metadata     : informations générales du document
    """

    def __init__(self):
        super().__init__(name="GeneratorAgent")

    async def run(self, session_id: str, payload: dict) -> dict:
        self.log(f"Démarrage génération CDC détaillé — session {session_id}")

        requirements = payload.get("requirements", [])
        services     = ", ".join(payload.get("services", []))
        budget       = payload.get("budget", "Non précisé")
        description  = payload.get("description", "")

        if not requirements:
            return self.build_error_response(
                "Aucune exigence reçue pour générer le CDC", session_id
            )

        # Formatage détaillé des exigences
        req_text = "\n".join([
            f"- [{r.get('id','?')}] [Priorité:{r.get('priority','?')}] "
            f"[{r.get('category','?')}] [MoSCoW:{r.get('moscow','?')}] "
            f"{r.get('description','')}"
            for r in requirements
        ])

        user_message = f"""
Informations complètes du projet à documenter :

Client       : {payload.get("client_name", "Non renseigné")}
Projet       : {payload.get("project_name", "Projet web")}
Services     : {services}
Budget       : {budget} EUR
Localisation : {payload.get("ville", "")} — {payload.get("pays", "")}
Description  : {description}

Exigences analysées ({len(requirements)} exigences) :
{req_text}

Génère un cahier des charges COMPLET, DÉTAILLÉ et PROFESSIONNEL en 15 sections.
Sois précis sur les technologies, l'architecture, les endpoints API et l'arborescence du projet.
Adapte tout le contenu au contexte exact de ce projet.
"""

        # Appel LLM avec max tokens élevé pour un document complet
        self.log("Appel LLM pour génération complète (15 sections)...")
        result = await self.llm.chat_json(
            SYSTEM_PROMPT,
            user_message,
            temperature=0.2,
        )

        if "error" in result:
            return self.build_error_response(
                "Échec de la génération du CDC", session_id
            )

        result.setdefault("sections",  [])
        result.setdefault("metadata",  {})
        result["success"]    = True
        result["session_id"] = session_id

        total = len(result["sections"])
        self.log(f"Génération terminée — {total} sections produites")
        return result