import os
import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langgraph_app import app

# Ensure API Key mapping for LangChain
if os.environ.get("GEMINI_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY")

api = FastAPI(title="Multi-Agent Writer API")

# Add CORS so React frontend can call it
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")
api.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

@api.post("/api/research")
async def research_topic(request: ResearchRequest):
    inputs = {
        "topic": request.topic, 
        "research_notes": [], 
        "final_draft": ""
    }
    
    async def event_generator():
        try:
            # We use stream() to get events from each node as they finish
            for output in app.stream(inputs):
                # output is a dict like {'researcher': {'research_notes': [...]}}
                for node_name, state_update in output.items():
                    event_data = {
                        "agent": node_name,
                        "status": f"{node_name.capitalize()} finished its task.",
                        "data": state_update.get("final_draft", "") if node_name == "writer" else ""
                    }
                    yield f"data: {json.dumps(event_data)}\n\n"
                    await asyncio.sleep(0.1) # Small pause for streaming effect
            
            # Send completion event
            yield f"data: {json.dumps({'agent': 'system', 'status': 'COMPLETE'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'agent': 'system', 'status': f'ERROR: {str(e)}'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)
