# Databricks notebook source
# MAGIC %pip install openai PyPDF2 python-docx

# COMMAND ----------

import os
import openai
from openai import OpenAI
from openai import AzureOpenAI

# COMMAND ----------

os.environ["OPENAI_API_KEY"] = "a6c57e86dd424bb3aad0aeec06ef4777"
#openai.api_key = os.environ["OPENAI_API_KEY"]

# COMMAND ----------

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

text = f"""
This is some text about working with databricks.
"""

prompt = f"""
What is about the {text}?
"""

chat_completion = client.chat.completions.create(
    model=llm_deploy_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{prompt}"},
    ],
)

print(chat_completion.choices[0].message.content)
