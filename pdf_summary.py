import streamlit as st
from pypdf import PdfReader
import ollama
from config import MODEL_NAME


def get_pdf_text(uploaded_file):

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def ask_llama(prompt):

    response = ollama.chat(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def pdf_page():

    st.title("📄 PDF Assistant")

    uploaded_file = st.file_uploader(

        "Upload your PDF",

        type=["pdf"]

    )

    if uploaded_file is None:

        st.info("Please upload a PDF.")

        return

    text = get_pdf_text(uploaded_file)

    st.success("✅ PDF Loaded Successfully")

    menu = st.selectbox(

        "Choose Feature",

        [

            "Summary",

            "Ask Question",

            "Generate Notes",

            "Generate Quiz"

        ]

    )

    if menu == "Summary":

        if st.button("Generate Summary"):

            with st.spinner("Generating Summary..."):

                prompt = f"""

Summarize this PDF in simple language.

{text}

"""

                answer = ask_llama(prompt)

                st.subheader("Summary")

                st.write(answer)

    elif menu == "Ask Question":

        question = st.text_input(

            "Ask anything from this PDF"

        )

        if st.button("Ask AI"):

            with st.spinner("Thinking..."):

                prompt = f"""

PDF Content:

{text}

Question:

{question}

Answer from PDF only.

"""

                answer = ask_llama(prompt)

                st.subheader("Answer")

                st.write(answer)
    elif menu == "Generate Notes":

        if st.button("Generate Notes"):

            with st.spinner("Generating Notes..."):

                prompt = f"""
Create short study notes from the following PDF.

Use headings and bullet points.

PDF:

{text}
"""

                answer = ask_llama(prompt)

                st.subheader("📚 Notes")

                st.write(answer)


    elif menu == "Generate Quiz":

        number = st.slider(

            "Number of Questions",

            5,

            20,

            10

        )

        if st.button("Generate Quiz"):

            with st.spinner("Generating Quiz..."):

                prompt = f"""
Create {number} MCQs from this PDF.

Each question should contain:

Question

A)

B)

C)

D)

Correct Answer

PDF:

{text}
"""

                answer = ask_llama(prompt)

                st.subheader("📝 Quiz")

                st.write(answer)