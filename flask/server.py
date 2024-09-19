# Databricks notebook source
from flask import Flask, request
#from flask_cors import CORS
import requests
from dbruntime.databricks_repl_context import get_context

app = Flask('rambo_zero_shot')

@app.route("/", methods=['POST'])
def zero_shot_api():
    #ide jön a app
     
     return "Chatbot válasz"

#ez létrehozza az endpointot és innentől hívható, én notebookban indítottam és innentől a notebook végig "busy", szóval egy másikból lehet meghívni 
app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
