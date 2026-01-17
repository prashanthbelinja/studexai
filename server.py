import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("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"))

@app.route("/")
def home():
    return "Studex AI backend running"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)

        user_text = data.get("message", "")
        mode = data.get("mode", "student")

        if not user_text:
            return jsonify({"reply": "Please type a question."})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Studex AI educational assistant."},
                {"role": "user", "content": user_text}
            ]
        )

        return jsonify({"reply": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"reply": "Backend error: " + str(e)})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
