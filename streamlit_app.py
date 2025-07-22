import streamlit as st
import requests
import time
import plotly.graph_objects as go
import os

st.set_page_config(page_title="NextGen Salary Dashboard", page_icon="💼", layout="wide")

# 🎨 Styling + Slogan
st.markdown("""
<style>
    html, body, [class*="css"] {
        background-color: #f0f4f8;
    }
    h1 {
        color: #FF4B4B;
        font-size: 48px;
        text-align: center;
    }
    .stButton button {
        background-color: #FF4B4B;
        color: white;
        font-size: 18px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚀 Unlock Your True Earning Potential</h1>", unsafe_allow_html=True)
st.markdown("""
    <h4 style='text-align: center; color: #2C3E50; font-style: italic;'>
    AI-powered insights to elevate your career journey.
    </h4>
""", unsafe_allow_html=True)
st.markdown("---")

# 🔍 Form
with st.form("predict_form"):
    col1, col2 = st.columns(2)
    with col1:
        experience = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Executive"])
        employment = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract", "Internship"])
        job_title = st.text_input("Job Title")
        residence = st.text_input("Employee Residence")
    with col2:
        remote_ratio = st.slider("Remote Ratio (%)", 0, 100, 50)
        company_location = st.text_input("Company Location")
        company_size = st.selectbox("Company Size", ["Small", "Medium", "Large"])
        resume = st.file_uploader("📄 Upload Resume (PDF/CSV)", type=["pdf", "csv"])

    submit = st.form_submit_button("🔍 Predict & Analyze")

# 💡 Output Section
if submit:
    with st.spinner("🎯 Predicting... and analyzing your profile"):
        time.sleep(2)
        payload = {
            "experience_level": experience,
            "employment_type": employment,
            "job_title": job_title,
            "employee_residence": residence,
            "remote_ratio": remote_ratio,
            "company_location": company_location,
            "company_size": company_size
        }

        salary = None
        try:
            response = requests.post("http://127.0.0.1:5000/predict", json=payload)
            salary = response.json().get('predicted_salary')
        except Exception:
            st.warning("🔄 Prediction service is offline. Showing estimated insights.")

        if salary:
            st.success(f"💰 Predicted Salary: ${salary}")
            st.balloons()
        else:
            salary = 70000  # fallback value
            st.info(f"💰 Estimated Salary: ${salary} (default)")

        # 📈 Salary Growth Chart
        years = list(range(1, 6))
        projected = [round(salary * (1.05 ** y)) for y in years]
        fig = go.Figure(data=go.Scatter(x=years, y=projected, mode='lines+markers'))
        fig.update_layout(title="📈 Salary Growth Over 5 Years", xaxis_title="Years", yaxis_title="USD")
        st.plotly_chart(fig)

        # 🧠 Career Suggestions
        st.markdown("### 🧠 Career Suggestions Based on Your Profile")
        st.info("You're a strong match for: **ML Engineer**, **Data Analyst**, **BI Developer**")

        # 🌍 Country Comparison Chart
        st.markdown("### 🌍 Top 5 Country Comparison")
        countries = ["US 🇺🇸", "Germany 🇩🇪", "India 🇮🇳", "UK 🇬🇧", "Canada 🇨🇦"]
        salaries = [salary * 1.2, salary * 1.15, salary * 0.8, salary, salary * 1.05]
        country_fig = go.Figure([go.Bar(x=countries, y=salaries, marker_color='indianred')])
        st.plotly_chart(country_fig)

        # 📄 Resume Feedback (Placeholder)
        if resume:
            st.markdown("### 📝 Resume Analysis & Skill Gaps")
            st.warning("Resume parsed: Looking for keywords... 🚧 *(Feature in development)*")

        # 📥 PDF Export
        st.markdown("### 📄 Export Your Insights")
        try:
            with open("report.pdf", "rb") as f:
                pdf_bytes = f.read()
            st.download_button("📥 Export PDF Report", data=pdf_bytes, file_name="salary_report.pdf", mime="application/pdf")
        except FileNotFoundError:
            st.warning("📄 PDF file not found. Please add 'report.pdf' to your folder.")
