import streamlit as st
import requests

# Streamlit UI for the chatbot
st.title("Databricks-Powered OpenAI Chatbot")

st.write("Chat with the OpenAI chatbot powered by Databricks.")

# Input field for the user's Bearer token
token = st.text_input("Bearer Token:", type="password")

# Input field for the base URL
base_url = st.text_input("Base URL:", placeholder="https://your-databricks-url.com")

# File uploader for text-based file formats (called with a separate button)
uploaded_file = st.file_uploader("Choose a file", type=["txt", "md", "json", "xml", "csv", "pdf", "docx", "html"])

# Function to call the REST API for the document upload
def call_databricks_rest_api_document(uploaded_file, base_url):
    url = f"{base_url}/document"
    
    headers = {
        "Authorization": f"Bearer {token}",
    }

    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    
    response = requests.post(url, headers=headers, files=files, verify=False)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Request failed with status code {response.status_code}"

# Button to submit the file upload
if st.button("Upload Document"):
    if uploaded_file:
        if base_url:
            response = call_databricks_rest_api_document(uploaded_file, base_url)
            st.write(f"Document Upload Response: {response}")
        else:
            st.write("Please enter a base URL.")
    else:
        st.write("Please upload a file.")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to call the REST API for questions
def call_databricks_rest_api(question, base_url):
    url = base_url
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "question": question
    }
    
    response = requests.post(url, headers=headers, json=payload, verify=False)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Request failed with status code {response.status_code}"

# Chat window
st.write("### Chat")

# Initialize 'ask_pressed' to detect if the question has been submitted
if "ask_pressed" not in st.session_state:
    st.session_state["ask_pressed"] = False

# Function to set the 'ask_pressed' flag when Enter is pressed
def submit_question():
    st.session_state["ask_pressed"] = True

# Input field for the user's new question, bind the on_change event
new_question = st.text_input("Type your question here:", key="new_question", on_change=submit_question)

# Check if either the button is pressed or the 'ask_pressed' flag is True from Enter key press
if st.button("Send") or st.session_state["ask_pressed"]:
    if new_question:
        if base_url:
            # Call the Databricks API with the user's question
            response = call_databricks_rest_api(new_question, base_url)
            
            # Add the new question and response to chat history
            st.session_state.chat_history.append({"question": new_question, "response": response})
            
            # Reset the flag and re-run the app to update the chat window
            st.session_state["ask_pressed"] = False
            st.rerun()
        else:
            st.write("Please enter a base URL.")
    else:
        st.write("Please enter a question.")

# Display chat history
for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['question']}")
    st.write(f"**Bot:** {chat['response']}")
