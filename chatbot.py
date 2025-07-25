import streamlit as st
from together import Together
from dotenv import load_dotenv
import os


load_dotenv()






st.markdown("""
##  Welcome!
This is an experimental chatbot project powered by AI, showcasing the capabilities of large language models (LLMs) through natural conversation.

You can start by entering your API Key to the side bar and typing a message below or clicking one of the quick prompts above.

**Note:** This project is for my portfolio only.
""")



st.sidebar.title("🔗 FLEXIBLE Chatbot")

name = st.sidebar.text_input("Insert your chatbot API Key here:", key="a")
model_input = st.sidebar.text_input("Insert your model address here:", key="b")

st.sidebar.warning("Note: Currently Together AI and Qwen Model only support this. However, feel free to try other LLM and models too.")
client = Together(api_key=name)

if not name or not model_input:
    st.sidebar.warning("Please insert a valid API key or model address")
    st.stop()
    
st.sidebar.header('Ask me the following:')
suggested_questions = [
    "Hi",
    "How are you?",
    "Is anyone there?",
    "What is the weather today?",
    "Create me a schedule for workout",
    "Code me a simple python program",
    "What is SEO and SSR/CSR",
]

try:
    if "messages" not in st.session_state:
        st.session_state.messages = []


    for question in suggested_questions:
        if st.sidebar.button(question):
            st.session_state.messages.append({"role": "user", "content": question})
            response = client.chat.completions.create(
                model=model_input,
                max_tokens=512,
                messages=st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me something..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model_input,
            max_tokens=512,
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
except Exception as e:
    st.error("Please check the API Key or Model Address")