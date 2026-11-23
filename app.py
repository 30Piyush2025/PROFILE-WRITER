import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Profile & Bio Writer Agent",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ AI Developer Profile & Bio Writer")
st.caption("Agentic LangGraph workflow powered by Groq (Llama 3.3 70B) for writing high-impact GitHub READMEs, LinkedIn About sections, Headlines, and Posts.")

# API Key handling
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key

content_type = st.sidebar.selectbox(
    "Target Content Type",
    [
        "GitHub Profile README",
        "LinkedIn About Section",
        "LinkedIn Headline (under 220 chars)",
        "LinkedIn Technical Post",
        "Custom Prompt"
    ]
)

num_variations = st.sidebar.slider("Number of Variations", min_value=1, max_value=5, value=3)

st.subheader("📝 Provide Your Raw Context & Details")
sample_context = (
    "AI/ML Engineer & 2nd-year B.Tech student in Artificial Intelligence at Dr. Ambedkar Institute of Technology for Handicapped (AITD), Kanpur.\n"
    "Intern at Coding Blocks (CBSOT). Experience building clinical NLP prediction models (Sentence-BERT), LangGraph multi-agent systems, and customer churn ML pipelines.\n"
    "Skills: Python, TensorFlow, Keras, Streamlit, LangGraph, Groq, Docker."
)

user_context = st.text_area(
    "Paste your skills, projects, accomplishments, or story:",
    value=sample_context,
    height=150
)

custom_request = ""
if content_type == "Custom Prompt":
    custom_request = st.text_input("Describe the custom format or output needed:", placeholder="e.g. Twitter/X Bio + Pin Tweet")

if st.button("🚀 Generate Humanized Profiles", type="primary"):
    if not os.environ.get("GROQ_API_KEY"):
        st.error("⚠️ Please enter a Groq API Key in the sidebar to run the agent.")
    elif not user_context.strip():
        st.warning("⚠️ Please provide some background details or context.")
    else:
        with st.spinner("Invoking LangGraph agent & generating variations..."):
            try:
                from src.graph import build_profile_graph
                app = build_profile_graph()

                type_map = {
                    "GitHub Profile README": "readme",
                    "LinkedIn About Section": "linkedin_about",
                    "LinkedIn Headline (under 220 chars)": "linkedin_headline",
                    "LinkedIn Technical Post": "linkedin_post",
                    "Custom Prompt": "custom"
                }

                state = {
                    "content_type": type_map.get(content_type, "custom"),
                    "context": user_context,
                    "num_variations": num_variations
                }
                if custom_request:
                    state["request"] = custom_request

                result = app.invoke(state)
                outputs = result.get("outputs", [])

                st.success(f"Generated {len(outputs)} humanized options!")

                for idx, out in enumerate(outputs, 1):
                    with st.expander(f"✨ Option {idx}", expanded=(idx == 1)):
                        st.markdown(out)
            except Exception as e:
                st.error(f"Error during agent invocation: {e}")
