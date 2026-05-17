"""
agents/analyzer.py — Agent d'analyse et priorisation des besoins

Rôle : prendre la liste de besoins bruts produite par CollectorAgent
et les transformer en exigences structurées, priorisées (méthode MoSCoW),
dédupliquées et validées.
"""

from agents.base_agent import BaseAgent

SYSTEM_PROMPT = """
Tu es un analyste logiciel senior spécialisé en ingénierie des exigences (requirements engineering).
Tu travailles pour EPS SARL, une agence web au Maroc.

À partir d'une liste de besoins bruts extraits d'un formulaire client, tu dois :
1. Classifier chaque besoin selon sa catégorie
2. Attribuer une priorité MoSCoW (Must, Should, Could, Won't)
3. Attribuer un niveau de priorité lisible (Haute, Moyenne, Basse)
4. Détecter et signaler les doublons ou contradictions
5. Ajouter des exigences techniques implicites si nécessaire
6. Générer un identifiant unique par exigence (REQ-001, REQ-002...)

Réponds UNIQUEMENT en JSON valide avec ce format exact :
{
  "requirements": [
    {
      "id": "REQ-001",
      "category": "fonctionnel",
      "priority": "Haute",
      "moscow": "Must",
      "description": "Le site doit afficher les services proposés avec descriptions et tarifs",
      "source": "explicite"
    },
    {
      "id": "REQ-002",
      "category": "non-fonctionnel",
      "priority": "Haute",
      "moscow": "Must",
      "description": "Le site doit être responsive sur mobile, tablette et desktop",
      "source": "implicite"
    }
  ],
  "conflicts": [
    "Description du conflit détecté si applicable"
  ],
  "duplicates": [
    "Description du doublon détecté si applicable"
  ],
  "stats": {
    "total": 10,
    "haute": 4,
    "moyenne": 4,
    "basse": 2
  }
}

Catégories possibles : fonctionnel, non-fonctionnel, technique, sécurité, performance, contenu, SEO, maintenance.
Source : "explicite" (demandé directement) ou "implicite" (déduit du contexte).
"""


class AnalyzerAgent(BaseAgent):
    """
    Agent 2 — Classification et priorisation des besoins.

    Entrée (payload) :
        needs       : liste de besoins issus de CollectorAgent
        client_name : pour le contexte
        services    : services sélectionnés dans le formulaire
        budget      : budget du projet

    Sortie (dict) :
        requirements : liste d'exigences structurées avec ID et priorité
        conflicts    : liste de conflits détectés
        duplicates   : liste de doublons
        stats        : compteurs par niveau de priorité
    """

    def __init__(self):
        super().__init__(name="AnalyzerAgent")

    async def run(self, session_id: str, payload: dict) -> dict:
        self.log(f"Démarrage analyse — session {session_id}")

        needs    = payload.get("needs", [])
        services = ", ".join(payload.get("services", []))
        budget   = payload.get("budget", "Non précisé")

        if not needs:
            return self.build_error_response(
                "Aucun besoin reçu à analyser", session_id
            )

        # Formatage des besoins pour le LLM 
        needs_text = "\n".join([
            f"- [{b.get('type', 'inconnu')}] {b.get('description', '')}"
            for b in needs
        ])

        user_message = f"""
Contexte du projet :
  Client   : {payload.get("client_name", "Non renseigné")}
  Services : {services}
  Budget   : {budget} EUR

Besoins bruts à analyser ({len(needs)} besoins) :
{needs_text}

Analyse, classe et priorise ces besoins selon la méthode MoSCoW.
Ajoute les exigences techniques implicites nécessaires pour un projet web professionnel.
"""

        # Appel au LLM 
        result = await self.ask_llm(SYSTEM_PROMPT, user_message)

        if "error" in result:
            return self.build_error_response(
                "Échec de l'analyse des besoins", session_id
            )

        # Validation et valeurs par défaut 
        result.setdefault("requirements", [])
        result.setdefault("conflicts",    [])
        result.setdefault("duplicates",   [])
        result.setdefault("stats",        {})
        result["success"]    = True
        result["session_id"] = session_id

        total = len(result["requirements"])
        self.log(f"Analyse terminée — {total} exigences générées")
        return result