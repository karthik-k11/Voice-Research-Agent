##Imports
import os
import re
from groq import Groq
from dotenv import load_dotenv

##Loading API Key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_search_term(user_input, history=[]):
    print(f"PLANNER: Analyzing intent for '{user_input}'...")
    
    # Only use the LAST exchange to avoid confusing the AI with old topics
    short_history = history[-2:] if history else []
    
    context_str = ""
    if short_history:
        context_str = "PREVIOUS CONVERSATION (For context resolving ONLY):\n"
        for msg in short_history:
            role = "User" if msg['role'] == "user" else "Assistant"
            content = msg['content'][:100] # Truncate to keep it focused
            context_str += f"- {role}: {content}...\n"
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are a Search Query Generator.
                    
                    {context_str}
                    
                    INSTRUCTIONS:
                    1. Look at the User's NEW INPUT.
                    2. If the user refers to the previous topic (e.g., "How old is HE?"), use the context to replace "HE".
                    3. If the user changes the topic (e.g., "Tell me about Tiger"), IGNORE the context and just output "Tiger".
                    4. CRITICAL: Output the final query inside brackets: [QUERY: your keywords here]
                    5. Do NOT output explanations.
                    
                    Example 1 (New Topic):
                    Input: "Tell me about Tigers"
                    Output: [QUERY: Tiger animal facts]
                    
                    Example 2 (Follow-up):
                    History: User asked about Elon Musk.
                    Input: "How old is he?"
                    Output: [QUERY: Elon Musk age]
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
        
        raw_output = completion.choices[0].message.content.strip()
        
        match = re.search(r'\[QUERY:\s*(.*?)\]', raw_output, re.IGNORECASE)
        
        if match:
            refined_query = match.group(1).strip()
            print(f"OPTIMIZED QUERY: {refined_query}")
            return refined_query
        else:
            print(f"PLANNER MALFORMED: '{raw_output}' -> Falling back to raw input.")
            return user_input

    except Exception as e:
        print(f"Planner Error: {e}")
        return user_input