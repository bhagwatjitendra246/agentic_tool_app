from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentStep:
    tool: str
    args: Dict[str, Any]
    result: Any


@dataclass
class AgentState:
    original_query: str
    current_value: Optional[Any] = None
    plan: List[Dict[str, Any]] = field(default_factory=list)
    history: List[AgentStep] = field(default_factory=list)
    success: bool = False
    error: Optional[str] = None