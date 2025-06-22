from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
query = "Paris"

# Search the index
response = es.search(index="city_data", query={"match": {"content": query}})
for hit in response["hits"]["hits"]:
    print(f"Found: {hit['_source']}")
