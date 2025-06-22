# import os
# from elasticsearch import Elasticsearch

# # Connect to Elasticsearch
# es = Elasticsearch("http://localhost:9200")

# # Index name in Elasticsearch
# INDEX_NAME = "city_data"

# # Function to delete the existing index (if needed)
# def delete_index():
#     if es.indices.exists(index=INDEX_NAME):
#         es.indices.delete(index=INDEX_NAME)
#         print(f"Index '{INDEX_NAME}' deleted.")

# # Function to create an index
# def create_index():
#     if not es.indices.exists(index=INDEX_NAME):
#         es.indices.create(index=INDEX_NAME)
#         print(f"Index '{INDEX_NAME}' created.")
#     else:
#         print(f"Index '{INDEX_NAME}' already exists.")

# # Function to index data
# def index_data():
#     data_folder = "data"
#     for file_name in os.listdir(data_folder):
#         if file_name.endswith(".txt"):
#             city_name = os.path.splitext(file_name)[0].lower()  # Normalize to lowercase
#             with open(os.path.join(data_folder, file_name), "r", encoding="utf-8") as file:
#                 content = file.read()
#                 document = {
#                     "city": city_name,
#                     "content": content,
#                 }
#                 # Index the document
#                 es.index(index=INDEX_NAME, document=document)
#                 print(f"Indexed: {city_name}")

# if __name__ == "__main__":
#     delete_index()  # Optional, if you want to delete and reindex from scratch
#     create_index()
#     index_data()

import os
from elasticsearch import Elasticsearch
from PyPDF2 import PdfReader  # Importing PyPDF2 for PDF parsing

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Index name in Elasticsearch
INDEX_NAME = "city_data"

# Function to delete the existing index (if needed)
def delete_index():
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Index '{INDEX_NAME}' deleted.")

# Function to create an index
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

# Helper function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()  # Extract text from each page
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF '{pdf_path}': {e}")
        return ""

# Function to index data
def index_data():
    # data_folder = "../data"
    data_folder = "../data"
    for file_name in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file_name)
        city_name = os.path.splitext(file_name)[0].lower()  # Normalize to lowercase

        if file_name.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif file_name.endswith(".pdf"):
            content = extract_text_from_pdf(file_path)
        else:
            print(f"Skipping unsupported file: {file_name}")
            continue

        # Only index if content was successfully extracted
        if content:
            document = {
                "city": city_name,
                "content": content,
            }
            # Index the document
            es.index(index=INDEX_NAME, document=document)
            print(f"Indexed: {city_name}")
        else:
            print(f"No content to index for: {file_name}")

if __name__ == "__main__":
    delete_index()  # Optional, if you want to delete and reindex from scratch
    create_index()
    index_data()
