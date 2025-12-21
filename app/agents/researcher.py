#Necessary imports
import wikipedia
import arxiv
from duckduckgo_search import DDGS

#Search Wikipedia function
def search_wiki(query, sentences=3):
    try:
        print(f"🔎 Searching Wikipedia for: {query}")
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except Exception as e:
        return f"Wikipedia error: {e}"