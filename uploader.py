"""Upload markdown files to Gemini API."""

import os
import time
    
def upload_markdown_file_to_gemini(client, file_path, file_search_store):
    # Gemini automatically does the chunkings and indexing
    operation = client.file_search_stores.upload_to_file_search_store(
        file = file_path,
        file_search_store_name = file_search_store.name,
        config = {
            'display_name': file_path.split("/")[-1],  # Use the file name as the display name
        }
    )
    
    while not operation.done:
        time.sleep(4)
        operation = client.operations.get(operation.name)
        
    # calc the number of chunks created for the uploaded file
    documents_in_store = client.file_search_stores.documents.list(
        parent=file_search_store.name
    )
    chunks_count = 0
    for doc in documents_in_store:
        if doc.source == file_path:
            chunks_count += 1
    
    return chunks_count
        

# Create vector store for RAG
def _create_file_search_store(client, file_search_store_name):    
    file_search_store = client.file_search_stores.create(
        config = {
            'display_name': file_search_store_name,
            'embedding_model': 'models/gemini-embedding-2'
        }
    )
    
    print(f"Created new Gemini File Search store: {file_search_store.name}") # Each store has a unique name
    

# File Search Store is created only once
def get_or_create_file_search_store(client, display_name):
    stores = client.file_search_stores.list()

    for store in stores:
        if store.display_name == display_name:
            return store

    return _create_file_search_store(client, display_name)