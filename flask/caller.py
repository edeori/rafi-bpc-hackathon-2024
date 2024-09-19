# Databricks notebook source
# Databricks notebook source
!pip install openai PyPDF2 python-docx
!pip install -qU openai
dbutils.library.restartPython()

# COMMAND ----------

import requests
# from flask import request
from dbruntime.databricks_repl_context import get_context
import pandas as pd
import os

ctx = get_context()
port = 5001
url = f"https://{ctx.browserHostName}/driver-proxy-api/o/0/{ctx.clusterId}/{port}"
print(url)
#'https://rbi-apex-hu01-ws01.cloud.databricks.com/driver-proxy-api/o/0/0826-102917-1qur3pd6/5001'

header = { #ez az általam generált token, ezzel megy
    'Content-Type': 'application/json',
    'Authorization': 'xxx' 
}
#query the endpoint:

query = "file/kérdés"

r = requests.post(url, headers=header, json=query)

print(r)

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
import csv
import json
from docx import Document
from bs4 import BeautifulSoup

#os.environ["OPENAI_API_KEY"] = ""
openai.api_type = "azure"
openai.api_version = "2023-07-01-preview"
openai.api_base = "https://chatgpt-summarization.openai.azure.com/"

llm_model_name = "gpt-4o"
llm_deploy_name = "model-gpt4o"
document_upload = True
chat_history = []
app_data = {
    'file_text': ""
}

client = AzureOpenAI(api_key="a6c57e86dd424bb3aad0aeec06ef4777",
                     api_version=openai.api_version,
                     azure_endpoint=openai.api_base,
                     )

def extract_text_from_file(file, file_extension):
    text = ""

    if file_extension in ['txt', 'md', 'csv']:
        # Plain text, markdown, or CSV files can be read directly as text
        text = file.read().decode('utf-8')

    elif file_extension == 'pdf':
        # Extract text from PDF
        print(file)
        reader = PyPDF2.PdfReader(file)
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()

    elif file_extension == 'json':
        # Load JSON and pretty-print it as text
        json_content = json.load(file)
        text = json.dumps(json_content, indent=4)

    elif file_extension == 'xml':
        # Parse XML and return pretty-printed content
        soup = BeautifulSoup(file, 'xml')
        text = soup.prettify()

    elif file_extension == 'html':
        # Parse HTML and extract visible text
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text(separator="\n")

    elif file_extension == 'docx':
        # Extract text from a Word document
        doc = Document(file)
        for para in doc.paragraphs:
            text += para.text + '\n'
    return text

def chat_with_openai(document_content, question):
    # prompt=f"The following is content from a document:\n{document_content}\n\nAnswer the following question based on this document:\n{question}"

    # response = client.chat.completions.create(
    #     model=llm_deploy_name,
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": f"{prompt}"},
    #     ],
    # )
    # return response.choices[0].message.content

    global document_upload
    # Kezdetben a dokumentum tartalmát is beillesztjük a promptba.
    if document_upload:
        chat_history.append(
            {"role": "system", "content": f"The following is content from a document:\n{document_content}"}
        )
        document_upload = False

    # Hozzáadjuk az új kérdést a felhasználótól a chat történethez.
    chat_history.append({"role": "user", "content": question})

    # OpenAI API hívás a teljes történettel.
    response = client.chat.completions.create(
        model=llm_deploy_name,
        messages=chat_history,
    )
    print(response)
    # Választ hozzáadjuk a chat történethez, így legközelebb is elérhető lesz.
    assistant_reply = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_reply})

    return assistant_reply

app = Flask('rambo_zero_shot')

@app.route("/document", methods=['POST'])
def document_upload():
    print("INCOMING FILE REQUEST")
    uploaded_file = request.files.get('file')

    if uploaded_file:
        global document_upload
        document_upload = True
        # Get the file extension
        file_extension = uploaded_file.filename.split('.')[-1].lower()
        print("file_extension: " + file_extension)
        # Check if the file type is allowed
        allowed_file_types = ["txt", "md", "json", "xml", "csv", "pdf", "docx", "html"]
        if file_extension not in allowed_file_types:
            return {"error": f"Unsupported file type: {file_extension}"}, 400

        # Extract the text from the file
        try:
            print("The file is: " + uploaded_file.filename)
            app_data['file_text'] = extract_text_from_file(uploaded_file, file_extension)
            return {"message": "File processed successfully!"}, 200
        except Exception as e:
            return {"error": f"Failed to process file: {str(e)}"}, 500
    else:
        return {"error": "No file uploaded"}, 400

@app.route("/", methods=['POST'])
def question():
    #ide jön a app
    body = request.json
    print(body)
    file_text = app_data.get('file_text')
    print(file_text)
    answer = chat_with_openai(file_text, body.get('question'))
    return answer

app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)

