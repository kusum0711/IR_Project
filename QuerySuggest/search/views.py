from django.shortcuts import render
from elasticsearch import Elasticsearch
from .nltk_utils import get_wordnet_info
from .models import City
from django.db import DatabaseError

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")


def search_page(request):
    return render(request, "search/search_page.html")



def query_results(request):
    query = request.GET.get("q", "")

    # Validate the query
    if not query:
        return render(
            request,
            "search/query_results.html",
            {"query": query, "results": [], "nltk_info": None, "random_citys": []},
        )

    results = []
    expanded_query = []  # To collect original terms and their synonyms
    terms = query.split()  # Split the query into individual words

    try:
        # Expand query terms with synonyms
        for term in terms:
            synonyms_data = get_wordnet_info(term)  # Fetch WordNet info for the term
            print(f"\nSynonyms for '{term}':")
            print(f"  {synonyms_data}")  # Debug print to check the returned data

            synonyms = synonyms_data.get("synonyms")
            expanded_query.append(term)  # Add the original term
            expanded_query.extend(syn for syn in synonyms if syn not in expanded_query)  # Add unique synonyms

        # Construct the Elasticsearch query with boosted weights
        weight_original = 100
        weight_synonyms = 70

        # Print which synonyms are being used
        print("\nExpanded Query with Synonyms:")
        print(f"  Original Terms: {terms}")
        print(f"  Synonyms Expanded: {expanded_query}")

        should_clauses = [
            {"match": {"content": {"query": term, "boost": weight_original}}} for term in terms
        ]
        should_clauses += [
            {"match": {"content": {"query": synonym, "boost": weight_synonyms}}} for synonym in expanded_query if synonym not in terms
        ]

        # DEBUG: Print the constructed Elasticsearch query body
        body = {"query": {"bool": {"should": should_clauses}}}
        print("\nConstructed Elasticsearch Query Body:")
        print(f"  {body}")

        # Perform the search in Elasticsearch
        response = es.search(index="city_data", body=body, size=10)
        
        # DEBUG: Print the raw Elasticsearch response
        print("\nElasticsearch Response:")
        print(f"  {response}")
    except Exception as e:
        return render(
            request,
            "search/query_results.html",
            {
                "query": query,
                "results": [{"title": "Error", "content": str(e)}],
                "nltk_info": None,
                "random_citys": [],
            },
        )

    # Parse the search results
    if response["hits"]["total"]["value"] > 0:
        print(f"\nNumber of Results Found: {response['hits']['total']['value']}")
        for hit in response["hits"]["hits"]:
            results.append(
                {
                    "title": hit["_source"].get("city", "Unknown"),
                    "content": hit["_source"].get("content", ""),
                    "score": hit["_score"],  # Display the score (relevance score)
                }
            )
            print("\nMatching Document:")
            print(f"  Title: {hit['_source'].get('city', 'Unknown')}")
            print(f"  Content: {hit['_source'].get('content', '')}")
            print(f"  Relevance Score: {hit['_score']}")
    else:
        results.append({"title": "No results found", "content": ""})
        print("\nNo results found.")

    # Fetch NLTK information (synonyms, definitions, related terms)
    try:
        nltk_info = get_wordnet_info(query)  # Fetch data for the full query
        print(f"\nNLTK Info for query '{query}':")
        print(f"  {nltk_info}")  # Debugging the NLTK info
    except Exception as e:
        nltk_info = None
        print(f"\nError fetching NLTK information: {e}")

    # Fetch 3 random city names from the database
    try:
        random_citys = City.objects.order_by("?")[:3]
    except DatabaseError as e:
        random_citys = []
        print(f"\nError fetching citys from database: {e}")

    # Remove duplicates from expanded_query
    suggestions = set(expanded_query) - set(terms)

    return render(
        request,
        "search/query_results.html",
        {
            "query": query,
            "results": results,
            "nltk_info": nltk_info,
            "random_citys": random_citys,
            "suggestions": list(suggestions),
        },
    )


