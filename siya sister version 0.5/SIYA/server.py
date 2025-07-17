# server.py
from flask import Flask, request, render_template
from brain.logic import generate_reply, update_mood, remember_chat
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/siya')
def siya_reply():
    msg = request.args.get("msg", "")
    if not msg:
        return "👧 Siya: Kuch toh bolo jaan 💖"
    update_mood(msg)
    reply = generate_reply(msg)
    remember_chat(msg, reply)
    return reply

if __name__ == "__main__":
    print("🧠 Siya's Web Brain running at http://localhost:7860")
    app.run(host="0.0.0.0", port=7860)
