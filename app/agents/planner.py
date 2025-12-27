##Imports
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_search_term(user_input):
    print(f"PLANNER: Analyzing intent for '{user_input}'...")
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": """You are a Voice Query Expert & Search Optimizer.
                    
                    YOUR GOAL: 
                    The user is speaking to a Research AI. The input is a raw voice transcript that may contain "hallucinations" (words that sound similar but are wrong).
                    
                    STEP 1: CORRECT PHONETIC ERRORS based on context.
                    - "Reset" usually means "Research" in this context.
                    - "Generator" usually means "Generative" if followed by AI.
                    - "High Torch" usually means "PyTorch".
                    - "Face" usually means "Hugging Face".
                    
                    STEP 2: EXTRACT KEYWORDS for a search engine.
                    - Strip conversational fluff ("Tell me about").
                    - If specific product/company -> Add "news" or "specs".
                    
                    Example 1:
                    Input: "Reset the applications of generator AI"
                    Correction: "Research applications of Generative AI"
                    Output: Generative AI applications healthcare
                    
                    Example 2:
                    Input: "Tell me about the history of Rome"
                    Output: Roman Empire History
                    """
                },
                {
                    "role": "user", 
                    "content": user_input
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=50
        )
        
        refined_query = completion.choices[0].message.content.strip()
        print(f"OPTIMIZED QUERY: {refined_query}")
        return refined_query

    except Exception as e:
        print(f"Planner Error: {e}")
        return user_input