from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1500
    )
    return response.choices[0].message.content

def get_fit_score(resume: str, jd: str) -> float:
    result = call_groq(
        "You are a recruitment expert. Return ONLY a number between 0 and 100. No explanation, no text, just the number.",
        f"Score this resume against the job description.\n\nJOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"
    )
    try:
        return float(''.join(filter(lambda x: x.isdigit() or x == '.', result)))
    except:
        return 0.0

def get_gap_analysis(resume: str, jd: str) -> str:
    return call_groq(
        "You are a career coach. Be specific, actionable, and concise.",
        f"List the skill gaps between this resume and job description. Format as bullet points.\n\nJOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"
    )

def get_interview_questions(resume: str, jd: str) -> str:
    return call_groq(
        "You are a senior technical interviewer.",
        f"Generate 8 targeted interview questions for this candidate based on their resume and the job description. Mix technical and behavioral questions.\n\nJOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"
    )

def get_cover_letter(resume: str, jd: str) -> str:
    return call_groq(
        "You are an expert cover letter writer. Write professionally and concisely.",
        f"Write a tailored cover letter.\n\nJOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"
    )

def get_rewritten_resume(resume: str, jd: str) -> str:
    return call_groq(
        "You are an expert resume writer. Optimize for ATS and relevance.",
        f"Rewrite this resume to better match the job description. Keep it professional.\n\nJOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"
    )
