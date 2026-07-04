"""Upload markdown files to Gemini API."""

import os
import time
    
def upload_markdown_files_to_gemini(client, file_path, file_search_store):
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
def create_file_search_store(client, file_search_store_name):    
    file_search_store = client.file_search_stores.create(
        config = {
            'display_name': file_search_store_name,
            'embedding_model': 'models/gemini-embedding-2'
        }
    )
    
    # Upload markdown files to the file search store
    embedded_files_count = 0
    for file in os.listdir("articles_markdown"):
        if not file.endswith(".md"):
            continue
        
        file_path = os.path.join("articles_markdown", file)
        
        chunks_count = upload_markdown_files_to_gemini(client, file_path, file_search_store)
        embedded_files_count += 1
        
        print(f"Embedded file {embedded_files_count} - {chunks_count} chunks")
        
    print(f"File search store created: {file_search_store.name}") # The file search store is created and last indefinitely with a unique name
    
    return file_search_store
