# Databricks notebook source
import base64
import os

def save_file_to_dbfs(filename, file_content_base64):
    file_content = base64.b64decode(file_content_base64)
    file_path = f"/dbfs/FileStore/{filename}"
    
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    return file_path  # Return the DBFS path for further processing

