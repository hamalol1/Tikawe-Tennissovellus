from flask import Flask, redirect, render_template, request
import db

app = Flask(__name__)

@app.route("/")
def index():
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")
    visits_result = db.query("SELECT COUNT(*) FROM visits")
    visit_count = visits_result[0][0]
    
    messages = db.query("SELECT content FROM messages")
    message_count = len(messages)
    
    return render_template("index.html", visit_count=visit_count, count=message_count, messages=messages)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    db.execute("INSERT INTO messages (content) VALUES (?)", [content])
    return redirect("/")