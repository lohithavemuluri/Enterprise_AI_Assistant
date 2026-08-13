import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from google import genai

from sql_agent import answer_question
from dashboard import show_dashboard
from ReportGenerator import generate_report
from evaluation import show_evaluation
from monitoring import log_info, log_error
from auth import login, logout
from ocr import extract_text_with_ocr



# LOAD API KEY


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# PAGE SETTINGS


st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# LOGIN

if not login():
    st.stop()

logout()

log_info("Enterprise AI Assistant started")


# TITLE

st.title("🤖 Enterprise AI Assistant")

st.write(
    "An AI-powered platform for enterprise documents "
    "and structured business data."
)


# SIDEBAR


st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Choose an assistant:",
    [
        "📄 Document Assistant",
        "🗄️ SQL Database Assistant",
        "📊 Enterprise Dashboard",
        "📑 AI Report Generator",
        "🔍 AI Response Evaluation"
    ]
)


# 1. DOCUMENT ASSISTANT


if option == "📄 Document Assistant":

    log_info("Document Assistant selected")

    st.header("📄 Document Assistant")

    st.write(
        "Upload an enterprise PDF and ask questions "
        "about the document."
    )

    uploaded_file = st.file_uploader(
        "Upload your enterprise document",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:

            # READ PDF BYTES

            pdf_bytes = uploaded_file.getvalue()

            full_text = ""

            # FIRST TRY NORMAL PDF TEXT EXTRACTION

            pdf_reader = PdfReader(
                uploaded_file
            )

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:

                    full_text += page_text + "\n"

            # OCR FALLBACK

            if not full_text.strip():

                st.info(
                    "This appears to be a scanned PDF. "
                    "Running OCR to extract the text..."
                )

                log_info(
                    f"Scanned PDF detected: {uploaded_file.name}"
                )

                full_text = extract_text_with_ocr(
                    pdf_bytes
                )

                if full_text.strip():

                    st.success(
                        "Scanned PDF processed successfully using OCR."
                    )

                    log_info(
                        "OCR extraction successful"
                    )

                else:

                    st.error(
                        "OCR could not extract text from this PDF."
                    )

            else:

                st.success(
                    "Document uploaded successfully!"
                )

                log_info(
                    f"Normal PDF uploaded: {uploaded_file.name}"
                )

            # CHECK EXTRACTED TEXT
       

            if full_text.strip():

                st.write(
                    "Your document is ready. "
                    "You can ask questions about it."
                )


                # CHUNK DOCUMENT

                chunk_size = 1500

                chunks = []

                for i in range(
                    0,
                    len(full_text),
                    chunk_size
                ):

                    chunk = full_text[
                        i:i + chunk_size
                    ]

                    if chunk.strip():

                        chunks.append(chunk)

                # TF-IDF SEARCH

                if len(chunks) > 0:

                    vectorizer = TfidfVectorizer(
                        stop_words="english"
                    )

                    document_vectors = (
                        vectorizer.fit_transform(
                            chunks
                        )
                    )


                    # QUESTION
     
                    question = st.text_input(
                        "Ask a question about your document:"
                    )


                    if st.button(
                        "Ask AI"
                    ):

                        if question.strip():

                            log_info(
                                f"Document question asked: {question}"
                            )

                            try:

                          
                                # QUESTION VECTOR
                    

                                question_vector = (
                                    vectorizer.transform(
                                        [question]
                                    )
                                )

                                # similarity

                                similarities = (
                                    cosine_similarity(
                                        question_vector,
                                        document_vectors
                                    )[0]
                                )

            
                                # TOP 3 CHUNKS
                       

                                top_indices = (
                                    similarities.argsort()[
                                        -3:
                                    ][::-1]
                                )


                                relevant_text = ""

                                for index in top_indices:

                                    relevant_text += (
                                        chunks[index]
                                    )

                                    relevant_text += (
                                        "\n\n"
                                    )


                                # GEMINI
                       

                                prompt = f"""
You are an Enterprise AI Assistant.

Answer the user's question using ONLY the
information provided in the document context.

If the answer cannot be found in the document,
say:

"I could not find this information in the uploaded document."

Document context:

{relevant_text}

User question:

{question}

Give a clear, professional and concise answer.
"""


                                response = (
                                    client.models.generate_content(
                                        model="gemini-3.6-flash",
                                        contents=prompt
                                    )
                                )


                      
                                # DISPLAY ANSWER
                         

                                st.subheader(
                                    "🤖 AI Answer"
                                )

                                st.write(
                                    response.text
                                )


                                log_info(
                                    "Document question answered successfully"
                                )


                            except Exception as e:

                                log_error(
                                    f"Document Assistant error: {str(e)}"
                                )

                                st.error(
                                    "Unable to process the document question."
                                )

                        else:

                            st.warning(
                                "Please enter a question."
                            )


                else:

                    st.warning(
                        "Could not create searchable text chunks."
                    )


            else:

                st.error(
                    "Could not extract any text from this PDF."
                )


        except Exception as e:

            log_error(
                f"Document upload error: {str(e)}"
            )

            st.error(
                "Unable to process the uploaded document."
            )


# 2. SQL DATABASE ASSISTANT

elif option == "🗄️ SQL Database Assistant":

    log_info(
        "SQL Database Assistant selected"
    )

    st.header(
        "🗄️ SQL Database Assistant"
    )

    st.write(
        "Ask questions about enterprise business data "
        "using natural language."
    )

    st.info(
        "You can ask questions about employees, "
        "products and sales."
    )

    # QUESTION

    question = st.text_input(
        "Ask a question about your business data:"
    )


    if st.button(
        "Run Database Query"
    ):

        if question.strip():

            log_info(
                f"SQL question asked: {question}"
            )

            try:

                with st.spinner(
                    "Analyzing your question..."
                ):

                    answer, sql = answer_question(
                        question
                    )


                # ANSWER
                st.subheader(
                    "🤖 AI Answer"
                )

                st.write(
                    answer
                )


                # SQL
        

                if sql:

                    with st.expander(
                        "View Generated SQL"
                    ):

                        st.code(
                            sql,
                            language="sql"
                        )


                log_info(
                    "SQL question answered successfully"
                )


            except Exception as e:

                log_error(
                    f"SQL Assistant error: {str(e)}"
                )

                st.error(
                    "Unable to process the database query."
                )

        else:

            st.warning(
                "Please enter a question."
            )


# 3. ENTERPRISE DASHBOARD

elif option == "📊 Enterprise Dashboard":

    log_info(
        "Enterprise Dashboard selected"
    )

    try:

        show_dashboard()

        log_info(
            "Enterprise Dashboard loaded successfully"
        )

    except Exception as e:

        log_error(
            f"Dashboard error: {str(e)}"
        )

        st.error(
            "Unable to load the dashboard."
        )


# 4. AI REPORT GENERATOR

elif option == "📑 AI Report Generator":

    log_info(
        "AI Report Generator selected"
    )

    try:

        generate_report()

        log_info(
            "AI Report Generator opened successfully"
        )

    except Exception as e:

        log_error(
            f"Report Generator error: {str(e)}"
        )

        st.error(
            "Unable to open the report generator."
        )

# 5. AI RESPONSE EVALUATION

elif option == "🔍 AI Response Evaluation":

    log_info(
        "AI Response Evaluation selected"
    )

    try:

        show_evaluation()

        log_info(
            "AI Response Evaluation opened successfully"
        )

    except Exception as e:

        log_error(
            f"Evaluation error: {str(e)}"
        )

        st.error(
            "Unable to open AI response evaluation."
        )