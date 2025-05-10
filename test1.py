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
    import tempfile
    import os

    st.title("ChatPDF - PDF로 질문하기")

    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    openai.api_key = api_key  # ✅ 최신 방식으로 설정

    uploaded_file = st.file_uploader("PDF 파일을 업로드하세요 (1개만)", type=["pdf"])

    if "vector_file_id" not in st.session_state:
        st.session_state.vector_file_id = None
    if "assistant_id" not in st.session_state:
        st.session_state.assistant_id = None
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

    # Clear 버튼 (벡터 삭제용)
    if st.button("Clear"):
        if st.session_state.vector_file_id:
            try:
                openai.files.delete(st.session_state.vector_file_id)
                st.success("벡터 파일이 삭제되었습니다.")
            except Exception as e:
                st.error(f"벡터 삭제 오류: {e}")
        st.session_state.vector_file_id = None
        st.session_state.assistant_id = None
        st.session_state.thread_id = None

    # 파일 업로드 처리
    if uploaded_file and api_key:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        with st.spinner("PDF 업로드 중..."):
            try:
                uploaded = openai.files.create(
                    file=open(tmp_file_path, "rb"),
                    purpose="assistants"
                )
                st.session_state.vector_file_id = uploaded.id
                st.success("PDF 업로드 성공!")
            except Exception as e:
                st.error(f"업로드 오류: {e}")

    # Assistant 생성
    if st.session_state.vector_file_id and not st.session_state.assistant_id:
        try:
            assistant = openai.beta.assistants.create(
                name="ChatPDF Assistant",
                instructions="업로드된 PDF 내용을 바탕으로 사용자의 질문에 답변하세요.",
                tools=[{"type": "file_search"}],
                file_ids=[st.session_state.vector_file_id],
                model="gpt-4"
            )
            st.session_state.assistant_id = assistant.id
            thread = openai.beta.threads.create()
            st.session_state.thread_id = thread.id
        except Exception as e:
            st.error(f"Assistant 생성 오류: {e}")

    # 사용자 질문
    if st.session_state.assistant_id and st.session_state.thread_id:
        prompt = st.chat_input("PDF 내용 기반으로 질문해보세요:")
        if prompt:
            st.chat_message("user").markdown(prompt)
            try:
                openai.beta.threads.messages.create(
                    thread_id=st.session_state.thread_id,
                    role="user",
                    content=prompt
                )

                with st.chat_message("assistant"):
                    with st.spinner("답변 생성 중..."):
                        run = openai.beta.threads.runs.create(
                            thread_id=st.session_state.thread_id,
                            assistant_id=st.session_state.assistant_id
                        )

                        while True:
                            run_status = openai.beta.threads.runs.retrieve(
                                thread_id=st.session_state.thread_id,
                                run_id=run.id
                            )
                            if run_status.status == "completed":
                                break

                        messages = openai.beta.threads.messages.list(
                            thread_id=st.session_state.thread_id
                        )
                        answer = messages.data[0].content[0].text.value
                        st.markdown(answer)
            except Exception as e:
                st.error(f"응답 오류: {e}")


