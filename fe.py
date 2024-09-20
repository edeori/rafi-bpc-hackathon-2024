import streamlit as st
import requests


# Streamlit UI for the chatbot
st.title("Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

cols=st.columns(2)
with cols[0]:
    # Input field for the user's Bearer token
    token = st.text_input("Bearer Token:", type="password")
with cols[1]:
    url = st.text_input("Databricks Url:", placeholder="https://your-databricks-url.com")

# Function to call the REST API (with SSL verification disabled)
def call_databricks_rest_api(question):
    # Your provided REST API endpoint (POST method)

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

def join_url_base_path(base_url, path):
    # Strip any trailing slashes from base_url and leading slashes from path
    base_url = base_url.rstrip('/')
    path = path.lstrip('/')

    return f"{base_url}/{path}"



# Function to call the REST API for the document upload
def call_databricks_rest_api_document(uploaded_file):
    # Your provided REST API endpoint for document upload
    documents_url = join_url_base_path(url, "document")

    # The headers for authentication
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Prepare the file to be sent
    files = {
        'file': (uploaded_file.name, uploaded_file, uploaded_file.type)
    }

    print(documents_url)
    # Make the POST request to the API with SSL verification disabled
    response = requests.post(documents_url, headers=headers, files=files, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text  # Use `.text` to get plain text
    else:
        return f"Error: Request failed with status code {response.status_code}"

ask = st.chat_input("What is up?")

with st.container(height=444):
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # React to user input
    if prompt := ask:
        # Call the Databricks API with the user's question
        response = call_databricks_rest_api(prompt)
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


with st.container(height=290):

    # File uploader for text-based file formats (called with a separate button)
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "md", "json", "xml", "csv", "pdf", "docx", "html"])

    # Button to submit the file upload
    if st.button("Upload Document"):
        if uploaded_file:
            # Call the Databricks API to upload the file
            response = call_databricks_rest_api_document(uploaded_file)

            # Display the response in Streamlit
            st.write(f"Document Upload Response: {response}")
        else:
            st.write("Please upload a file.")
