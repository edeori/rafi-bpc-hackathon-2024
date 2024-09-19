import streamlit as st
import requests

# Streamlit UI for the chatbot
st.title("Databricks-Powered OpenAI Chatbot")

st.write("Ask a question to the chatbot:")

# Input field for the user's Bearer token
token = st.text_input("Bearer Token:", type="password")

# Input field for the user's question
question = st.text_input("Your Question:")

# File uploader for text-based file formats (called with a separate button)
uploaded_file = st.file_uploader("Choose a file", type=["txt", "md", "json", "xml", "csv", "pdf", "docx", "html"])

# Function to call the REST API (with SSL verification disabled)
def call_databricks_rest_api(question):
    # Your provided REST API endpoint (POST method)
    url = "https://rbi-apex-us01-workspace-01.cloud.databricks.com/driver-proxy-api/o/0/0919-072250-osoz48qo/5001"
    
    # The headers for authentication and content type
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Payload to be sent to the API
    payload = {
        "question": question  # Assuming your API accepts this parameter
    }
    
    # Make the POST request to the API with SSL verification disabled
    response = requests.post(url, headers=headers, json=payload, verify=False)  # Disable SSL verification
    
    # Check if the request was successful
    if response.status_code == 200:
        # Return plain text response
        return response.text  # Use `.text` to get plain text
    else:
        return f"Error: Request failed with status code {response.status_code}"

# Button to submit the question
if st.button("Ask"):
    if question:
        # Call the Databricks API with the user's question
        response = call_databricks_rest_api(question)
        
        # Display the plain text response in Streamlit
        st.write(f"Response: {response}")

# Function to call the REST API for the document upload
def call_databricks_rest_api_document(uploaded_file):
    # Your provided REST API endpoint for document upload
    url = "https://rbi-apex-us01-workspace-01.cloud.databricks.com/driver-proxy-api/o/0/0919-072250-osoz48qo/5001/document"
    
    # The headers for authentication
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Prepare the file to be sent
    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    
    # Make the POST request to the API with SSL verification disabled
    response = requests.post(url, headers=headers, files=files, verify=False)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.text  # Use `.text` to get plain text
    else:
        return f"Error: Request failed with status code {response.status_code}"

# Button to submit the file upload
if st.button("Upload Document"):
    if uploaded_file:
        # Call the Databricks API to upload the file
        response = call_databricks_rest_api_document(uploaded_file)
        
        # Display the response in Streamlit
        st.write(f"Document Upload Response: {response}")
    else:
        st.write("Please upload a file.")
