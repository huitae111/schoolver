import streamlit as st
import openai
import os

# API 키 입력받기
api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

# 질문 입력
question = st.text_area("질문을 입력하세요:")

# 실행 버튼
if st.button("답변 받기") and api_key and question:
    client = openai.OpenAI(api_key=api_key)  # 최신 버전 방식

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 친절한 도우미야."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        st.write("### GPT의 답변:")
        st.write(answer)

    except Exception as e:
        st.error(f"오류 발생: {e}")
