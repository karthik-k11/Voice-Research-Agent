##Necessary imports
import os
from groq import Groq
from dotenv import load_dotenv

##Loading the groq API
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_search_term(user_input):
    print(f"PLANNER: Refining query for '{user_input}'...")
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Search Query Optimizer. Your job is to extract the main topic from the user's voice command for a search engine (Wikipedia/Google). Output ONLY the search keywords. No intro, no quotes.\n\nExample:\nInput: 'Tell me the history of the Roman Empire'\nOutput: Roman Empire History\n\nInput: 'What are the rumors about iPhone 17'\nOutput: iPhone 17 release date rumors"
                },
                {
                    "role": "user", 
                    "content": user_input
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0, # 0 means "be exact, don't be creative"
            max_tokens=20
        )

        refined_query = completion.choices[0].message.content.strip()
        print(f"✨ OPTIMIZED QUERY: {refined_query}")
        return refined_query