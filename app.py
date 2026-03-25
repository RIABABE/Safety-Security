import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/safety-chat")
def safety_chat():
    return render_template("safeher_live.html")

@app.route("/api/chat", methods=["POST"])
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "SafeGuard AI"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {
                        "role": "system",
                        "content": data.get("system", "You are SafeHer, a compassionate personal safety assistant for women in Nigeria. Give detailed, helpful, specific answers about personal safety, mental health, legal rights, and emergency support.")
                    }
                ] + data.get("messages", [])
            }
        )
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({
            "content": [{"text": reply}]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
