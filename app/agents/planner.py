##Imports
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_search_term(user_input):
    print(f"PLANNER: Refining query for '{user_input}'...")
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    #UPDATED PROMPT
                    "content": """You are a Search Query Optimizer. 
                    Your job is to generate the BEST search keywords to get accurate data.
                    
                    RULES:
                    1. Strip conversational fluff ("Tell me about", "I want to know").
                    2. If the user asks for "rumors" or "leaks", change it to "latest news" or "specs" (so we find launched products too).
                    3. Output ONLY the keywords.
                    
                    Example:
                    Input: 'What are the rumors about iPhone 17'
                    Output: iPhone 17 latest news specs
                    
                    Input: 'History of Rome'
                    Output: Roman Empire History"""
                },
                {
                    "role": "user", 
                    "content": user_input
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=30
        )
        
        refined_query = completion.choices[0].message.content.strip()
        print(f"OPTIMIZED QUERY: {refined_query}")
        return refined_query

    except Exception as e:
        print(f"Planner Error: {e}")
        return user_input