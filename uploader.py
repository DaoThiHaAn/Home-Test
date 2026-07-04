"""Upload markdown files to Gemini API."""

import time
    
def upload_markdown_file_to_gemini(client, file_path, file_search_store, file_number=0):
    # Gemini automatically does the chunkings and indexing
    operation = client.file_search_stores.upload_to_file_search_store(
        file = file_path,
        file_search_store_name = file_search_store.name,
        config = {
            'display_name': file_path.split("/")[-1],  # Use the file name as the display name
            "mime_type": "text/markdown",
        }
    )
    
    while not operation.done:
        time.sleep(4)
        operation = client.operations.get(operation)
        
    print(f"File {file_number}: {file_path} is embedded")
        
        

# Create vector store for RAG
def _create_file_search_store(client, file_search_store_name):    
    file_search_store = client.file_search_stores.create(
        config = {
            'display_name': file_search_store_name,
            'embedding_model': 'models/gemini-embedding-2'
        }
    )
    
    time.sleep(5)  # Wait for the store to be fully created
    print(f"Created new Gemini File Search store: {file_search_store.name}") # Each store has a unique name
    return file_search_store
    

# File Search Store is created only once
def get_or_create_file_search_store(client, display_name):
    stores = client.file_search_stores.list()

    for store in stores:
        if store.display_name == display_name:
            return store

    return _create_file_search_store(client, display_name)