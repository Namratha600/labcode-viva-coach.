import streamlit as st
import requests


st.set_page_config(
    page_title="LabCode Fixer & Viva Coach",
    page_icon="💻",
    layout="centered"
)


st.title("💻 LabCode Fixer & Viva Coach")

st.write(
    "Debug your code, understand the error, and prepare for your viva."
)

st.caption("Debug → Understand → Correct → Defend")


st.info(
    "💡 Paste your code and the compiler or runtime error. "
    "The AI will explain why it failed, provide a corrected version, "
    "and generate 3 technical viva questions."
)


st.divider()


st.subheader("📝 Enter Your Problem")


language = st.selectbox(
    "Programming Language",
    ["Java", "Python", "C", "C++"]
)


code = st.text_area(
    "💻 Your Code",
    placeholder="Paste your code here...",
    height=250
)


error = st.text_area(
    "⚠️ Error Message",
    placeholder="Paste the compiler or runtime error here...",
    height=150
)


col1, col2 = st.columns(2)


with col1:
    analyze_button = st.button(
        "🔍 Analyze Code",
        use_container_width=True
    )


with col2:
    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


if clear_button:
    st.rerun()


if analyze_button:

    if not code.strip():

        st.warning("Please paste your code.")

    elif not error.strip():

        st.warning("Please paste the error message.")

    else:

        data = {
            "language": language,
            "code": code,
            "error": error
        }

        try:

            with st.spinner("🤖 Analyzing your code..."):

                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json=data,
                    timeout=120
                )

            if response.status_code == 200:

                result = response.json()

                if "analysis" in result:

                    st.divider()

                    st.subheader("🤖 AI Analysis")

                    st.markdown(result["analysis"])

                else:

                    st.error(
                        result.get(
                            "error",
                            "Something went wrong."
                        )
                    )

            else:

                st.error(
                    f"Backend returned an error "
                    f"(status code: {response.status_code})."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the backend. "
                "Make sure FastAPI is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The AI took too long to respond. "
                "Please try again."
            )


st.divider()


st.subheader("💡 Example Problem")


st.code(
    """numbers = [1, 2, 3]
print(numbers[5])""",
    language="python"
)


st.caption(
    "Error: IndexError: list index out of range"
)


st.divider()


st.caption(
    "LabCode Fixer & Viva Coach • "
    "Built for learning, debugging, and viva preparation."
)