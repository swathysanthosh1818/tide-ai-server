from flask_cors import CORS
from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)
CORS(app)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/plan", methods=["POST"])
def plan():
    tasks = request.json["tasks"]
    lines = "\n".join(f"- {t}" for t in tasks)
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            system="You are Tide's planning assistant. Be concise.",
            messages=[{"role": "user", "content": f"Order these tasks by urgency, one reason each:\n{lines}"}],
        )
        text = msg.content[0].text or "Tackle the oldest task first."
    except Exception:
        text = "The assistant is busy. Try again in a moment."
    return jsonify({"plan": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
