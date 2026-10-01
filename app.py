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
from datetime import datetime, timedelta

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
    if "user_id" not in session:
        flash("Kirjaudu sisään nähdäksesi avoimet pelivuorot.")
        return redirect("/login")

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
        username = request.form["username"].strip()
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if not username or " " in username:
            flash("VIRHE: Käyttäjänimi ei saa olla tyhjä tai sisältää välilyöntejä")
            return render_template("register.html", filled={"username": username})

        if len(username) > 16:
            flash("VIRHE: Käyttäjänimi saa olla enintään 16 merkkiä pitkä")
            return render_template("register.html", filled={"username": username})
            
        if " " in password1:
            flash("VIRHE: Salasana ei saa sisältää välilyöntejä")
            return render_template("register.html", filled={"username": username})

        if len(password1) < 4:
            flash("VIRHE: Salasanan pitää olla vähintään 4 merkkiä pitkä")
            return render_template("register.html", filled={"username": username})

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
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])
        
        if result and check_password_hash(result[0]["password_hash"], password):
            user_id = result[0]["id"]
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            
            flash("Kirjautuminen onnistui!")
            return redirect("/user/" + str(user_id))
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return render_template("login.html", filled_username=username)

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]

    if "csrf_token" in session:
        del session["csrf_token"]
    return redirect("/")

