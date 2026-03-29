import streamlit as st
import os
from parser import parse_resume
from matcher import match_resume_to_job

st.set_page_config(
    page_title="Resume Matcher AI",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }
    
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        padding-top: 2rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
    }
    
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .score-circle {
        text-align: center;
        padding: 2rem;
    }
    
    .score-number {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .skill-tag-green {
        display: inline-block;
        background: rgba(52, 211, 153, 0.15);
        color: #34d399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .skill-tag-red {
        display: inline-block;
        background: rgba(248, 113, 113, 0.15);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .skill-tag-blue {
        display: inline-block;
        background: rgba(96, 165, 250, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .info-label {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 4px;
    }
    
    .info-value {
        color: #f1f5f9;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .section-heading {
        color: #f1f5f9;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .progress-bar-bg {
        background: rgba(255,255,255,0.1);
        border-radius: 100px;
        height: 8px;
        margin-top: 8px;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #a78bfa, #60a5fa) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(167, 139, 250, 0.4) !important;
    }
    
    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.03) !important;
        border: 2px dashed rgba(167, 139, 250, 0.4) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
    }
    
    div[data-testid="stTextArea"] textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-size: 0.9rem !important;
    }
    
    .stSpinner > div {
        border-top-color: #a78bfa !important;
    }

    label, .stTextArea label, .stFileUploader label {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }
    
    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎯 Resume Matcher AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Upload your resume · Paste a job description · Get instant match analysis</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"], label_visibility="visible")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    job_description = st.text_area("Job Description", height=220, placeholder="Paste the job description here...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    match_btn = st.button("⚡ Analyze Match")

with col_right:
    if match_btn:
        if uploaded_file and job_description:
            save_path = os.path.join("uploads", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Analyzing resume..."):
                resume_data = parse_resume(save_path)
                result = match_resume_to_job(resume_data["skills"], job_description)
            
            score = result["match_score"]
            if score >= 70:
                score_color = "#34d399"
                verdict = "🟢 Strong Match"
            elif score >= 40:
                score_color = "#fbbf24"
                verdict = "🟡 Moderate Match"
            else:
                score_color = "#f87171"
                verdict = "🔴 Weak Match"
            
            st.markdown(f"""
            <div class="card" style="text-align:center; padding: 2rem;">
                <div style="font-size: 5rem; font-weight: 800; color: {score_color};">{score}%</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-top: 0.5rem;">{verdict}</div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 100px; height: 10px; margin-top: 1rem;">
                    <div style="background: {score_color}; width: {score}%; height: 10px; border-radius: 100px; transition: all 1s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card">
                <div class="info-label">Candidate</div>
                <div class="info-value">{resume_data['name']}</div>
                <hr class="divider">
                <div class="info-label">Email</div>
                <div class="info-value">{resume_data['email']}</div>
                <hr class="divider">
                <div class="info-label">Skills Found in Resume</div>
                <div class="info-value">{len(resume_data['skills'])} skills detected</div>
            </div>
            """, unsafe_allow_html=True)
            
            if result["matched_skills"]:
                tags = "".join([f'<span class="skill-tag-green">✓ {s}</span>' for s in result["matched_skills"]])
                st.markdown(f'<div class="card"><div class="section-heading">✅ Matched Skills ({len(result["matched_skills"])})</div>{tags}</div>', unsafe_allow_html=True)
            
            if result["missing_skills"]:
                tags = "".join([f'<span class="skill-tag-red">✗ {s}</span>' for s in result["missing_skills"]])
                st.markdown(f'<div class="card"><div class="section-heading">❌ Missing Skills ({len(result["missing_skills"])})</div>{tags}</div>', unsafe_allow_html=True)
            
            if resume_data["skills"]:
                tags = "".join([f'<span class="skill-tag-blue">{s}</span>' for s in resume_data["skills"]])
                st.markdown(f'<div class="card"><div class="section-heading">📋 All Resume Skills</div>{tags}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="text-align:center; padding: 3rem;">
                <div style="font-size: 3rem;">👈</div>
                <div style="color: #94a3b8; margin-top: 1rem; font-size: 1rem;">Upload resume and paste job description to see results</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 3rem;">
            <div style="font-size: 3rem;">🎯</div>
            <div style="color: #f1f5f9; font-size: 1.2rem; font-weight: 600; margin-top: 1rem;">Results will appear here</div>
            <div style="color: #94a3b8; margin-top: 0.5rem;">Upload your resume and paste a job description</div>
        </div>
        """, unsafe_allow_html=True)