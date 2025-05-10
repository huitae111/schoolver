import streamlit as st
import openai  # ✅ 올바른 임포트

st.sidebar.title("메뉴")
page = st.sidebar.radio("이동할 페이지 선택", ["챗봇", "국립부경대학교 도서관 챗봇", "ChatPDF"])

if page == "챗봇":
    st.title("챗봇 페이지")
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear 대화 초기화"):
        st.session_state.messages = []
        st.success("대화가 초기화되었습니다!")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ OpenAI 클라이언트 초기화 (정상 방식)
    client = openai.OpenAI(api_key=api_key)

    if prompt := st.chat_input("메시지를 입력하세요"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("GPT 응답 생성 중..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
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

elif page == "국립부경대학교 도서관 챗봇":
    import fitz

    def extract_text_from_pdf(file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    client = openai.OpenAI(api_key=api_key)

    rules_text = extract_text_from_pdf("국립부경대학교 도서관 규정.pdf")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("대화 초기화"):
        st.session_state.messages = []

    if prompt := st.chat_input("도서관에 대해 궁금한 점을 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        messages = [
            {"role": "system", "content": "너는 국립부경대학교 도서관 규정집에 기반해서만 대답하는 어시스턴트야."},
            {"role": "system", "content": rules_text},
        ] + st.session_state.messages

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            answer = response.choices[0].message.content
            st.chat_message("assistant").markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"오류 발생: {e}")

elif page == "ChatPDF":
    st.title("홈 페이지")
    st.write("여기는 홈입니다.")
