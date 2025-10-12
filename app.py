from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    words = ["apina", "banaani", "cembalo"]
    return render_template("index.html", message="Tervetuloa!", items=words)

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    message = request.form["message"]
    return render_template("result.html", message=message)
