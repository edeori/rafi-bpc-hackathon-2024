# Databricks notebook source
!pip install llama-index-embeddings-azure-openai
!pip install llama-index-llms-azure-openai
!pip install llama-index

dbutils.library.restartPython()


# COMMAND ----------

import os
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.core import load_index_from_storage
import logging
import sys


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

documents = SimpleDirectoryReader(input_files=["/Workspace/Users/vendel.mellau@raiffeisen.hu/Data/patterns.pdf"]).load_data()
index = VectorStoreIndex.from_documents(documents)

DOCS_DIR = "/Workspace/Users/vendel.mellau@raiffeisen.hu/Data"
PERSIST_DIR = "/Workspace/Users/vendel.mellau@raiffeisen.hu/Index"

if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)
docs = os.listdir(DOCS_DIR)
docs = [d for d in docs]
docs.sort()
print(f"Files in {DOCS_DIR}")
for doc in docs:
    print(doc)

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.response_synthesizers import get_response_synthesizer

splitter = SentenceSplitter(chunk_size=2048)

response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True
)

def create_retrieve_index(index_path, docs_path, index_type):
    if not os.path.exists(index_path):
        print(f"Creating Directory {index_path}")
        os.mkdir(index_path)
    if os.listdir(index_path) == []:
        print("Loading Documents...")
        documents = SimpleDirectoryReader(input_files=[f"{docs_path}/patterns.pdf"]).load_data()
        print("Creating Index...")
        index = index_type.from_documents(documents,
                                          show_progress=True,
                                          )
        print("Persisting Index...")
        index.storage_context.persist(persist_dir=index_path)
        print("Done!")
    else:
        print("Reading from Index...")
        index = load_index_from_storage(storage_context=StorageContext.from_defaults(persist_dir=index_path))
        print("Done!")
    return index

vectorstoreindex = create_retrieve_index(PERSIST_DIR, DOCS_DIR, VectorStoreIndex)

query_engine = vectorstoreindex.as_query_engine(retriever_mode="embedding",
                                                response_mode="compact",
                                                verbose=True)
response = query_engine.query("What is the book about?")
print(response)
