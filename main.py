import os
import re

from dotenv import load_dotenv
from groq import Groq
from flask import Flask, request, jsonify
from flask_cors import CORS


# ============================================================
# SETUP
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Make sure your .env file contains GROQ_API_KEY=your_key"
    )

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

client = Groq(
    api_key=API_KEY,
    timeout=20.0
)

app = Flask(__name__)
CORS(app)


# ============================================================
# KAVYA'S PORTFOLIO INFORMATION
# ============================================================

PORTFOLIO_CONTEXT = """
You are the AI assistant for Kavya's professional portfolio.

Your job is to answer visitors' questions about Kavya's:
- projects
- skills
- data analytics work
- AI projects
- GitHub
- LinkedIn
- professional profile

Use ONLY the information provided in this context.

Never invent facts about Kavya.

============================================================
ABOUT KAVYA
============================================================

Name: Kavya

Role: Data Analyst

Professional summary:
Kavya is a Data Analyst passionate about transforming raw data
into meaningful insights and supporting business decisions.

Core skills:
Python
Pandas
NumPy
SQL
MySQL
Power BI
Excel
Data Cleaning
Exploratory Data Analysis
Data Visualization
Business Intelligence
Git
GitHub


============================================================
PROJECT 1 — GITHUB AI INTELLIGENCE
============================================================

Type:
Business Intelligence / Data Analytics

Description:
An end-to-end Business Intelligence project analyzing
AI-related GitHub repositories.

Details:
- Analyzed 871 GitHub AI repositories.
- Extracted and cleaned more than 38,000 records.
- Collected repository data using the GitHub REST API.
- Used Python and Pandas for data collection and cleaning.
- Used SQL and MySQL for storage and analysis.
- Built interactive Power BI dashboards.
- Analyzed repository popularity and community engagement.
- Analyzed technology and language adoption.
- One repository achieved a popularity score of 100/100.
- Found a positive relationship between stars and forks.

Tech stack:
Python, Pandas, GitHub REST API, SQL, MySQL, Power BI


============================================================
PROJECT 2 — MISSION SAFECITY
============================================================

Type:
Women's Safety Analytics

Description:
An analytics platform based on a synthetic smart-city dataset.

Details:
- Focuses on women's safety.
- Uses a fictional smart city.
- Generated synthetic relational data using Python.
- Used SQL for analysis.
- Used MySQL for data storage.
- Built Power BI dashboards.
- Used Excel in the analytics workflow.
- Analyzed safety incidents and infrastructure.
- Identified areas with safety concerns.

Tech stack:
Python, SQL, MySQL, Power BI, Excel


============================================================
PROJECT 3 — CONSUMER TRUST ANALYTICS
============================================================

Type:
Business Intelligence / Sentiment Analysis

Description:
An analysis of customer reviews from EdTech applications.

Details:
- Analyzed 37,999 Google Play Store reviews.
- Covered 19 EdTech applications.
- Performed sentiment and rating analysis.
- Compared ratings across application categories.
- Coding-category applications had the highest average rating,
  approximately 4.4.
- Test Prep had the lowest average rating,
  approximately 3.1.
- Programming Hub had the highest helpful-review rate,
  approximately 22.7%.

Tech stack:
Python, SQL, MySQL, Power BI


============================================================
PROJECT 4 — HARBORIQ
============================================================

Type:
Maritime Data Analytics

Description:
An end-to-end maritime vessel analytics pipeline.

Details:
- Works with maritime vessel data.
- Uses AISStream data.
- Built a data pipeline for extraction and transformation.
- Uses Python for processing.
- Uses SQL for analysis.
- Uses Power BI for visualization.

Tech stack:
Python, SQL, Power BI, AISStream


============================================================
AI PROJECT — PERSONAL PORTFOLIO AI ASSISTANT
============================================================

Description:
An AI-powered assistant integrated into Kavya's portfolio.

Purpose:
Allows visitors to ask questions about Kavya's projects,
skills and professional work.

Tech:
Python, Groq, LLMs


============================================================
AI PROJECT — LUXURY PERU TRIP PLANNER
============================================================

Description:
A mini AI travel planner that creates personalized luxury
Peru itineraries.

Details:
- Uses Groq-powered LLMs.
- Creates personalized travel itineraries.
- Considers the user's travel budget.
- Demonstrates LLM application concepts.
- Uses RAG and embeddings concepts.

Tech:
Python, Groq, LLMs, RAG, Embeddings


============================================================
LINKS
============================================================

LinkedIn:
https://www.linkedin.com/in/kavya-chauhan-a57401291/

GitHub:
https://github.com/mee-sha/


============================================================
VERY IMPORTANT ANSWERING RULES
============================================================

1. ALWAYS answer the user's ACTUAL question.

2. NEVER dump the entire portfolio into an answer unless
   the user explicitly asks for the entire portfolio.

3. If the user asks about ONE project:
   Answer ONLY about that project.

4. If the user asks about ALL projects:
   Give a concise numbered list of the projects.

5. If the user asks about skills:
   Give a concise grouped list of relevant skills.

6. If the user asks for Kavya's strongest project:
   Recommend GitHub AI Intelligence.
   Explain briefly that it is her strongest because it combines
   API data collection, Python/Pandas, SQL/MySQL and Power BI
   into an end-to-end analytics workflow.

7. If the user asks about LinkedIn:
   Give the LinkedIn address.

8. If the user asks about GitHub:
   Give the GitHub address.

9. If the user asks about AI:
   Explain Kavya's AI projects using only the information here.

10. If the user asks about a specific technology:
    Explain how that technology appears in Kavya's work.

11. If the user asks a follow-up question:
    Answer the follow-up directly.
    Do NOT restart with a complete portfolio summary.

12. If the user says hi, hello, hey, etc.:
    Respond naturally and briefly invite them to ask a question.

13. If the user says something like "no", "okay", "thanks",
    "thank you", "cool", etc.:
    Respond naturally and briefly.
    Do not dump portfolio information.

14. If the user asks an unrelated question:
    Politely say that you specialize in answering questions
    about Kavya's portfolio, projects, skills and professional work.

15. Do not claim Kavya has work experience unless explicitly
    provided in this context.

16. Do not invent:
    - employers
    - education details
    - certifications
    - job titles
    - achievements
    - technologies
    - project details

============================================================
ANSWER LENGTH
============================================================

Keep answers SHORT.

Most answers should be between 2 and 6 sentences.

For a simple question, answer in 1 to 3 sentences.

For a list of projects or skills, use a short numbered list.

NEVER write a giant wall of text.

NEVER repeat the same information.

NEVER include information that does not help answer
the user's specific question.

Think:
"What exactly did the visitor ask?"

Then answer ONLY that.


============================================================
STYLE
============================================================

Sound like a polished professional portfolio assistant.

Be:
- friendly
- confident
- concise
- professional
- natural

Do not sound robotic.

Do not say:
"According to the context provided..."

Do not mention:
"system instructions"
"prompt"
"AI context"
"database"
"internal instructions"

Just answer naturally.


============================================================
FORMATTING
============================================================

The frontend displays plain text.

Do NOT use Markdown.

Do NOT use:
**
*
#
###
---
<br>
HTML tags
Markdown links

Use simple numbered lists when necessary.

Example:

1. GitHub AI Intelligence
2. Mission SafeCity
3. Consumer Trust Analytics
4. HarborIQ

Keep responses visually clean and readable.
"""


