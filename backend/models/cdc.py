from pydantic import BaseModel
from typing import List, Optional

class CDCResponse(BaseModel):
    session_id:   str
    client_name:  str
    project_name: str
    services:     List[str]  = []
    budget:       Optional[str] = None
    ville:        Optional[str] = None
    pays:         Optional[str] = None
    requirements: List[dict] = []
    stats:        dict       = {}
    sections:     List[dict] = []
    metadata:     dict       = {}
    summary:      Optional[str] = None
    questions:    List[str]  = []
    generated_at: str
