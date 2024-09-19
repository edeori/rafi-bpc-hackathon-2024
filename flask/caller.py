# Databricks notebook source
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
