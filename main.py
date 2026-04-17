from fastapi import FastAPI
from typing import Dict, Any
import uvicorn
from datetime import datetime
from agent.graph import build_agent_graph

app = FastAPI(title="SIEM-Agnostic AI SOC Agent", version="0.4.0")

@app.get("/")
async def root():
    return {"status": "Agent API is online", "time": datetime.now().isoformat()}

@app.post("/webhook/alert")
async def receive_alert(payload: Dict[str, Any]):
    print(f"\n[!] INCOMING SIEM WEBHOOK AT {datetime.now().strftime('%H:%M:%S')}")
    
    agent_graph = build_agent_graph()
    
    initial_state = {
        "alert": payload,
        "dynamic_playbook": [],
        "tool_results": [],
        "verdict": "pending",
        "confidence": 0.0
    }
    
    print("\n--- STARTING LANGGRAPH AGENT RUN ---")
    
    # We use ainvoke (async invoke) to run the graph and wait for it to finish
    final_state = await agent_graph.ainvoke(initial_state)
            
    print("\n--- LANGGRAPH RUN COMPLETE ---")
    
    return {
        "status": "success", 
        "message": "Playbook generated.",
        "playbook": final_state["dynamic_playbook"][0]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)