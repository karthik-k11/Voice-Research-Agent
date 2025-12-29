##Imports
import os
import re 
from groq import Groq
from dotenv import load_dotenv

##Loading API Key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_search_term(user_input):
    print(f"PLANNER: Analyzing intent for '{user_input}'...")
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": """You are a Keyword Extractor.
                    
                    TASK:
                    1. Analyze the user's voice input.
                    2. Correct any phonetic errors (e.g. "Reset" -> "Research").
                    3. Strip conversational fluff ("Tell me about", "I want to know").
                    4. CRITICAL: Output ONLY the final search keywords. DO NOT write "Step 1", "Correction:", or explanations.
                    
                    Examples:
                    Input: "Reset the applications of generator AI"
                    Output: Generative AI applications healthcare
                    
                    Input: "Tell me about Python"
                    Output: Python programming language
                    
                    Input: "Compare React and Angular"
                    Output: React vs Angular framework comparison
                    """
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
        
        raw_output = completion.choices[0].message.content.strip()
        
        refined_query = re.sub(r'(Step \d:|Input:|Output:|Correction:)', '', raw_output, flags=re.IGNORECASE).strip()
        
        if not refined_query:
            refined_query = user_input

        print(f"OPTIMIZED QUERY: {refined_query}")
        return refined_query

    except Exception as e:
        print(f"Planner Error: {e}")
        return user_input