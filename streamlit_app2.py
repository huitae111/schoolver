import streamlit as st
import openai
import json

# 👉 1. 비밀번호 입력받기 (API Key)
api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

# 👉 2. 사용자 질문 입력
question = st.text_area("질문을 입력하세요:")

# 👉 3. 버튼 클릭 시 GPT 호출
if st.button("답변 받기") and api_key and question:
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # 또는 gpt-4-1106-preview
            messages=[
                {"role": "system", "content": "너는 사용자의 질문을 입력받아 응답을 하는 도우미야."},
                {"role": "user", "content": question}
            ]
        )

        answer = response["choices"][0]["message"]["content"]
        st.write("### GPT의 답변:")
        st.write(answer)

    except Exception as e:
        st.error(f"오류 발생: {e}")
