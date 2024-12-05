from googlesearch import search

# def get_snippets(query, num_results=10):
#     try:
#         # Perform the search
#         results = search(query, num=num_results, stop=num_results, pause=2)
        
#         snippets = []
#         for result in results:
#             snippets.append(result)
        
#         return snippets
#     except Exception as e:
#         print("Error:", e)
#         return []

from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_snippets(query, num_results=10):
    try:
        # Perform the search
        search_results = search(query, num=num_results, stop=num_results, pause=2)
        
        snippets = []
        for url in search_results:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Get the first <p> tag's text as a snippet (this is a basic approach and might not always be accurate)
                p_tag = soup.find('p')
                if p_tag:
                    snippets.append(p_tag.text)
        
        return snippets
    except Exception as e:
        print("Error:", e)
        return []


# Example usage
query = "Python programming"
snippets = get_snippets(query)
for idx, snippet in enumerate(snippets, 1):
    print(f"{idx}. {snippet}\n")