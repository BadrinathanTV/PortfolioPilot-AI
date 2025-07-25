# app.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

# Import your existing backend modules
from core.graph_builder import graph
from tools.zerodha_client import initialize_zerodha_client
from tools import zerodha_tools

# This is a bit of a hack to ensure the client is set for all tool modules
# In a larger app, you might use a more robust dependency injection pattern.
risk_tools_module = __import__("tools.risk_tools", fromlist=[""])
technical_tools_module = __import__("tools.technical_tools", fromlist=[""])


def login_page():
    """
    Displays the login page for the user to authenticate with Zerodha.
    """
    st.set_page_config(page_title="Finance Bot Login", page_icon="🔑")
    st.title("Welcome to the Finance Bot 🤖")
    st.write("Please log in to your Zerodha account to continue.")

    login_url = initialize_zerodha_client(generate_url_only=True)
    st.markdown(f"**Step 1:** [Click here to log in to Zerodha]({login_url})")
    st.info("After logging in, copy the `request_token` from the URL in your browser's address bar.")

    request_token = st.text_input("Step 2: Paste your request_token here", key="request_token_input")

    if st.button("Connect to Zerodha", key="connect_button"):
        if request_token:
            with st.spinner("Authenticating..."):
                try:
                    client = initialize_zerodha_client(request_token=request_token)
                    if client:
                        st.success("✅ Zerodha connection successful!")
                        st.session_state.zerodha_client = client
                        st.session_state.logged_in = True
                        
                        # Inject the live client into all relevant tool modules
                        zerodha_tools.set_client(client)
                        
                        st.rerun()
                    else:
                        st.error("❌ Authentication failed. Please check your request_token.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please paste your request_token.")


def chat_page():
    """
    Displays the main chatbot interface after the user has logged in.
    """
    st.set_page_config(page_title="Finance Bot", page_icon="📈")
    st.title("Finance Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = [AIMessage(content="Hello! How can I assist you today?")]

    for message in st.session_state.messages:
        with st.chat_message(message.type):
            st.markdown(message.content)

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                message_placeholder = st.empty()
                

                graph_input = {
                    "messages": st.session_state.messages
                }

                # Stream the response from the graph
                final_response = ""
                for chunk in graph.stream(graph_input):
                    agent_response = chunk.get("supervisor", {}).get("messages", [])
                    if agent_response:
                        message_content = agent_response[-1].content
                        if message_content:
                            final_response += message_content
                            message_placeholder.markdown(final_response + "▌")
                
                message_placeholder.markdown(final_response)
        
        st.session_state.messages.append(AIMessage(content=final_response))

# --- Main App Logic ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    chat_page()
else:
    login_page()
