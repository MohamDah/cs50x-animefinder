import os
import requests
import urllib.parse

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required


# be able to upload images

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# config for uploading


db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    #forget current user
    session.clear()
    #if through post
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", "ur smarter than this man")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", "ur smarter than this man")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", "make sure what you entered is correct")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        #ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", "ur smarter than this man")
        name = request.form.get("username")
        names = db.execute("SELECT username FROM users WHERE username = ?", name)
        if len(names) != 0:
            return apology("username already used", "sucks man change your name")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", "ur smarter than this man")

        # check confirmation if it matches
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("confirmation does not match", "ur smarter than this man")

        # insert new user
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        except:
            return apology("username is used, try a different one", "sucks man change your name")

        # keep user logged in after registeration
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/find", methods=["GET", "POST"])
def find():
    if request.method == "POST":
        if not request.form.get("img"):
            return apology("must provide image url", "cmon man")
        img = request.form.get("img")
        try:
            data = requests.get("https://api.trace.moe/search?anilistInfo&url={}".format(urllib.parse.quote_plus(img))).json()
            url = ("https://api.trace.moe/search?anilistInfo&url={}".format(urllib.parse.quote_plus(img)))
            real = {
                "result": data["result"][0]
            }
        except:
            return apology("provide valid image url", "check if the url leads to a public image")
        if session.get("user_id") is not None:
            user_id = session.get("user_id")
            name = db.execute("SELECT username FROM users WHERE id = ?", user_id)

            db.execute("INSERT INTO history (his_name, his_anime, his_url, his_date) VALUES(?, ?, ?, DATETIME())", name[0]["username"], real["result"]["anilist"]["title"]["romaji"], url)

        return render_template("found.html", data=real)

    else:
        return render_template("find.html")


@app.route("/found", methods=["POST"])
def found():
    if request.method == "POST":
        url = request.form.get("url")
        data = requests.get(url).json()
        real = {
            "result": data["result"][0]
        }
        return render_template("found.html", data=real)



@app.route("/history")
@login_required
def history():
    user_id = session.get("user_id")
    name = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    history = db.execute("SELECT * FROM history WHERE his_name = ? ORDER BY his_date DESC", name[0]["username"])
    return render_template("history.html", history=history)


@app.route("/remove", methods=["POST"])
def remove():
    his_id = request.form.get("his_id")
    db.execute("DELETE FROM history WHERE his_id = ?", his_id)
    return redirect("/history")
