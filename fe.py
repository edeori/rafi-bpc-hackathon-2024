import streamlit as st
import requests

# Streamlit UI for the chatbot
st.title("Databricks-Powered OpenAI Chatbot")

st.write("Ask a question to the chatbot:")

# Input field for the user's question
question = st.text_input("Your Question:")

# Function to call the REST API (with SSL verification disabled)
def call_databricks_rest_api(question):
    # Your provided REST API endpoint (POST method)
    url = "https://rbi-apex-us01-workspace-01.cloud.databricks.com/driver-proxy-api/o/0/0919-072250-osoz48qo/5001"
    
    # The headers for authentication and content type
    headers = {
        "Authorization": f"Bearer ",
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
