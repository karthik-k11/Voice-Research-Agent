##Necessary Imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#IMPORT AGENTS
from app.agents.planner import extract_search_term
from app.agents.researcher import perform_research
from app.agents.brain import think

app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Mount Frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

#Data Model
class VoiceQuery(BaseModel):
    text: str

#The Core Logic Endpoint
@app.post("/process-voice")
async def process_voice(query: VoiceQuery):
    print(f"\nRECEIVED: {query.text}")
    
    if len(query.text) < 3:
        return {"reply": "I didn't catch that. Please speak again."}

    #Optimize the Search
    search_term = extract_search_term(query.text)

    # Execute Search with clean terms
    raw_data = perform_research(search_term)
    
    #Synthesize Answer
    summary = think(raw_data)
    
    print(f"REPLY: {summary}")
    return {"reply": summary}