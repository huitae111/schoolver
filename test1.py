import streamlit as st
import openai
import os

# API 키 입력받기
api_key = "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"

# 질문 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

# 실행 버튼
if api_key and question:
    client = openai.OpenAI(api_key=api_key)  # 최신 버전 방식

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "너는 친절한 도우미야."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        st.write(answer)

    except Exception as e:
        st.error(f"오류 발생: {e}")