@app.route("/new_thread", methods=["GET", "POST"])
def new_thread():
    require_login()

    if request.method == "GET":
        nyt = datetime.now()
        seuraava_tunti = (nyt + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        min_time = seuraava_tunti.strftime("%Y-%m-%dT%H:%M")
        return render_template("new_thread.html", min_time=min_time)

    if request.method == "POST":
        check_csrf() 
        
        play_time_raw = request.form["play_time"]
        location = request.form["location"]
        skill_level = request.form["skill_level"]
        player_count = request.form["player_count"]
        duration = request.form["duration"]
        content = request.form["content"]
        
        try:
            dt = datetime.strptime(play_time_raw, "%Y-%m-%dT%H:%M")
            if dt < datetime.now():
                flash("Peliajan on oltava tulevaisuudessa.")
                return redirect("/new_thread")
                
            dt = dt.replace(minute=0)
            play_time = dt.strftime("%d.%m.%Y klo %H:%M")
        except ValueError:
            abort(403)
        
        allowed_locations = ["Kimpisen massatenniskentät", "Huhtiniemen sisähalli"]
        allowed_levels = ["Aloittelija", "Keskitaso", "Kilpa"]
        
        try:
            p_count = int(player_count)
            duration_h = int(duration)
        except ValueError:
            abort(403)
            
        if location not in allowed_locations or skill_level not in allowed_levels or p_count < 1 or p_count > 4 or duration_h < 1 or duration_h > 10:
            abort(403)
            
        if not play_time or len(content) > 5000:
            abort(403)
            
        user_id = session["user_id"]

        forum.add_thread(play_time, location, skill_level, p_count, duration_h, content, user_id)
        
        flash("Pelivuoro ilmoitettu onnistuneesti!")
        return redirect("/")

@app.route("/thread/<int:thread_id>")
def show_thread(thread_id):
    if "user_id" not in session:
        flash("Kirjaudu sisään nähdäksesi ilmoituksen tarkemmat tiedot.")
        return redirect("/login")

    thread = forum.get_thread(thread_id)
    if not thread:
        abort(404)
        
    messages = forum.get_messages(thread_id)
    participants = forum.get_participants(thread_id)
    
    is_participant = any(p["id"] == session["user_id"] for p in participants)
    
    return render_template("thread.html", thread=thread, messages=messages, participants=participants, is_participant=is_participant)

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

@app.route("/remove_thread/<int:thread_id>", methods=["POST"])
def remove_thread(thread_id):
    require_login()
    check_csrf()
    thread = forum.get_thread(thread_id)
    if not thread or thread["user_id"] != session["user_id"]:
        abort(403)
        
    forum.remove_thread(thread_id)
    flash("Ilmoitus poistettu onnistuneesti.")
    return redirect("/")

@app.route("/search")
def search():
    if "user_id" not in session:
        flash("Kirjaudu sisään etsiäksesi pelivuoroja.")
        return redirect("/login")

    play_time = request.args.get("play_time", "")
    location = request.args.get("location", "")
    player_count = request.args.get("player_count", "")
    
    if "play_time" in request.args:
        results = forum.search_threads(play_time, location, player_count)
        searched = True
    else:
        results = []
        searched = False

    return render_template("search.html", results=results, searched=searched, 
                           play_time=play_time, location=location, player_count=player_count)

@app.route("/user/<int:user_id>")
@app.route("/user/<int:user_id>/<int:page>")
def show_user(user_id, page=1):
    user = users.get_user(user_id)
    if not user:
        abort(404)
        
    page_size = 10
    total_messages = users.message_count(user_id)
    page_count = math.ceil(total_messages / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/user/" + str(user_id) + "/1")
    if page > page_count:
        return redirect("/user/" + str(user_id) + "/" + str(page_count))
        
    messages = users.get_messages(user_id, page, page_size)
    return render_template("user.html", user=user, messages=messages, page=page, page_count=page_count, total_messages=total_messages)

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

@app.route("/join", methods=["POST"])
def join():
    require_login()
    check_csrf()
    thread_id = int(request.form["thread_id"])
    thread = forum.get_thread(thread_id)
    participants = forum.get_participants(thread_id)
    
    if len(participants) < thread["player_count"]:
        try:
            forum.add_participant(session["user_id"], thread_id)
            flash("Olet nyt mukana pelivuorolla!")
        except sqlite3.IntegrityError:
            flash("Olet jo mukana.")
    else:
        flash("Vuoro on jo täynnä.")
    return redirect("/thread/" + str(thread_id))

@app.route("/leave", methods=["POST"])
def leave():
    require_login()
    check_csrf()
    thread_id = int(request.form["thread_id"])
    forum.remove_participant(session["user_id"], thread_id)
    flash("Ilmoittautuminen peruttu.")
    return redirect("/thread/" + str(thread_id))

@app.route("/edit_thread/<int:thread_id>", methods=["GET", "POST"])
def edit_thread(thread_id):
    require_login()
    thread = forum.get_thread(thread_id)
    
    if not thread:
        abort(404)
        
    if thread["user_id"] != session["user_id"]:
        abort(403)
        
    messages = forum.get_messages(thread_id)
    first_message = messages[0] if messages else None

    if request.method == "GET":
        nyt = datetime.now()
        seuraava_tunti = (nyt + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        min_time = seuraava_tunti.strftime("%Y-%m-%dT%H:%M")
        
        try:
            dt = datetime.strptime(thread["play_time"], "%d.%m.%Y klo %H:%M")
            current_play_time = dt.strftime("%Y-%m-%dT%H:%M")
        except ValueError:
            current_play_time = ""

        return render_template("edit_thread.html", thread=thread, current_play_time=current_play_time, min_time=min_time, content=first_message["content"] if first_message else "")

    if request.method == "POST":
        check_csrf() 
        
        play_time_raw = request.form["play_time"]
        location = request.form["location"]
        skill_level = request.form["skill_level"]
        player_count = request.form["player_count"]
        duration = request.form["duration"]
        content = request.form["content"]
        
        try:
            dt = datetime.strptime(play_time_raw, "%Y-%m-%dT%H:%M")
            if dt < datetime.now():
                flash("Peliajan on oltava tulevaisuudessa.")
                return redirect("/edit_thread/" + str(thread_id))
                
            dt = dt.replace(minute=0)
            play_time = dt.strftime("%d.%m.%Y klo %H:%M")
        except ValueError:
            abort(403)
        
        allowed_locations = ["Kimpisen massatenniskentät", "Huhtiniemen sisähalli"]
        allowed_levels = ["Aloittelija", "Keskitaso", "Kilpa"]
        
        try:
            p_count = int(player_count)
            duration_h = int(duration)
        except ValueError:
            abort(403)
            
        if location not in allowed_locations or skill_level not in allowed_levels or p_count < 1 or p_count > 4 or duration_h < 1 or duration_h > 10:
            abort(403)
            
        if not play_time or len(content) > 5000:
            abort(403)
            
        forum.update_thread(thread_id, play_time, location, skill_level, p_count, duration_h)
        if first_message:
            forum.update_message(first_message["id"], content)
        
        flash("Ilmoitusta muokattu onnistuneesti!")
        return redirect("/thread/" + str(thread_id))


@app.errorhandler(403)
def forbidden(e):
    flash("Pääsy evätty. Kirjaudu sisään käyttääksesi tätä toimintoa.")
    return redirect("/login")

@app.errorhandler(404)
def not_found(e):
    flash("Etsimääsi sivua tai ilmoitusta ei löytynyt.")
    return redirect("/")