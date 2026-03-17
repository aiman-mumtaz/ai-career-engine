# 🍄 Career Liaison: AI Cold Email Agent

**Career Liaison** is an elite automated outreach tool designed to bridge the gap between candidates and recruiters. By leveraging LLMs and the "Power-Ups" found in your resume, it generates personalized, punchy cold emails and delivers them directly to hiring teams.

## Features

* **Resume Intelligence**: Parses your PDF resume to extract key "Power-Ups" (skills).
* **Persona-Driven Generation**: Uses an elite AI agent to draft bold, professional cold emails under 100 words.
* **Automated Delivery**: Integrated SMTP support to fire off emails instantly.
* **Mission Control**: A Streamlit-based dashboard to manage company lists and track outreach progress.
* **Safety Features**: Includes "Stop/Reset" functionality to halt automated processes at any time.

---

## Technical Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Orchestration**: [LangChain](https://www.langchain.com/)
* **LLM**: Google Gemini / OpenAI (via LangChain)
* **Mailing**: Python `smtplib` with MIME support
* **Secrets**: Streamlit Secrets Management

---

## Installation & Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/career-liaison.git
cd career-liaison

```

### 2. Install Dependencies

```bash
pip install streamlit langchain-core langchain-google-genai PyPDF2

```

### 3. Configuration (Secrets)

Create a folder named `.streamlit` and add a `secrets.toml` file. This is crucial for the mailer to work.

```toml
# .streamlit/secrets.toml

[smtp]
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_email = "your-email@gmail.com"
smtp_password = "your-16-char-app-password"

[GOOGLE_API_KEY]
api_key = "your-gemini-api-key"

```

---

## How to Use

1. **Launch the App**:
```bash
streamlit run app.py

```


2. **Upload Resume**: Drop your PDF resume into the sidebar.
3. **Target Companies**: Enter the company name and recruiter email.
4. **Fire Away**: Click **"Start Mission"** to generate and send.
5. **Emergency Stop**: Use the **"Stop"** button to immediately halt the process.

---

## Project Structure

```text
├── .streamlit/
│   └── secrets.toml      
├── utils/
│   └── mailer.py       
├── app.py               
├── requirements.txt    
└── README.md             # You are here

```

---

## Security Note

This project uses **App Passwords**.

* **Never** commit your `.streamlit/secrets.toml` to GitHub.
* Ensure your `.gitignore` includes `.streamlit/secrets.toml`.
* For Gmail, you **must** use a 16-character App Password, not your standard account password.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
