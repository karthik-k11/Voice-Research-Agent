##Necessary Imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#IMPORT AGENTS
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
    print(f"\n🎤 RECEIVED: {query.text}")
    
    if len(query.text) < 3:
        return {"reply": "I didn't catch that. Please speak again."}

    #Research Phase
    raw_data = perform_research(query.text)
    
    #Thinking Phase 3
    summary = think(raw_data)
    
    print(f"REPLY: {summary}")
    
    ##Response
    return {"reply": summary}

@app.get("/")
async def read_root():
    return {"status": "Deep-Dive Agent is Online"}