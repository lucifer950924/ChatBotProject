from ddgs import DDGS

def searchwithDUckDuckGO(query:str) -> str:
    '''
    Search the web for up-to-date information

    Args:
        query : Seraches for the query

    Returns:
        results : returns the search results for the query
    '''

    with DDGS() as ds:
        results = list(ds.text(query,max_results=2))

        return str(results[0]['body']) 



