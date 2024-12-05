from googlesearch import search

# to search
query = "which one is the best apple?"
#results = search(query, num=10, stop=10, pause=2)
results = search(query)
for j in results:
    print(j)