# Databricks notebook source
!pip install openai PyPDF2 python-docx
!pip install -qU openai
dbutils.library.restartPython()

# COMMAND ----------

!pip install llama-index-embeddings-azure-openai
!pip install llama-index-llms-azure-openai
!pip install llama-index
!pip install openai PyPDF2 python-docx
!pip install -qU openai

dbutils.library.restartPython()

# COMMAND ----------

from flask import Flask, request
import os
import openai
from openai import OpenAI
from openai import AzureOpenAI
import PyPDF2
import json
import base64
from docx import Document
from bs4 import BeautifulSoup

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.core import Settings

api_key = ""
azure_endpoint = "https://chatgpt-summarization.openai.azure.com/"
api_version = "2024-02-15-preview"

llm = AzureOpenAI(
    model="gpt-4o",
    deployment_name="model-gpt4o",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="model-text-embedding-ada-002",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

from llama_index.core import Settings
Settings.llm = llm
Settings.embed_model = embed_model

app_data = {'file_text': ""}

# Save the file to DBFS
def save_file_to_dbfs(filename, file_content):
    print("save file to dbfs")
    
    # Define the path in DBFS
    file_path = f"/dbfs/FileStore/{filename}"
    print(f"File path: {file_path}")
    
    # Ensure content is not None
    if not file_content:
        print("Error: File content is empty")
        return None
    
    print(f"File content size: {len(file_content)} bytes")
    
    try:
        # Save the binary content directly to the file
        with open(file_path, "wb") as f:
            f.write(file_content)  # Write the raw binary content
        print(f"File saved successfully at {file_path}")
    except Exception as e:
        print(f"Error saving file to DBFS: {str(e)}")
        raise e  # Rethrow the exception so it can be caught later

    return file_path

from os import listdir

# Index files using LlamaIndex
def index_files_in_llama(file_paths):
    print("index_files_in_llama")

    print(listdir("/dbfs/FileStore"))
    
    # Ensure the directory exists and is accessible
    input_dir = "/dbfs/FileStore"  # Correct path for accessing files in DBFS via Python
    #input_dir_files = listdir("/dbfs/FileStore")
    #print(f"Loading documents {input_dir_files} from directory: /dbfs/FileStore")
    print(f"Loading documents from directory: {input_dir}")

    try:
        # Load files from DBFS using SimpleDirectoryReader
        documents = SimpleDirectoryReader(input_dir=input_dir).load_data()
        #documents = SimpleDirectoryReader(input_files=["/dbfs/FileStore/example-pdf.pdf"]).load_data()
        print(f"Loaded {len(documents)} documents")
    except Exception as e:
        #print(f"Error loading documents {input_dir_files} from /dbfs/FileStore: {str(e)}")
        print(f"Error loading documents from {input_dir}: {str(e)}")
        return None
    
    # Create a VectorStoreIndex (LlamaIndex) to index the files
    try:
        # Optionally save the index to disk (for future use)
        index = VectorStoreIndex.from_documents(documents,
                                          show_progress=True,
                                          )
        print("Index created successfully")
        print("Persisting Index...")
        index.storage_context.persist(persist_dir="/dbfs/FileStore/docstore.json")
        print("Index saved to disk")
    except Exception as e:
        print(f"Error creating or saving index: {str(e)}")
        return None
    
    return index

def handle_request(question):
    print("Handling request:", question)
    
    # Set up the storage context for loading the index
    #storage_context = StorageContext.from_defaults(persist_dir="/dbfs/FileStore")
    vectorstoreindex = load_index_from_storage(storage_context=StorageContext.from_defaults(persist_dir="/dbfs/FileStore/docstore.json"))
    query_engine = vectorstoreindex.as_query_engine(retriever_mode="embedding",
                                                response_mode="compact",
                                                verbose=True)

    # OpenAI API hívás a teljes történettel.
    
    response = query_engine.query(question)
    print(response)
    
    return str(response).encode('utf-8')


# Flask App
app = Flask('llama_openai_app')

# API for document upload
@app.route("/document", methods=['POST'])
def document_upload():
    uploaded_file = request.files.get('file')  # This is a FileStorage object
    if uploaded_file:
        file_extension = uploaded_file.filename.split('.')[-1].lower()
        allowed_file_types = ["pdf", "txt", "docx"]
        
        if file_extension not in allowed_file_types:
            return {"error": f"Unsupported file type: {file_extension}"}, 400
        
        try:
            # Read the binary content of the uploaded file
            file_content = uploaded_file.read()  # This reads the file as bytes
            
            # Now pass the binary content to save_file_to_dbfs
            file_path = save_file_to_dbfs(uploaded_file.filename, file_content)
            print(f"File saved at: {file_path}")
            
            # Further processing (e.g., indexing the file) can go here
            index_files_in_llama(file_path)
            
            return {"message": "File processed successfully!"}, 200
        except Exception as e:
            return {"error": f"Failed to process file: {str(e)}"}, 500
    else:
        return {"error": "No file uploaded"}, 400

# API for querying the index
@app.route("/", methods=['POST'])
def question():
    body = request.json
    answer = handle_request(body.get('question'))
    return answer

# Run the Flask app
app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
