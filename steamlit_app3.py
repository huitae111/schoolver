import streamlit as st
import openai

# 🔑 OpenAI API 키 입력 (환경 변수나 secrets로 안전하게 관리 권장)
openai.api_key = "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"

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

    # GPT 모델 호출
    with st.chat_message("assistant"):
        with st.spinner("GPT 응답 생성 중..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 또는 gpt-4
                messages=st.session_state.messages
            )
            assistant_reply = response["choices"][0]["message"]["content"]
            st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
