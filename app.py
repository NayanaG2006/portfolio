from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "data.db"

def db():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS visits(n INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS msgs(name TEXT, email TEXT, message TEXT)")
    return c

@app.route("/")
def home():
    c = db()
    c.execute("INSERT INTO visits VALUES (1)")
    c.commit()
    count = c.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    return render_template("index.html", count=count, sent=request.args.get("sent"))

@app.route("/contact", methods=["POST"])
def contact():
    c = db()
    c.execute("INSERT INTO msgs VALUES (?,?,?)",
              (request.form["name"], request.form["email"], request.form["message"]))
    c.commit()
    return redirect("/?sent=1#contact")

@app.route("/messages")
def messages():
    rows = db().execute("SELECT * FROM msgs").fetchall()
    return "<br>".join(f"{n} ({e}): {m}" for n, e, m in rows) or "No messages yet"