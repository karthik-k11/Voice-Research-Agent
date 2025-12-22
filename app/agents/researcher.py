#Necessary imports 
import wikipedia
import arxiv
from duckduckgo_search import DDGS

def search_wiki(query):
    print(f"Searching Wikipedia for: {query}")
    try:
        #Search for titles first
        search_results = wikipedia.search(query)
        if not search_results:
            return "No Wikipedia page found."
        
        #Get the summary of the first result
        summary = wikipedia.summary(search_results[0], sentences=4)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Wikipedia topic ambiguous: {e.options[:3]}"
    except Exception as e:
        return f"Wikipedia error: {e}"

def search_arxiv(query, max_results=2):
    print(f"Searching ArXiv for: {query}")
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = []
        for result in client.results(search):
            results.append(f"Paper: {result.title}\nAbstract: {result.summary[:200]}...")
        return "\n\n".join(results) if results else "No ArXiv papers found."
    except Exception as e:
        return f"ArXiv error: {e}"

def search_web(query, max_results=3):
    print(f"Searching Web for: {query}")
    try:
        #forces English results, avoiding location bias
        results = DDGS().text(query, region='wt-wt', max_results=max_results)
        if not results:
            return "No web results found."
        formatted = [f"Web: {r['title']} - {r['body']}" for r in results]
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Web search error: {e}"

def perform_research(topic):

    wiki = search_wiki(topic)
    web = search_web(topic)
    
    return f"""
    TOPIC: {topic}
    
    SOURCE 1: WIKIPEDIA
    {wiki}
    
    SOURCE 2: WEB SEARCH
    {web}
    """