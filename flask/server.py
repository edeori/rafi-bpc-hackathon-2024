# Databricks notebook source
!pip install openai PyPDF2 python-docx
!pip install -qU openai
dbutils.library.restartPython()

# COMMAND ----------

from flask import Flask, request
#from flask_cors import CORS
import requests
from dbruntime.databricks_repl_context import get_context
import os
import openai
from openai import OpenAI
from openai import AzureOpenAI
import PyPDF2

#os.environ["OPENAI_API_KEY"] = ""
openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = "https://chatgpt-summarization.openai.azure.com/"

llm_model_name = "gpt-4o"
llm_deploy_name = "model-gpt4o"

client = AzureOpenAI(api_key="OPENAPI_KEY",
                     api_version=openai.api_version,
                     azure_endpoint=openai.api_base,
                     )

uploaded_file_path = "/Workspace/Users/peter.zilahi@raiffeisen.hu/rafi-bpc-hackathon-2024/example-pdf.pdf"

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

def chat_with_openai(document_content, question):
    prompt=f"The following is content from a document:\n{document_content}\n\nAnswer the following question based on this document:\n{question}"

    response = client.chat.completions.create(
        model=llm_deploy_name,
        messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}"},
    ],
    )
    return response.choices[0].message.content

app = Flask('rambo_zero_shot')

@app.route("/", methods=['POST'])
def question():
    #ide jön a app
     body = request.json
     print(body)
     # Extract text from the uploaded PDF
     document_text = extract_text_from_pdf(uploaded_file_path)
     #print(document_text[:500])  # Preview first 500 characters
     answer = chat_with_openai(document_text, body.get('question'))
     return answer

app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
