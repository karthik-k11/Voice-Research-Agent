##Imports
import wikipedia
import arxiv
from ddgs import DDGS
import warnings

##Search wikipedia
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

def search_wiki(query):
    print(f"Searching Wikipedia for: {query}")
    try:
        # Simple Wikipedia fetch
        search_results = wikipedia.search(query)
        if not search_results:
            return "No Wikipedia page found."
        summary = wikipedia.summary(search_results[0], sentences=4, auto_suggest=False)
        return summary
    except Exception as e:
        return f"Wikipedia error: {e}"

def search_arxiv(query, max_results=2):
    print(f"Searching ArXiv for: {query}")
    try:
        # Simple Academic Paper fetch
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
        results = []
        for result in client.results(search):
            results.append(f"Paper: {result.title}\nAbstract: {result.summary[:200]}...")
        return "\n\n".join(results) if results else "No ArXiv papers found."
    except Exception as e:
        return f"ArXiv error: {e}"

##Web search
def search_web(query, max_results=3):
    print(f"Searching Web for: {query}")
    try:
        ##Text search using DDGS
        results = DDGS().text(query, region='wt-wt', max_results=max_results)
        
        if not results:
            return "No web results found."
            
        formatted = [f"Web: {r['title']} - {r['body']}" for r in results]
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Web search error: {e}"

##End Function
def perform_research(topic):
    wiki = search_wiki(topic)
    web = search_web(topic)
    arxiv_data = search_arxiv(topic)

    return {
        "WIKIPEDIA": wiki,
        "WEB": web,
        "ARXIV": arxiv_data
    }