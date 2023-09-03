import streamlit as st
import random
import openai

openai.api_key = st.secrets["general"]["OPENAI_API_KEY"]

st.title('K_BOT')

if 'chat_log' not in st.session_state:
    st.session_state.chat_log = []

if 'last_input' not in st.session_state:
    st.session_state.last_input = ""

with st.form(key='chat_form'):
    user_input = st.text_area("あの頃の...", height=200)  # text_areaを使用して高さを調整
    send_button = st.form_submit_button("送信")
   
    if send_button and user_input and user_input != st.session_state.last_input:
        # OpenAI APIを使用して応答を取得
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "The assistant is trained to emulate the tone and style of a woman who has a deep, yet platonic relationship with a man she met during her study abroad."},
                    {"role": "user", "content": "それまで何をするつもり？"},
                    {"role": "assistant", "content": "邦くんとはまた会えるから、それまでに勉強とバイトで頑張ろう!"},
                    {"role": "user", "content": user_input}
                ]
            )
            bot_response = response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            bot_response = str(e)
        
        st.session_state.chat_log.insert(0, ("Bot", bot_response))
        st.session_state.chat_log.insert(0, ("User", user_input))
        st.session_state.last_input = user_input
        
for role, message in st.session_state.chat_log:
    if role == "User":
        st.write(f'<div style="text-align: left; padding: 10px; border-radius: 5px; background-color: #191970; word-wrap: break-word;">{message}</div>', unsafe_allow_html=True)
    else:
        st.write(f'<div style="text-align: right; padding: 10px; border-radius: 5px; background-color: #B1063A; word-wrap: break-word;">{message}</div>', unsafe_allow_html=True)
