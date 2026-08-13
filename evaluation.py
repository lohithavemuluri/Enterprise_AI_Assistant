import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# LOAD KEY
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# EVALUATE AI RESPONSE

def evaluate_response(question, context, answer):

    prompt = f"""
You are an AI response evaluator.

Evaluate the following AI answer using ONLY the
provided context.

QUESTION:
{question}

CONTEXT:
{context}

AI ANSWER:
{answer}

Give an evaluation using this format:

Relevance: X/10
Accuracy: X/10
Clarity: X/10
Overall Score: X/10

Feedback:
Write a short explanation.

Do not invent information.
If the answer is not supported by the context,
give a low Accuracy score.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# EVALUATION PAGE

def show_evaluation():

    st.header("🔍 AI Response Evaluation")

    st.write(
        "Evaluate the quality of an AI-generated answer "
        "using a question and supporting context."
    )

    # USER INPUT

    question = st.text_input(
        "Enter the question:"
    )

    context = st.text_area(
        "Enter the supporting context:",
        height=200
    )

    answer = st.text_area(
        "Enter the AI answer:",
        height=150
    )
 
    # EVALUATE BUTTON
 

    if st.button("🔍 Evaluate AI Response"):

        if (
            question.strip()
            and context.strip()
            and answer.strip()
        ):

            with st.spinner(
                "Evaluating AI response..."
            ):

                try:

                    result = evaluate_response(
                        question,
                        context,
                        answer
                    )

                    st.subheader(
                        "📊 Evaluation Result"
                    )

                    st.write(result)

                except Exception as e:

                    st.error(
                        "Unable to evaluate the response."
                    )

                    with st.expander(
                        "Technical Details"
                    ):

                        st.code(str(e))

        else:

            st.warning(
                "Please fill in all three fields."
            )