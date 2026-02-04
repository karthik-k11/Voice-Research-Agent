##Necessary Imports
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Request
from app.agents import planner, researcher, brain, gatekeeper
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

##Helper function
def get_chat_history(request: Request):
    if not hasattr(request.state, "chat_history"):
        request.state.chat_history = []
    return request.state.chat_history


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")

@app.post("/process-voice")
async def process_voice(
    request: Request,
    text: str = Form(...)
):
    try:
        chat_history = get_chat_history(request)

        user_input = text
        print(f"RECEIVED: {user_input}")

        search_query = planner.extract_search_term(user_input, chat_history)

        if not search_query or len(search_query.strip()) < 5:
            fallback = "Could you please be more specific?"

            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": fallback})

            return {
                "reply": fallback,
                "metadata": {
                    "status": "clarification_required"
                }
            }

        research_payload = researcher.perform_research(search_query)

        allowed, confidence = gatekeeper.allow_response(research_payload)

        if not allowed:
            fallback = (
                "I don’t have enough reliable information to answer that confidently. "
                "Could you clarify or narrow the question?"
            )

            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": fallback})

            return {
                "reply": fallback,
                "metadata": {
                    "confidence": confidence,
                    "status": "blocked_by_gatekeeper"
                }
            }

        combined_text = "\n\n".join(
            f"{k}:\n{v}" for k, v in research_payload.items()
        )

        response = brain.think(combined_text)

        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})

        if len(chat_history) > 4:
            chat_history.pop(0)
            chat_history.pop(0)

        return {
            "reply": response,
            "metadata": {
                "confidence": confidence,
                "status": "approved"
            }
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {"reply": "System error occurred."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)