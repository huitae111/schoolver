import streamlit as st
from openai import OpenAI

# API 키
api_key = "sk-..."  # 실제 키 넣기

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

# 메시지 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # GPT 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("GPT 응답 생성 중..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # 또는 gpt-4
                    messages=[
                        {"role": "system", "content": "너는 친절한 도우미야."},
                        *st.session_state.messages
                    ]
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"오류 발생: {e}")
