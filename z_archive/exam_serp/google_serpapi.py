#from serpapi import GoogleSearch
from serpapi import search 

def query_serpapi(question):
    # Define your SerpAPI API key
    api_key = "27b1750ec8be8989730f92bc3dd95bc221eaafbdd12e3aa5310159e5b5e5c0e5"

    # Set up the search parameters
    params = {
        "q": question,  # The question you want to query
        "location": "United States",  # You can change this to your desired location
        "hl": "en",  # Language
        "gl": "us",  # Geolocation
        "api_key": api_key
    }

    # Perform the search
    serp_result = search(params)
    results = serp_result.as_dict()

    # Extract and return the organic results
    organic_results = results.get("organic_results", [])
    return organic_results

def search_by_query(question_to_search):
    organic_results = query_serpapi(question_to_search)
    print("len of result", len(organic_results))
    for idx, result in enumerate(organic_results, 1):
        print(f"{idx}. {result['title']}\n{result['snippet']}\n")
    return organic_results


if __name__ == "__main__":
    # Test the function
    #question_to_search = "What is the capital of France?"
    question_to_search = "法国的首都有什么好玩的?"
    search_by_query(question_to_search)



