# app/agents/researcher.py
##Imports
import wikipedia
import arxiv
from ddgs import DDGS

##Search Wikipedia
def search_wiki(query):
    print(f"🔎 Searching Wikipedia for: {query}")
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return "No Wikipedia page found."
        summary = wikipedia.summary(search_results[0], sentences=4)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Wikipedia topic ambiguous: {e.options[:3]}"
    except Exception as e:
        return f"Wikipedia error: {e}"

##Search ArXiv
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

##Search Web
def search_web(query, max_results=3):
    print(f"Searching Web for: {query}")
    
    if "news" in query.lower() or "latest" in query.lower() or "today" in query.lower():
        print(f"NEWS MODE ACTIVATED: Switching to DDGS News Search...")
        try:
            #DDGS().news() returns specific articles, not homepages!
            results = list(DDGS().news(keywords=query, region='wt-wt', max_results=max_results))
            if not results:
                return "No news articles found."
            
            formatted = [f"News ({r['title']}): {r['body']} (Source: {r['source']})" for r in results]
            return "\n\n".join(formatted)
        except Exception as e:
            return f"News search error: {e}"
    else:
        # Standard Text Search for non-news queries
        try:
            results = DDGS().text(query, region='wt-wt', max_results=max_results, timelimit='y')
            if not results:
                return "No web results found."
            formatted = [f"Web ({r['title']}): {r['body']}" for r in results]
            return "\n\n".join(formatted)
        except Exception as e:
            return f"Web search error: {e}"

##The main function
def perform_research(topic):
    wiki = search_wiki(topic)
    web = search_web(topic)
    return f"TOPIC: {topic}\n\nSOURCE 1: WIKIPEDIA\n{wiki}\n\nSOURCE 2: WEB\n{web}"