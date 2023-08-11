import streamlit as st
import requests
import time

st.title("DocuGPT")
# "https://gtemv618lc.execute-api.us-east-1.amazonaws.com/query-post-api"

def get_response_from_api(query):
    api_gateway_url = "https://ak0zrj23m4.execute-api.us-east-1.amazonaws.com/query"
    payload = {"message": query}

    try:
        response = requests.post(api_gateway_url, json=payload)
        if response.status_code == 200:
            return response.text
        else:
            return "Error: Failed to get a response from the API Gateway."
    except requests.exceptions.RequestException as e:
        return "Error: " + str(e)

# Initialising the Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying the chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

if prompt := st.chat_input("Send a Message"):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "img/usericon.png"})
    with st.chat_message("user", avatar="img/usericon.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="img/mainlogo.png"):
        assistant_response = get_response_from_api(prompt)
        message_placeholder = st.empty()
        full_response = ""
        for char in assistant_response:
            full_response += char
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response, "avatar": "img/mainlogo.png"})

# Retrieving all chat messages
all_messages = st.session_state.messages