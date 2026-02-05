import ChatBot
import streamlit as st



st.set_page_config(
    page_title = 'Welcome!!',
    layout='wide'
)

st.title("Your AI Assistant")

st.caption("Ask me anything!!!")

if 'messages' not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])


user_input = st.chat_input('Type your prmpt: ')

if user_input:
    st.session_state.messages.append({
        "role" : "user",
        "content" : user_input
    })

    with st.chat_message('assistant'):
        with st.spinner("Thinking ........."):
            response = ChatBot.RAGOllama(userPrompt=user_input)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content" : response
        }
    )
    st.rerun()

    