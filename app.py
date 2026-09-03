import sqlite3
import time
import math
import secrets 
import markupsafe
from flask import Flask, redirect, render_template, request, session, abort, make_response, g, flash
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import forum
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        abort(403)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    total_threads = forum.thread_count()
    page_count = math.ceil(total_threads / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    threads = forum.get_threads(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, threads=threads)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
            
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: Antamasi salasanat eivät ole samat")
            return render_template("register.html", filled={"username": username})

        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
            flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
            return redirect("/")
        except sqlite3.IntegrityError:
            flash("VIRHE: Valitsemasi tunnus on jo varattu")
            return render_template("register.html", filled={"username": username})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        
        if result and check_password_hash(result[0]["password_hash"], password):
            session["username"] = username
            session["user_id"] = result[0]["id"]
            session["csrf_token"] = secrets.token_hex(16)
            
            return redirect(next_page if next_page else "/")
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return render_template("login.html", next_page=next_page)


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]

    if "csrf_token" in session:
        del session["csrf_token"]
    return redirect("/")

@app.route("/new_thread", methods=["POST"])
def new_thread():
    require_login()
    check_csrf() 
    
    title = request.form["title"]
    content = request.form["content"]
    
    if not title or len(title) > 100 or len(content) > 5000:
        abort(403)
        
    user_id = session["user_id"]

    thread_id = forum.add_thread(title, content, user_id)
    return redirect("/thread/" + str(thread_id))

@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    thread = forum.get_thread(thread_id)

    if not thread:
        abort(404)
        
    messages = forum.get_messages(thread_id)
    return render_template("thread.html", thread=thread, messages=messages)

@app.route("/new_message", methods=["POST"])
def new_message():
    require_login()
    check_csrf() 
    
    content = request.form["content"]
    user_id = session["user_id"]
    thread_id = request.form["thread_id"]
    
    if not content or len(content) > 5000:
        abort(403)

    try:
        forum.add_message(content, user_id, thread_id)
    except sqlite3.IntegrityError:
        abort(403)
        
    return redirect("/thread/" + str(thread_id))

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    require_login()
    message = forum.get_message(message_id)
    
    if not message:
        abort(404)
        
    if message["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", message=message)

    if request.method == "POST":
        check_csrf() 
        content = request.form["content"]
        if not content or len(content) > 5000:
            abort(403)
        forum.update_message(message["id"], content)
        return redirect("/thread/" + str(message["thread_id"]))

@app.route("/remove/<int:message_id>", methods=["GET", "POST"])
def remove_message(message_id):
    require_login()
    message = forum.get_message(message_id)
    
    if not message:
        abort(404)
        
    if message["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", message=message)

    if request.method == "POST":
        check_csrf() 
        if "continue" in request.form:
            forum.remove_message(message["id"])
        return redirect("/thread/" + str(message["thread_id"]))

@app.route("/search")
def search():
    query = request.args.get("query")
    results = forum.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    messages = users.get_messages(user_id)
    return render_template("user.html", user=user, messages=messages)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_image.html")

    if request.method == "POST":
        check_csrf() 
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: Lähettämäsi tiedosto ei ole jpg-tiedosto")
            return redirect("/add_image")

        image = file.read()
        if len(image) > 100 * 1024:
            flash("VIRHE: Lähettämäsi tiedosto on liian suuri")
            return redirect("/add_image")

        user_id = session["user_id"]
        users.update_image(user_id, image)
        flash("Kuvan lisääminen onnistui")
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response