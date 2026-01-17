import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = OpenAI(api_key=os.getenv("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"))

@app.route("/")
def home():
    return "Studex AI backend running"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_text = data.get("message","")
    mode = data.get("mode","student")

    if mode == "student":
        system_prompt = "You are Studex AI for students. Explain simply with examples."
    elif mode == "teacher":
        system_prompt = "You are Studex AI for teachers. Give structured lesson plans and activities."
    else:
        system_prompt = "You are Studex AI for parents. Give simple learning guidance."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content": system_prompt},
            {"role":"user","content": user_text}
        ]
    )

    return jsonify({"reply": response.choices[0].message.content})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
