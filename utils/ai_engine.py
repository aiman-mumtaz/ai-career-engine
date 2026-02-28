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
        ("system", "You are an elite Indian career agent. Write a punchy cold email (max 100 words). Mention the company and one specific skill from the resume. Use a professional yet bold tone."),
        ("user", "Resume: {resume}\nCompany: {company}\nRole: {role}\n\nFormat:\nSUBJECT: [Subject]\nBODY: [Body]")
    ])
    chain = prompt | llm
    res = chain.invoke({"resume": resume_text[:3000], "company": company_name, "role": persona}).content
    try:
        subject = res.split("BODY:")[0].replace("SUBJECT:", "").strip()
        body = res.split("BODY:")[1].strip()
        return subject, body
    except:
        return f"Application for {persona} role", res