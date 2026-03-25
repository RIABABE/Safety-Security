from tkinter.filedialog import Open
from tkinter.messagebox import IGNORE

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "messages" not in data:
            return jsonify({"error": "Missing 'messages' in request"}), 400

        # Example dummy AI response (you’ll plug in Anthropic later)
        user_message = data["messages"][-1]["content"]

        reply = (
            "This is a test reply from your safety assistant.\n\n"
            "If you are in immediate danger:\n"
            "- Try to move to a safe, visible place (e.g., shop, police post, filling station).\n"
            "- Call 112 (Police) or 199 (National Emergency) and clearly state your location.\n"
            "- Share your live location with a trusted contact via WhatsApp or Telegram.\n\n"
            "If you are not in immediate danger, still document what happened and consider reaching out to support services."
        )

        return jsonify({
            "response": reply.strip(),
            "timestamp": "now"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "SafeGuard AI is running"}), 200

@app.route('/safety-chat')
def safety_chat():
    return render_template('safeher_live.html')

import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/safety-chat')
def safety_chat():
    return render_template('safeher_live.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={
            'Content-Type': 'application/json',
            'x-api-key': os.getenv('ANTHROPIC_API_KEY'),
            'anthropic-version': '2023-06-01'
        },
        json={
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 1000,
            'system': data.get('system'),
            'messages': data.get('messages')
        }
    )
    
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
