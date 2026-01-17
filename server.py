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
