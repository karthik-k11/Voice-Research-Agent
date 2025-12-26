##Imports
import os
import datetime
from dotenv import load_dotenv
from groq import Groq

##Loading API  Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def think(research_text):
    ##Get Today's Date
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    print(f"Brain is thinking (Context Date: {today})...")
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    #INJECT DATE HERE
                    "content": f"Current Date: {today}. You are a concise voice assistant. Summarize the user's research data relative to today's date. Ignore outdated rumors if newer info is present."
                },
                {
                    "role": "user",
                    "content": f"Here is the research data found:\n{research_text}\n\nSummarize this for me."
                }
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.6,
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        return "Error connecting to brain."