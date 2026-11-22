"""
School Help Guide — AI Assistant
IBM SkillsBuild AI Experiential Learning Lab | Team: Tech Orbit

Helps college students find the correct school services:
financial aid, tutoring, and academic advising.

Usage:
    python assistant.py

Requirements:
    pip install -r requirements.txt
    Copy env.example to .env and fill in your credentials.
"""

import json
import os
import sys

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()

API_KEY    = os.getenv("OPENAI_API_KEY", "")          # IBM Cloud API key
BASE_URL   = os.getenv("OPENAI_BASE_URL", "https://us-south.ml.cloud.ibm.com")
MODEL_NAME = os.getenv("MODEL_NAME", "ibm/granite-4-h-small")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")

# ── Load school services knowledge base ──────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(SCRIPT_DIR, "school_data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    SCHOOL_DATA = json.load(f)


def build_system_prompt(school_data: dict) -> str:
    """
    Build the system prompt by embedding the school services knowledge base
    so the AI only references verified, official information.
    """
    services_text = ""
    for svc in school_data["services"]:
        c = svc["contact"]
        # Only include contact fields that have a non-empty value
        contact_lines = "\n".join(
            line for line in [
                f"Location: {c['location']}" if c["location"] else "",
                f"Phone: {c['phone']}"       if c["phone"]    else "",
                f"Email: {c['email']}"       if c["email"]    else "",
            ] if line
        )
        bring = "\n".join(f"    - {item}" for item in svc["what_to_bring"])
        services_text += f"""
SERVICE: {svc['name']}
Description: {svc['description']}
{contact_lines}
Hours: {c['hours']}
Website: {c['website']}
SUGGESTED PREPARATION ONLY — these are NOT required documents. The student must confirm actual requirements directly with the office:
{bring}
Next steps: {svc['next_steps']}
---"""

    fallback = school_data["general_fallback"]
    fc = fallback["contact"]

    return f"""You are a friendly and helpful AI assistant for {school_data['school_name']}.
Your only job is to help college students find the correct school service office based on what they need.

RULES YOU MUST FOLLOW:
1. Your knowledge is strictly limited to the SCHOOL SERVICES section below. You MUST NOT use any
   external knowledge about CSUDH or any other institution — not phone numbers, not office names, not
   locations, not websites, not hours. If the information is not explicitly written in the SCHOOL
   SERVICES section, it does not exist for the purposes of this conversation. Never invent details and
   never use a contact field from one service when answering about a different service.
2. If a contact field (phone, email, location) is not shown for a service, do NOT display it and do NOT
   label it as missing or unavailable. Instead, tell the student to check the official website for that
   detail and show the website URL.
3. The items listed under "SUGGESTED PREPARATION ONLY" are suggestions, NOT official requirements. When
   presenting them, you MUST include this exact sentence: "Please confirm the actual requirements with
   the office before your visit." Never present these items as a required checklist.
4. For academic advising ONLY: before recommending any Student Success Center, you MUST first ask the
   student which college or major they belong to, unless they have already stated it in this conversation.
   Do not name, suggest, or recommend any specific center until the student has confirmed their college
   or major. This rule applies even when the student's question is otherwise clear.
5. If a student asks about two services in the same message, address both services fully — provide the
   relevant office information for each one in the same response. Do not ask a follow-up question when
   both needs are already clear.
6. If a student's question is unclear or genuinely ambiguous, ask ONE focused follow-up question before
   answering. Do not ask a follow-up if the student's need is already clear.
7. Never ask for the student's personal information (student ID number, GPA, grades, financial details).
8. If the student's need does not match any listed service, direct them to CSUDH Student Affairs using
   the fallback contact below.
9. Keep answers clear and concise — use short paragraphs or bullet points.
10. Use a warm, respectful tone. Students may be stressed or confused.

SCHOOL SERVICES:
{services_text}

FALLBACK — if no service matches:
When a student asks about anything not covered by the three services above, you MUST respond using
ONLY the message below — do not add, invent, or supplement it with any other information, phone
numbers, office names, locations, or URLs beyond https://www.csudh.edu:

"That's a great question! The School Help Guide currently covers financial aid, tutoring, and
academic advising. For other campus services, I recommend visiting the official CSUDH website
at https://www.csudh.edu — it has a full directory of campus offices and contact information.
You can also reach out to CSUDH Student Affairs for guidance."
"""


def chat(model: ModelInference, history: list[dict]) -> str:
    """Send the full conversation history to the model and return the reply."""
    response = model.chat(
        messages=history,
        params={
            "temperature": 0.3,   # low temperature = more consistent, factual answers
            "max_new_tokens": 512,
        },
    )
    return response["choices"][0]["message"]["content"].strip()


def run():
    """Main conversation loop."""
    if not API_KEY:
        print(
            "\n[ERROR] No IBM Cloud API key found.\n"
            "Copy env.example to .env and add your credentials, then run again.\n"
        )
        sys.exit(1)

    if not PROJECT_ID:
        print(
            "\n[ERROR] No WATSONX_PROJECT_ID found.\n"
            "Add your watsonx.ai project ID to .env, then run again.\n"
        )
        sys.exit(1)

    credentials = Credentials(url=BASE_URL, api_key=API_KEY)
    model = ModelInference(
        model_id=MODEL_NAME,
        credentials=credentials,
        project_id=PROJECT_ID,
        params={"temperature": 0.3, "max_new_tokens": 512},
    )

    system_prompt = build_system_prompt(SCHOOL_DATA)
    # watsonx.ai Granite supports a system message as the first history entry
    history = [{"role": "system", "content": system_prompt}]

    print("=" * 60)
    print("  School Help Guide — AI Assistant")
    print(f"  {SCHOOL_DATA['school_name']} | Team: Tech Orbit")
    print("=" * 60)
    print("  Type your question and press Enter.")
    print("  Type 'quit' or 'exit' to end the session.")
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSession ended. Good luck with your studies!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye", "q"}:
            print("\nAssistant: Take care! Reach out any time you need help. Good luck!")
            break

        # Add student message to history
        history.append({"role": "user", "content": user_input})

        # Get AI response
        try:
            reply = chat(model, history)
        except Exception as e:
            print(f"\n[ERROR] Could not reach the AI model: {e}\n")
            # Remove the failed user message so history stays clean
            history.pop()
            continue

        # Add assistant reply to history (keeps context across turns)
        history.append({"role": "assistant", "content": reply})

        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    run()