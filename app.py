import streamlit as st
import os
import tempfile
from parser import parse_resume
from matcher import match_resume_to_job

st.set_page_config(page_title="Resume Matcher AI", page_icon="🎯", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
.stApp { background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 50%, #0d1b2a 100%); min-height: 100vh; }
.hero { text-align: center; padding: 3rem 0 2rem; }
.hero-badge { display: inline-block; background: rgba(167,139,250,0.15); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); border-radius: 100px; padding: 6px 18px; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 1.2rem; }
.hero-title { font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin-bottom: 1rem; }
.hero-title span { background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { color: #64748b; font-size: 1.1rem; max-width: 500px; margin: 0 auto 2rem; line-height: 1.6; }
.glass-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 1.8rem; margin-bottom: 1.2rem; transition: border-color 0.3s; }
.glass-card:hover { border-color: rgba(167,139,250,0.3); }
.card-label { color: #475569; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.8rem; }
.score-wrap { text-align: center; padding: 2.5rem 1rem; }
.score-num { font-size: 6rem; font-weight: 800; line-height: 1; }
.score-label { font-size: 1rem; font-weight: 500; margin-top: 0.5rem; letter-spacing: 0.05em; }
.score-bar-bg { background: rgba(255,255,255,0.06); border-radius: 100px; height: 6px; margin-top: 1.5rem; overflow: hidden; }
.verdict-strong { color: #34d399; }
.verdict-medium { color: #fbbf24; }
.verdict-weak { color: #f87171; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.2rem; }
.info-item { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1rem 1.2rem; }
.info-item-label { color: #475569; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; }
.info-item-value { color: #e2e8f0; font-size: 0.95rem; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.skill-section { margin-bottom: 1.2rem; }
.skill-section-title { color: #94a3b8; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 8px; }
.skill-dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; }
.tag { display: inline-block; border-radius: 8px; padding: 5px 14px; margin: 3px; font-size: 0.82rem; font-weight: 500; }
.tag-green { background: rgba(52,211,153,0.1); color: #34d399; border: 1px solid rgba(52,211,153,0.2); }
.tag-red { background: rgba(248,113,113,0.1); color: #f87171; border: 1px solid rgba(248,113,113,0.2); }
.tag-blue { background: rgba(96,165,250,0.1); color: #60a5fa; border: 1px solid rgba(96,165,250,0.2); }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon { font-size: 3.5rem; margin-bottom: 1rem; }
.empty-title { color: #e2e8f0; font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem; }
.empty-sub { color: #475569; font-size: 0.95rem; }
.stButton > button { width: 100%; background: linear-gradient(135deg, #7c3aed, #2563eb) !important; color: white !important; border: none !important; border-radius: 14px !important; padding: 0.85rem 2rem !important; font-size: 1rem !important; font-weight: 700 !important; letter-spacing: 0.03em !important; transition: all 0.3s ease !important; }
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
div[data-testid="stFileUploader"] { background: rgba(255,255,255,0.02) !important; border: 2px dashed rgba(124,58,237,0.4) !important; border-radius: 16px !important; }
div[data-testid="stTextArea"] textarea { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 12px !important; color: #e2e8f0 !important; font-size: 0.9rem !important; }
div[data-testid="stTextArea"] textarea:focus { border-color: rgba(124,58,237,0.5) !important; }
label { color: #475569 !important; font-weight: 600 !important; font-size: 0.75rem !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-badge">AI Powered</div>
  <div class="hero-title">Find Your Perfect<br><span>Job Match</span></div>
  <div class="hero-sub">Upload your resume, paste a job description, and get instant AI-powered match analysis with skill gap insights.</div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card"><div class="card-label">Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><div class="card-label">Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area("Paste job description", height=200, placeholder="Paste the full job description here...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    match_btn = st.button("⚡  Analyze Match Now")

with col_right:
    if match_btn:
        if uploaded_file and job_description:
            save_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with st.spinner("Analyzing..."):
                resume_data = parse_resume(save_path)
                result = match_resume_to_job(resume_data["skills"], job_description)

            score = result["match_score"]
            if score >= 70:
                color = "#34d399"
                verdict = "🟢 Strong Match"
                vc = "verdict-strong"
            elif score >= 40:
                color = "#fbbf24"
                verdict = "🟡 Moderate Match"
                vc = "verdict-medium"
            else:
                color = "#f87171"
                verdict = "🔴 Weak Match"
                vc = "verdict-weak"

            st.markdown(f"""
            <div class="glass-card">
              <div class="score-wrap">
                <div class="score-num" style="color:{color};">{score}%</div>
                <div class="score-label {vc}">{verdict}</div>
                <div class="score-bar-bg">
                  <div style="background:{color};width:{score}%;height:6px;border-radius:100px;"></div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="info-grid">
              <div class="info-item">
                <div class="info-item-label">Candidate</div>
                <div class="info-item-value">{resume_data['name']}</div>
              </div>
              <div class="info-item">
                <div class="info-item-label">Email</div>
                <div class="info-item-value">{resume_data['email']}</div>
              </div>
              <div class="info-item">
                <div class="info-item-label">Skills Found</div>
                <div class="info-item-value">{len(resume_data['skills'])} skills</div>
              </div>
              <div class="info-item">
                <div class="info-item-label">Job Requires</div>
                <div class="info-item-value">{len(result['job_skills'])} skills</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if result["matched_skills"]:
                tags = "".join([f'<span class="tag tag-green">✓ {s}</span>' for s in result["matched_skills"]])
                st.markdown(f'<div class="glass-card"><div class="skill-section-title"><span class="skill-dot" style="background:#34d399;"></span>Matched Skills — {len(result["matched_skills"])}</div>{tags}</div>', unsafe_allow_html=True)

            if result["missing_skills"]:
                tags = "".join([f'<span class="tag tag-red">✗ {s}</span>' for s in result["missing_skills"]])
                st.markdown(f'<div class="glass-card"><div class="skill-section-title"><span class="skill-dot" style="background:#f87171;"></span>Missing Skills — {len(result["missing_skills"])}</div>{tags}</div>', unsafe_allow_html=True)

            if resume_data["skills"]:
                tags = "".join([f'<span class="tag tag-blue">{s}</span>' for s in resume_data["skills"]])
                st.markdown(f'<div class="glass-card"><div class="skill-section-title"><span class="skill-dot" style="background:#60a5fa;"></span>All Resume Skills</div>{tags}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="empty-icon">👈</div><div class="empty-title">Almost there!</div><div class="empty-sub">Upload your resume and paste a job description to get started</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state"><div class="empty-icon">🎯</div><div class="empty-title">Ready to analyze</div><div class="empty-sub">Your match results will appear here instantly</div></div>', unsafe_allow_html=True)
