##Necessary Imports
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.agents import planner, researcher, brain
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

##Memory Storage
chat_history = []

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

@app.post("/process-voice")
async def process_voice(text: str = Form(...)):
    try:
        user_input = text
        print(f"RECEIVED: {user_input}")
        
        ##PLAN with Context
        search_query = planner.extract_search_term(user_input, chat_history)
        
        ##RESEARCH
        research_data = researcher.perform_research(search_query)
        
        ##THINK & REPLY
        response = brain.think(research_data)
        
        ##UPDATE MEMORY
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})
        
        # Keep memory short to save tokens
        if len(chat_history) > 4:
            chat_history.pop(0)
            chat_history.pop(0)
            
        print(f"REPLY: {response}")
        return {"reply": response}
        
    except Exception as e:
        print(f"ERROR: {e}")
        return {"reply": f"System Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)