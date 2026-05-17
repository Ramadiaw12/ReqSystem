"""
agents/generator.py — Agent de génération du cahier des charges

Rôle : prendre les exigences analysées et produire un cahier des charges
complet, structuré et professionnel, prêt à être affiché dans React
et exporté en DOCX / PDF.
"""

from agents.base_agent import BaseAgent

SYSTEM_PROMPT = """
Tu es un expert en rédaction de cahiers des charges pour des projets web et digitaux.
Tu travailles pour EPS SARL, une agence web au Maroc.
Tu rédiges des documents professionnels, clairs et complets destinés aux clients.

À partir des exigences analysées d'un projet, génère un cahier des charges préliminaire
structuré en sections. Chaque section doit être rédigée en français professionnel,
avec un niveau de détail adapté à un document contractuel.

Réponds UNIQUEMENT en JSON valide avec ce format exact :
{
  "sections": [
    {
      "id": "s1",
      "title": "1. Présentation du projet",
      "content": "Contenu détaillé de la section..."
    },
    {
      "id": "s2",
      "title": "2. Objectifs du projet",
      "content": "..."
    },
    {
      "id": "s3",
      "title": "3. Périmètre fonctionnel",
      "content": "..."
    },
    {
      "id": "s4",
      "title": "4. Exigences fonctionnelles",
      "content": "..."
    },
    {
      "id": "s5",
      "title": "5. Exigences non-fonctionnelles",
      "content": "..."
    },
    {
      "id": "s6",
      "title": "6. Contraintes techniques",
      "content": "..."
    },
    {
      "id": "s7",
      "title": "7. Planning prévisionnel",
      "content": "..."
    },
    {
      "id": "s8",
      "title": "8. Budget estimatif",
      "content": "..."
    },
    {
      "id": "s9",
      "title": "9. Livrables attendus",
      "content": "..."
    },
    {
      "id": "s10",
      "title": "10. Conditions et modalités",
      "content": "..."
    }
  ],
  "metadata": {
    "title": "Cahier des charges — [Nom du projet]",
    "client": "Nom du client",
    "agency": "EPS SARL",
    "version": "1.0",
    "status": "Préliminaire"
  }
}

Chaque section doit être substantielle (minimum 3-5 phrases).
Utilise les exigences fournies pour remplir les sections de façon précise et contextuelle.
Le ton doit être professionnel, clair et sans ambiguïté.
"""


class GeneratorAgent(BaseAgent):
    """
    Agent 3 — Génération du cahier des charges complet.

    Entrée (payload) :
        requirements : liste d'exigences issues de AnalyzerAgent
        client_name  : nom du client
        project_name : nom du projet
        services     : services sélectionnés
        budget       : budget en EUR
        ville        : ville du client
        pays         : pays du client

    Sortie (dict) :
        sections     : liste des sections du CDC avec titre et contenu
        metadata     : informations générales du document
    """

    def __init__(self):
        super().__init__(name="GeneratorAgent")

    async def run(self, session_id: str, payload: dict) -> dict:
        self.log(f"Démarrage génération CDC — session {session_id}")

        requirements = payload.get("requirements", [])
        services     = ", ".join(payload.get("services", []))
        budget       = payload.get("budget", "Non précisé")

        if not requirements:
            return self.build_error_response(
                "Aucune exigence reçue pour générer le CDC", session_id
            )

        # ── Formatage des exigences pour le LLM ──────────────────────────
        req_text = "\n".join([
            f"- [{r.get('id', '?')}] [{r.get('priority', '?')}] "
            f"[{r.get('category', '?')}] {r.get('description', '')}"
            for r in requirements
        ])

        user_message = f"""
Informations du projet :
  Client       : {payload.get("client_name", "Non renseigné")}
  Projet       : {payload.get("project_name", "Projet web")}
  Services     : {services}
  Budget       : {budget} EUR
  Localisation : {payload.get("ville", "")} — {payload.get("pays", "")}

Exigences analysées ({len(requirements)} exigences) :
{req_text}

Génère un cahier des charges préliminaire complet et professionnel
en te basant sur ces informations. Sois précis, concret et contextuel.
"""

        # Appel au LLM 
        result = await self.ask_llm(SYSTEM_PROMPT, user_message)

        if "error" in result:
            return self.build_error_response(
                "Échec de la génération du CDC", session_id
            )

        #  Validation 
        result.setdefault("sections",  [])
        result.setdefault("metadata",  {})
        result["success"]    = True
        result["session_id"] = session_id

        total = len(result["sections"])
        self.log(f"Génération terminée — {total} sections produites")
        return result