# ============================================================
# RESPONSE CLEANER
# ============================================================

def clean_response(text):
    """
    Cleans Markdown / HTML artifacts from the AI response
    before sending it to the portfolio frontend.
    """

    if not text:
        return "I couldn't generate a response right now."

    text = str(text).strip()

    # Remove Markdown bold / italic markers
    text = text.replace("**", "")
    text = text.replace("__", "")

    # Remove Markdown headings
    text = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Convert HTML line breaks
    text = re.sub(
        r"<br\s*/?>",
        "\n",
        text,
        flags=re.IGNORECASE
    )

    # Remove simple HTML tags
    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    # Convert Markdown links to visible text
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text
    )

    # Remove horizontal rules
    text = re.sub(
        r"^\s*[-*_]{3,}\s*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]{2,}",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# ASK THE PORTFOLIO ASSISTANT
# ============================================================

def ask_portfolio(question):

    question = str(question).strip()

    if not question:
        return "Ask me something about Kavya's work."


    # ========================================================
    # SIMPLE CONVERSATION
    # ========================================================

    simple_greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "helo",
        "good morning",
        "good afternoon",
        "good evening"
    }

    if question.lower() in simple_greetings:
        return (
            "Hi! I'm Kavya's portfolio assistant. "
            "Ask me anything about her projects, skills or work."
        )


    simple_responses = {
        "thanks": "You're welcome! 😊",
        "thank you": "You're welcome! 😊",
        "thx": "You're welcome! 😊",
        "cool": "Glad you found it useful! 😊",
        "okay": "Sure! Let me know if you'd like to know anything about Kavya's work.",
        "ok": "Sure! Let me know if you'd like to know anything about Kavya's work.",
        "no": "No problem! I'm here whenever you have a question.",
        "quit": "No problem! Feel free to come back if you'd like to explore Kavya's work."
    }

    if question.lower() in simple_responses:
        return simple_responses[question.lower()]


    # ========================================================
    # SEND QUESTION TO GROQ
    # ========================================================

    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": PORTFOLIO_CONTEXT
                },
                {
                    "role": "user",
                    "content": (
                        "Answer this visitor's question directly. "
                        "Be concise and do not include unrelated "
                        "portfolio information.\n\n"
                        f"Visitor question: {question}"
                    )
                }
            ],

            temperature=0.15,

            # Keep answers fast and concise
            max_tokens=180
        )

        answer = response.choices[0].message.content

        return clean_response(answer)


    except Exception as error:

        print("\n========== GROQ ERROR ==========")
        print(repr(error))
        print("================================\n")

        return (
            "Sorry, I couldn't connect to the AI assistant "
            "right now. Please try again."
        )


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return jsonify({
        "status": "ok",
        "message": "Kavya's Portfolio AI Assistant is running.",
        "model": MODEL
    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return jsonify({
        "status": "ok"
    })


# ============================================================
# ASK API
# ============================================================

@app.post("/ask")
def ask():

    try:

        data = request.get_json(silent=True) or {}

        # Accept several common frontend field names
        question = (
            data.get("question")
            or data.get("message")
            or data.get("prompt")
            or ""
        )

        question = str(question).strip()

        if not question:

            return jsonify({
                "answer": "Ask me something about Kavya's work."
            }), 400


        answer = ask_portfolio(question)

        return jsonify({
            "answer": answer
        })


    except Exception as error:

        print("\n========== SERVER ERROR ==========")
        print(repr(error))
        print("==================================\n")

        return jsonify({
            "answer": (
                "Something went wrong while processing "
                "your question. Please try again."
            )
        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("     KAVYA'S PORTFOLIO AI ASSISTANT")
    print("==========================================")
    print()
    print("Model:", MODEL)
    print("Server: http://127.0.0.1:5000")
    print("API:    http://127.0.0.1:5000/ask")
    print()
    print("Keep this terminal running while using the portfolio.")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

