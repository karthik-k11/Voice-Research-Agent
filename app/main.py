#Necessary imports
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

#Enable CORS (Allows the browser to talk to the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

#Defining the Data Model
class VoiceQuery(BaseModel):
    text: str

#The API Endpoint
@app.post("/process-voice")
async def process_voice(query: VoiceQuery):
    print(f"🎤 RECEIVED AUDIO TEXT: {query.text}")
    
    response_text = f"I heard you say: {query.text}. The research agent is not active yet, but the connection is working."
    
    return {"reply": response_text}

#Root endpoint to check status
@app.get("/")
async def read_root():
    return {"status": "Deep-Dive Agent is Online"}