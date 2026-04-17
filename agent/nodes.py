from core.state import AgentState
from core.config import settings
from agent.prompts import SYSTEM_PROMPT
from anthropic import AsyncAnthropic
import json

anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

async def plan_node(state: AgentState):
    print("\n[Brain] Reading alert and generating playbook...")
    
    alert_string = json.dumps(state["alert"], indent=2)
    
    try:
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": f"Triage this alert and build a playbook:\n{alert_string}"}
            ]
        )
        
        # The LLM's response is our dynamic playbook!
        agent_analysis = response.content[0].text
        print("\n[+] LLM Playbook Generated:")
        print(agent_analysis)
        
        return {"dynamic_playbook": [agent_analysis], "verdict": "investigating"}
        
    except Exception as e:
        print(f"[!] Error calling LLM: {e}")
        return {"dynamic_playbook": [f"Error: {e}"], "verdict": "pending"}

def execute_node(state: AgentState):
    print("\n[Muscle] (Mock) Executing tools defined in playbook...")
    return {"tool_results": ["Mock VT Result: Clean"]}

def reflect_node(state: AgentState):
    print("\n[Reflect] Evaluating evidence...")
    return {"verdict": "pending"} # Ends the graph for now