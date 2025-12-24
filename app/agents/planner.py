##Necessary imports
import os
from groq import Groq
from dotenv import load_dotenv

##Loading the groq API
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))