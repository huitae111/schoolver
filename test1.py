import streamlit as st
from openai import OpenAI

st.sidebar.title("📚 메뉴")
page = st.sidebar.radio("이동할 페이지 선택", ["홈", "챗봇"])

if page == "홈":
    st.title("홈 페이지")
    st.write("여기는 홈입니다.")

elif page == "챗봇":
    st.title("🤖 챗봇 페이지")
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Clear 대화 초기화"):
    st.session_state.messages = []
    st.success("대화가 초기화되었습니다!")

# 이전 대화 보여주기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


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
