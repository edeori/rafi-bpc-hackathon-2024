# Databricks notebook source
from flask import Flask, request
#from flask_cors import CORS
import requests
from dbruntime.databricks_repl_context import get_context
import os
import openai
from openai import OpenAI
from openai import AzureOpenAI

#os.environ["OPENAI_API_KEY"] = ""
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

def chat_with_openai(question):
    chat_completion = client.chat.completions.create(
        model=llm_deploy_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{question}"},
        ],
    )
    answer = chat_completion.choices[0].message.content
    print(answer)
    return answer

app = Flask('rambo_zero_shot')

@app.route("/", methods=['POST'])
def question():
    #ide jön a app
     body = request.json
     answer = chat_with_openai(body["question"])
     return answer

app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
