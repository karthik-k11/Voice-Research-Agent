#Imports
import os
from dotenv import load_dotenv
from groq import Groq

#Load environment variables from .env file
load_dotenv()

#Get the key securely
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing! Check your .env file.")

client = Groq(api_key=api_key)

def think(research_text):
    print("Brain is thinking (via Groq)...")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise voice assistant. Summarize the user's research data into 2-3 spoken sentences. Do not use asterisks, markdown, or bullet points."
                },
                {
                    "role": "user",
                    "content": f"Here is the research data found:\n{research_text}\n\nSummarize this for me."
                }
            ],
            model="llama3-8b-8192",  ##llm3
            temperature=0.6,
        )
        response = chat_completion.choices[0].message.content
        print(f"Brain Response: {response}")
        return response

    except Exception as e:
        print(f"Groq Error: {e}")
        return "I encountered an error connecting to my brain."