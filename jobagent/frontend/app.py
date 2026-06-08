import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Recruitment Platform", layout="wide")
st.title("🎯 AI Recruitment Platform")
st.caption("RAG-powered candidate screening using Claude API")

def safe_get(url, **kwargs):
    try:
        res = requests.get(url, **kwargs)
        return res.json() if res.content else []
    except Exception as e:
        st.error(f"Backend error: {e}")
        return []

def safe_post(url, **kwargs):
    try:
        res = requests.post(url, **kwargs)
        return res
    except Exception as e:
        st.error(f"Backend error: {e}")
        return None

# SIDEBAR NAVIGATION
page = st.sidebar.selectbox("Navigate", [
    "➕ Add Candidate",
    "📋 Post Job",
    "🏆 Rank Candidates",
    "🤖 AI Analysis",
    "📊 View All"
])

# ADD CANDIDATE
if page == "➕ Add Candidate":
    st.header("➕ Add Candidate")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    uploaded_file = st.file_uploader("Upload Resume (.txt)", type=["txt"])
    resume_text = ""
    if uploaded_file:
        resume_text = uploaded_file.read().decode("utf-8")
    else:
        resume_text = st.text_area("Or paste resume text", height=250)

    if st.button("Add Candidate"):
        if not name or not email or not resume_text:
            st.error("All fields are required.")
        else:
            res = safe_post(f"{API_URL}/candidates", json={
                "name": name,
                "email": email,
                "resume_text": resume_text
            })
            if res and res.status_code == 200:
                st.success(f"✅ Candidate **{name}** added and resume embedded!")
                st.json(res.json())
            elif res:
                try:
                    st.error(res.json().get("detail", "Error adding candidate"))
                except:
                    st.error(f"Error: {res.status_code} - {res.text}")

# POST JOB
elif page == "📋 Post Job":
    st.header("📋 Post a Job Description")
    title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    description = st.text_area("Job Description", height=250)

    if st.button("Post Job"):
        if not title or not company or not description:
            st.error("All fields are required.")
        else:
            res = safe_post(f"{API_URL}/jobs", json={
                "title": title,
                "company": company,
                "description": description
            })
            if res and res.status_code == 200:
                st.success(f"✅ Job **{title}** posted!")
                st.json(res.json())
            elif res:
                st.error(f"Error: {res.status_code} - {res.text}")

# RANK CANDIDATES (RAG)
elif page == "🏆 Rank Candidates":
    st.header("🏆 RAG-Based Candidate Ranking")
    jobs = safe_get(f"{API_URL}/jobs")
    if not jobs:
        st.warning("No jobs posted yet. Please post a job first.")
    else:
        job_map = {f"{j['title']} @ {j['company']}": j['id'] for j in jobs}
        selected_job = st.selectbox("Select Job", list(job_map.keys()))

        if st.button("Rank Candidates"):
            jd_id = job_map[selected_job]
            res = safe_get(f"{API_URL}/jobs/{jd_id}/rank-candidates")
            if res and "ranked_candidates" in res:
                st.subheader(f"Top Matches for: {res['job_title']}")
                for c in res["ranked_candidates"]:
                    with st.expander(f"🥇 Rank {c['rank']} — {c['name']} ({c['email']})"):
                        st.write(f"**Similarity Score:** {round(1 - c['similarity_distance'], 2)}")
                        st.write(f"**Candidate ID:** {c['candidate_id']}")
            else:
                st.info("No candidates found or no results.")

# AI ANALYSIS
elif page == "🤖 AI Analysis":
    st.header("🤖 Full AI Analysis Pipeline")

    col1, col2 = st.columns(2)

    with col1:
        candidates = safe_get(f"{API_URL}/candidates")
        if not candidates:
            st.warning("No candidates added yet.")
            st.stop()
        candidate_map = {f"{c['name']} ({c['email']})": c['id'] for c in candidates}
        selected_candidate = st.selectbox("Select Candidate", list(candidate_map.keys()))

    with col2:
        jobs = safe_get(f"{API_URL}/jobs")
        if not jobs:
            st.warning("No jobs posted yet.")
            st.stop()
        job_map = {f"{j['title']} @ {j['company']}": j['id'] for j in jobs}
        selected_job = st.selectbox("Select Job", list(job_map.keys()))

    if st.button("▶ Run Full AI Pipeline"):
        with st.spinner("Running AI analysis... this takes ~30 seconds"):
            res = safe_post(f"{API_URL}/analyze", json={
                "candidate_id": candidate_map[selected_candidate],
                "jd_id": job_map[selected_job]
            })

        if res and res.status_code == 200:
            data = res.json()
            st.success(f"✅ Analysis complete for **{data['candidate']}** → **{data['job']}**")
            st.metric("🎯 Fit Score", f"{data['fit_score']} / 100")

            st.subheader("🔍 Gap Analysis")
            st.write(data["gap_analysis"])

            st.subheader("❓ Interview Questions")
            st.write(data["interview_questions"])

            st.subheader("✉️ Cover Letter")
            st.write(data["cover_letter"])

            st.subheader("📄 Rewritten Resume")
            st.write(data["rewritten_resume"])
        elif res:
            try:
                st.error(f"Error: {res.json().get('detail', 'Something went wrong')}")
            except:
                st.error(f"Error {res.status_code}: {res.text}")

# VIEW ALL
elif page == "📊 View All":
    st.header("📊 Database Overview")

    st.subheader("👥 All Candidates")
    candidates = safe_get(f"{API_URL}/candidates")
    if candidates:
        for c in candidates:
            st.write(f"**{c['id']}** — {c['name']} | {c['email']}")
    else:
        st.info("No candidates yet.")

    st.divider()

    st.subheader("💼 All Jobs")
    jobs = safe_get(f"{API_URL}/jobs")
    if jobs:
        for j in jobs:
            st.write(f"**{j['id']}** — {j['title']} @ {j['company']}")
    else:
        st.info("No jobs yet.")
