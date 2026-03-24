import dotenv
from flask import Flask, render_template, request, jsonify
import anthropic
import os
from dotenv import load_dotenv
import flask

load_dotenv()

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are SafeGuard AI, a compassionate, calm, and highly knowledgeable personal safety assistant built specifically for women and vulnerable individuals in Nigeria and across Africa.

Your core responsibilities:
1. EMERGENCY GUIDANCE: When someone is in immediate danger, give clear, numbered, actionable steps first. Always mention Nigerian emergency numbers: Police 112, National Emergency 199, Lagos State 767.
2. PERSONAL SAFETY TIPS: Provide practical, Nigeria-specific safety advice for everyday situations.
3. INCIDENT REPORTING: Guide users through how to report crimes, harassment, or violence to Nigerian authorities.
4. MENTAL WELLNESS: Offer empathetic support and coping strategies for trauma and distress.
5. CYBER SAFETY: Advise on protecting personal information and handling online harassment.
6. LEGAL RIGHTS: Explain relevant Nigerian laws protecting women (VAPP Act) in simple language.

Tone guidelines:
- Be warm, calm, and non-judgmental at all times
- In emergencies: be direct, numbered, clear
- Use simple, accessible English
- Show empathy before giving advice when someone is distressed

Formatting:
- Use short paragraphs and numbered steps for clarity
- Bold key actions using **bold**
- Keep responses focused and actionable"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        messages = data.get("messages", [])

        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        ai_reply = response.content[0].text
        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "SafeGuard AI is running"})


if __name__ == "__main__":
    print("SafeGuard AI is starting...")
    print("Open your browser: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)



## 📄 FILE 2: `requirements.txt`
flask==3.0
anthropic==0.34
python-dotenv==1.0




## 📄 FILE 3: `.env` (Create this file, never share it publicly)
ANTHROPIC_API_KEY=your_anthropic_api_key_here