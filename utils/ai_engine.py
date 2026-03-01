import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def identify_persona(resume_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Analyze the resume and return exactly ONE category: Software Engineering, Hardware Engineering, Product Management, Operations, Sales, Marketing."),
        ("user", "{resume}")
    ])
    chain = prompt | llm
    return chain.invoke({"resume": resume_text[:5000]}).content.strip()


def generate_email(resume_text, company_name, persona):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are applying for a job. Write a formal cold email (max 100 words) to the recruiter. Focus on top, most mentioned skill from the resume. Use a professional tone and avoid generic phrases."),
        ("user", "Resume: {resume}\nCompany: {company}\nRole: {role}\n\nFormat:\nSUBJECT: [Subject]\nBODY: [Body]")
    ])
    chain = prompt | llm
    res = chain.invoke({"resume": resume_text[:2500], "company": company_name, "role": persona}).content
    try:
        if "BODY:" in res:
            parts = res.split("BODY:")
            subject = parts[0].replace("SUBJECT:", "").strip()
            body = parts[1].strip()
            return subject, body
        else:
            subject = f"Strategic Inquiry: {persona} Role @ {company_name}"
            body = res.strip()
            return subject, body
    except:
        return f"Application: {persona}", res