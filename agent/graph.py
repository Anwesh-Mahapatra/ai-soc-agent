from langgraph.graph import StateGraph, START, END
from core.state import AgentState
from agent.nodes import plan_node, execute_node, reflect_node

def build_agent_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("plan", plan_node)
    workflow.add_node("execute", execute_node)
    workflow.add_node("reflect", reflect_node)
    
    workflow.add_edge(START, "plan")
    workflow.add_edge("plan", "execute")
    workflow.add_edge("execute", "reflect")
    
    workflow.add_conditional_edges(
        "reflect",
        lambda s: "plan" if s["verdict"] == "investigating" else END
    )
    
    return workflow.compile()