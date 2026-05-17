from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class SessionStatus(str, Enum):
    CREATED    = "created"
    COLLECTING = "collecting"
    ANALYZING  = "analyzing"
    GENERATING = "generating"
    DONE       = "done"
    ERROR      = "error"

class SessionCreate(BaseModel):
    client_name:  str           = Field(..., min_length=2)
    email:        str           = Field(...)
    telephone:    Optional[str] = None
    site_web:     Optional[str] = None
    ville:        Optional[str] = None
    pays:         Optional[str] = None
    budget:       Optional[str] = None
    services:     List[str]     = []
    description:  Optional[str] = None
    project_name: Optional[str] = "Projet web"

class SessionResponse(BaseModel):
    id:           str
    status:       SessionStatus
    client_name:  str
    project_name: str
    created_at:   str
    updated_at:   str
    error:        Optional[str] = None

    class Config:
        from_attributes = True
