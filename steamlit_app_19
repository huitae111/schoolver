import streamlit as st

# 메시지를 저장할 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 보여주기
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 화면에 출력
    st.chat_message("user").markdown(prompt)
    # 메시지를 세션에 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 챗봇 응답 (예시: echo 응답)
    response = f"Echo: {prompt}"
    # 챗봇 응답 출력
    with st.chat_message("assistant"):
        st.markdown(response)
    # 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})
