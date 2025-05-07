import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 불러오기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("GPT 응답 생성 중..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            assistant_reply = response.choices[0].message.content
            st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
