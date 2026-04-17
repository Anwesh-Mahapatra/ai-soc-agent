from typing import TypedDict, Annotated, Literal, List, Dict, Any
import operator

class AgentState(TypedDict):
    alert: Dict[str, Any]                 
    dynamic_playbook: List[str]           
    tool_results: Annotated[list, operator.add] 
    verdict: Literal["malicious", "benign", "investigating", "pending"]
    confidence: float
