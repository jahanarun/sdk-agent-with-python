from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.models.enumerations import StrategyName

class Strategy(BaseModel):
    name: StrategyName
    agents_involved: List[str]


class Message(BaseModel):
    content: str
    role: Optional[str] = None
    id: str
    metadata: Optional[Dict[str, Any]] = None  # For any additional metadata, including adaptive card responses

class AgentRequest(BaseModel):
    conversation_id: str
    message: Message
    history: Optional[List[Message]] = None
    strategy: Optional[Strategy] = None