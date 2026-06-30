from dotenv import load_dotenv
import os
import html
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Blood Work Analyzer AI",
    page_icon="🩸",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    color: #f8fafc;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 95%;
}

.main-header {
    padding: 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    box-shadow: 0 20px 45px rgba(0,0,0,0.35);
    margin-bottom: 26px;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #ffffff;
}

.main-subtitle {
    font-size: 16px;
    color: #e0e7ff;
    margin-top: 10px;
}

.metric-box {
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    margin-bottom: 16px;
}

.metric-value {
    font-size: 32px;
    font-weight: 800;
    color: #38bdf8;
}

.metric-label {
    color: #e2e8f0;
    font-size: 14px;
    margin-top: 8px;
}

.card {
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid #334155;
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 16px 35px rgba(0,0,0,0.35);
    margin-bottom: 18px;
}

.card-title {
    font-size: 20px;
    font-weight: 750;
    color: #ffffff;
    margin-bottom: 14px;
}

.scroll-box {
    height: 230px;
    overflow-y: auto;
    padding: 16px;
    border-radius: 14px;
    background: #020617;
    border: 1px solid #334155;
    color: #e5e7eb;
    line-height: 1.7;
    font-size: 15px;
    white-space: pre-wrap;
}

.warning-box {
    background: rgba(245, 158, 11, 0.14);
    border: 1px solid #f59e0b;
    color: #fde68a;
    padding: 15px;
    border-radius: 14px;
    margin-top: 18px;
    line-height: 1.5;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    margin-top: 30px;
    padding-bottom: 20px;
}

.stTextArea textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 16px !important;
    border: 1px solid #334155 !important;
    font-size: 15px !important;
}

.stButton button {
    height: 54px;
    border-radius: 15px;
    font-size: 17px;
    font-weight: 750;
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    border: none !important;
    color: white !important;
}

.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 25px rgba(37,99,235,0.35);
}
</style>
""", unsafe_allow_html=True)

if not api_key:
    st.error("GOOGLE_API_KEY or GEMINI_API_KEY not found in .env file.")
    st.stop()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0
)

st.markdown("""
<div class="main-header">
    <div class="main-title">🩸 Blood Work Analyzer AI</div>
    <div class="main-subtitle">
        AI-powered blood report summary, abnormal value detection, Indian diet suggestions and lifestyle guidance.
    </div>
</div>
""", unsafe_allow_html=True)

top1, top2, top3, top4 = st.columns(4)

with top1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-value">AI</div>
        <div class="metric-label">Powered Analysis</div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-value">24x7</div>
        <div class="metric-label">Instant Summary</div>
    </div>
    """, unsafe_allow_html=True)

with top3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-value">Indian</div>
        <div class="metric-label">Diet Plan</div>
    </div>
    """, unsafe_allow_html=True)

with top4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-value">Safe</div>
        <div class="metric-label">Doctor Advice Needed</div>
    </div>
    """, unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.15], gap="large")

with left_col:
    st.markdown('<div class="card-title">📋 Paste Blood Work Report</div>', unsafe_allow_html=True)

    blood_report = st.text_area(
        label="Blood Report",
        height=520,
        placeholder="Paste your blood work report here...",
        label_visibility="collapsed"
    )

    analyze_clicked = st.button(
        "🧠 Analyze Blood Report",
        type="primary",
        use_container_width=True
    )

    st.markdown("""
    <div class="warning-box">
        ⚠️ This AI report is for informational purposes only.
        Please consult a qualified doctor before taking any medical decision.
    </div>
    """, unsafe_allow_html=True)

with right_col:
    summary_box = st.empty()
    abnormal_box = st.empty()
    diet_box = st.empty()
    lifestyle_box = st.empty()

def render_card(box, title, content):
    safe_content = html.escape(content or "No data available.")
    box.markdown(f"""
    <div class="card">
        <div class="card-title">{title}</div>
        <div class="scroll-box">{safe_content}</div>
    </div>
    """, unsafe_allow_html=True)

render_card(summary_box, "🩺 Health Summary", "Your health summary will appear here.")
render_card(abnormal_box, "⚠️ Abnormal Parameters", "High/Low values will appear here.")
render_card(diet_box, "🍎 Suggested Indian Diet Plan", "Diet suggestions will appear here.")
render_card(lifestyle_box, "🏃 Lifestyle & Follow-up Advice", "Lifestyle recommendations will appear here.")

if analyze_clicked:
    if not blood_report.strip():
        st.warning("Please paste a blood work report before analyzing.")
    else:
        with st.spinner("Analyzing your blood work report..."):
            prompt = f"""
You are a responsible medical report assistant.

Analyze the following blood report and provide output in exactly these sections:

SECTION 1 - HEALTH SUMMARY
Give a simple 4-5 line summary in non-technical language.

SECTION 2 - ABNORMAL PARAMETERS
List abnormal values only.
Format:
- Test Name: Value | Status: HIGH/LOW | Reference Range | Simple Meaning

If no abnormal values are found, write:
No major abnormal values detected based on the provided reference ranges.

SECTION 3 - INDIAN DIET PLAN
Give practical Indian food suggestions.
Include:
Foods to eat more:
Foods to avoid/reduce:

Use common Indian foods like dal, roti, sabzi, rice, curd, fruits, nuts, sprouts, vegetables, etc.

SECTION 4 - LIFESTYLE AND FOLLOW-UP
Give concise lifestyle advice.
Also mention when to consult a doctor.

Important:
- Do not diagnose disease.
- Do not prescribe medicine.
- Keep language simple.
- Always recommend consulting a qualified doctor.

Blood Report:
{blood_report}
"""
            response = llm.invoke(prompt)
            full_response = response.content

        def extract_section(text, start, end=None):
            if start not in text:
                return ""
            part = text.split(start, 1)[1]
            if end and end in part:
                part = part.split(end, 1)[0]
            return part.strip()

        health_summary = extract_section(
            full_response,
            "SECTION 1 - HEALTH SUMMARY",
            "SECTION 2 - ABNORMAL PARAMETERS"
        )

        abnormal_values = extract_section(
            full_response,
            "SECTION 2 - ABNORMAL PARAMETERS",
            "SECTION 3 - INDIAN DIET PLAN"
        )

        diet_plan = extract_section(
            full_response,
            "SECTION 3 - INDIAN DIET PLAN",
            "SECTION 4 - LIFESTYLE AND FOLLOW-UP"
        )

        lifestyle = extract_section(
            full_response,
            "SECTION 4 - LIFESTYLE AND FOLLOW-UP"
        )

        if not any([health_summary, abnormal_values, diet_plan, lifestyle]):
            health_summary = full_response

        render_card(summary_box, "🩺 Health Summary", health_summary)
        render_card(abnormal_box, "⚠️ Abnormal Parameters", abnormal_values)
        render_card(diet_box, "🍎 Suggested Indian Diet Plan", diet_plan)
        render_card(lifestyle_box, "🏃 Lifestyle & Follow-up Advice", lifestyle)

st.markdown("""
<div class="footer">
    ⚠️ AI-generated report. This is not medical advice. Please consult a qualified doctor.
    <br>
    Powered by Gemini AI | Built with Streamlit
</div>
""", unsafe_allow_html=True)