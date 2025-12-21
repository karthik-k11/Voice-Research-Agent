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

#Search ArXiv, which is good for technical papers
def search_arxiv(query, max_results=2):
    try:
        print(f"🔎 Searching ArXiv for: {query}")
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for result in client.results(search):
            results.append(f"Title: {result.title}\nSummary: {result.summary[:200]}...") # Truncate for speed
            
        return "\n\n".join(results)
    except Exception as e:
        return f"ArXiv error: {e}"
    
#Search Web using DuckDuckGo
def search_web(query, max_results=3):
    try:
        print(f"🔎 Searching Web for: {query}")
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No web results found."

        formatted_results = [f"{r['title']}: {r['body']}" for r in results]
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Web search error: {e}"

#The tool calling function
def perform_research(topic):
    print(f"🚀 Starting research on: {topic}")
    
    # Gather data
    wiki_data = search_wiki(topic)
    arxiv_data = search_arxiv(topic)
    web_data = search_web(topic)
    
    # Combine into a single text block
    full_report = f"""
    === WIKIPEDIA ===
    {wiki_data}
    
    === ACADEMIC PAPERS (ArXiv) ===
    {arxiv_data}
    
    === WEB SEARCH ===
    {web_data}
    """
    
    return full_report