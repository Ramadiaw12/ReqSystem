"""
agents/collector.py — Agent de collecte des besoins clients

Rôle : recevoir les données brutes du formulaire EPS SARL
(nom, email, services, budget, description...) et les transformer
en une liste structurée de besoins compréhensibles par l'agent suivant.
"""

from agents.base_agent import BaseAgent

SYSTEM_PROMPT = """
Tu es un expert en recueil de besoins logiciels et digitaux.
Tu travailles pour EPS SARL, une agence web au Maroc.

À partir des informations brutes d'un formulaire client, tu dois :
1. Identifier et extraire tous les besoins explicites (ce que le client demande directement)
2. Identifier les besoins implicites (ce qui est nécessaire mais non mentionné)
3. Reformuler chaque besoin de façon claire et professionnelle
4. Poser des questions de clarification si des informations manquent

Réponds UNIQUEMENT en JSON valide avec ce format exact :
{
  "needs": [
    {
      "type": "fonctionnel",
      "description": "Le site doit afficher les services proposés par le client"
    },
    {
      "type": "non-fonctionnel",
      "description": "Le site doit être responsive sur mobile, tablette et desktop"
    },
    {
      "type": "technique",
      "description": "Intégration d'un certificat SSL pour sécuriser le site"
    }
  ],
  "questions": [
    "Avez-vous déjà un logo ou une charte graphique existante ?",
    "Souhaitez-vous un système de blog ou d'actualités ?"
  ],
  "summary": "Résumé en 2-3 phrases du projet compris"
}

Les types possibles sont : fonctionnel, non-fonctionnel, technique, contenu, sécurité, performance.
"""


class CollectorAgent(BaseAgent):
    """
    Agent 1 — Collecte et extraction des besoins depuis le formulaire client.

    Entrée (payload) :
        client_name   : nom complet du client
        email         : email de contact
        telephone     : numéro de téléphone
        site_web      : site web actuel (si existant)
        ville         : ville du client
        pays          : pays du client
        budget        : budget en EUR
        services      : liste des services cochés dans le formulaire
        description   : description libre du projet (optionnel)

    Sortie (dict) :
        needs         : liste de besoins structurés
        questions     : questions de clarification
        summary       : résumé du projet
    """

    def __init__(self):
        super().__init__(name="CollectorAgent")

    async def run(self, session_id: str, payload: dict) -> dict:
        self.log(f"Démarrage collecte — session {session_id}")

        # Construction du message utilisateur 
        services = ", ".join(payload.get("services", []))
        budget   = payload.get("budget", "Non précisé")

        user_message = f"""
Voici les informations du formulaire client à analyser :

Nom & Prénom   : {payload.get("client_name", "Non renseigné")}
Email          : {payload.get("email", "Non renseigné")}
Téléphone      : {payload.get("telephone", "Non renseigné")}
Site web actuel: {payload.get("site_web", "Aucun")}
Ville          : {payload.get("ville", "Non renseignée")}
Pays           : {payload.get("pays", "Non renseigné")}
Budget (EUR)   : {budget}
Services voulus: {services}
Description    : {payload.get("description", "Aucune description fournie")}

Analyse ces informations et extrais les besoins du projet.
"""

        #  Appel au LLM
        result = await self.ask_llm(SYSTEM_PROMPT, user_message)

        # Validation du résultat 
        if "error" in result:
            return self.build_error_response(
                "Échec de l'extraction des besoins", session_id
            )

        # On s'assure que les clés attendues sont présentes
        result.setdefault("needs",     [])
        result.setdefault("questions", [])
        result.setdefault("summary",   "")
        result["success"]    = True
        result["session_id"] = session_id

        self.log(f"Collecte terminée — {len(result['needs'])} besoins extraits")
        return result