#Imports
import os
import re
from groq import Groq
from dotenv import load_dotenv

##Loading the API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Update function signature to accept history
def extract_search_term(user_input, history=[]):
    print(f"PLANNER: Analyzing intent for '{user_input}'...")
    
    # Format history into a string for the prompt
    context_str = ""
    if history:
        context_str = "PREVIOUS CONVERSATION:\n"
        for msg in history:
            context_str += f"- {msg['role'].upper()}: {msg['content']}\n"
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are a Context-Aware Search Optimizer.
                    
                    {context_str}
                    
                    TASK:
                    1. Analyze the user's NEW input.
                    2. Resolve pronouns ("he", "it", "they") using the PREVIOUS CONVERSATION.
                    3. Output ONLY the final search keywords.
                    
                    Example 1:
                    History: User asked about "Elon Musk".
                    Input: "How old is he?"
                    Output: Elon Musk age
                    
                    Example 2:
                    Input: "Tell me about Python"
                    Output: Python programming language
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
        
        # Safety Cleanup
        refined_query = re.sub(r'(Step \d:|Input:|Output:|Correction:)', '', raw_output, flags=re.IGNORECASE).strip()
        
        if not refined_query:
            refined_query = user_input

        print(f"OPTIMIZED QUERY: {refined_query}")
        return refined_query

    except Exception as e:
        print(f"Planner Error: {e}")
        return user_input