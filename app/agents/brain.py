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
                    "content": f"""Current Date: {today}. 
                    You are a highly credible Voice Research Assistant. 
                    
                    YOUR TASKS:
                    1. Synthesize the provided research data into a clear, spoken summary.
                    2. ATTRIBUTION: You MUST mention the source name for key facts (e.g., "According to Wikipedia...", "Research suggests...", "Sources like TechCrunch state...").
                    3. DISCLAIMER: If the topic is Medical, Financial, or Legal, start with "I am an AI, not a professional, but data suggests..."
                    4. Keep it under 4 sentences.
                    """
                },
                {
                    "role": "user",
                    "content": f"Here is the research data found:\n{research_text}\n\nSynthesize this answer."
                }
            ],
            model="llama-3.1-8b-instant", 
            temperature=0.6,
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        return "Error connecting to brain."