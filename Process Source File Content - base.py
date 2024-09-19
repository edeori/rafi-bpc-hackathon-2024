# Databricks notebook source
# MAGIC %pip install openai PyPDF2 python-docx

# COMMAND ----------

import os
import openai
from openai import OpenAI
from openai import AzureOpenAI

openai.api_type = "azure"
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_version = "2023-07-01-preview"
openai.api_base = "https://chatgpt-summarization.openai.azure.com/"

llm_model_name = "gpt-4o"
llm_deploy_name = "model-gpt4o"

client = AzureOpenAI(api_key=openai.api_key,
                     api_version=openai.api_version,
                     azure_endpoint=openai.api_base,
                     )

# COMMAND ----------

import PyPDF2

uploaded_file_path = "/Workspace/Users/marton.ferenczi@raiffeisen.hu/rafi-bpc-hackathon-2024/example-pdf.pdf"

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Extract text from the uploaded PDF
document_text = extract_text_from_pdf(uploaded_file_path)
#print(document_text[:500])  # Preview first 500 characters


# COMMAND ----------

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

# Example of querying the document content
question = "What is the main topic of the document?"
answer = chat_with_openai(document_text, question)
print(f"Answer: {answer}")

