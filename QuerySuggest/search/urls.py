from django.urls import path
from .views import search_page, query_results 

urlpatterns = [
    path('', search_page, name='search_page'),  # Search page
    path('results/', query_results, name='query_results'),  # Query results page
]
