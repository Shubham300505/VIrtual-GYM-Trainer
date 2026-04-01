from ai import chat_with_ai
from flask import Flask, render_template, request, redirect, session
from logic import generate_plan
import sqlite3

app = Flask(__name__)
app.secret_key = "gymsecret"

# ---------- DATABASE SETUP ----------
def get_db():
    conn = sqlite3.connect("gym.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()

    # USERS TABLE
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        userid TEXT PRIMARY KEY,
        name TEXT,
        password TEXT
    )
    """)

    # 🔥 PROGRESS TABLE (NEW)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS progress(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT,
        weight REAL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

create_table()

# ---------- CHECK USER ----------
def user_exists(userid):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE userid=?",
        (userid,)
    ).fetchone()
    conn.close()
    return user is not None

# ---------- LOGIN CHECK ----------
def check_login(userid, password):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE userid=? AND password=?",
        (userid, password)
    ).fetchone()
    conn.close()
    return user is not None

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("home.html")

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        userid = request.form["userid"]
        password = request.form["password"]

        if check_login(userid, password):
            session["user"] = userid
            return redirect("/planner")
        else:
            return "Invalid ID or Password"

    return render_template("login.html")

# SIGNUP
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        userid = request.form["userid"]
        name = request.form["name"]
        password = request.form["password"]

        if user_exists(userid):
            return "User ID already exists"

        conn = get_db()
        conn.execute(
            "INSERT INTO users(userid,name,password) VALUES(?,?,?)",
            (userid, name, password)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")

# WORKOUT PLANNER PAGE
@app.route("/planner")
def planner():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")

# RESULT PAGE
@app.route("/result", methods=["POST"])
def result():
    if "user" not in session:
        return redirect("/")

    data = request.form
    plan = generate_plan(data)
    return render_template("result.html", plan=plan)

# 🔥 SAVE PROGRESS (NEW FEATURE)
@app.route("/save_progress", methods=["POST"])
def save_progress():
    if "user" not in session:
        return redirect("/")

    weight = request.form["weight"]
    userid = session["user"]

    conn = get_db()
    conn.execute(
        "INSERT INTO progress(userid, weight) VALUES(?,?)",
        (userid, weight)
    )
    conn.commit()
    conn.close()

    return redirect("/planner")

# 🔥 LOGOUT (NEW FEATURE)
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_msg = request.form["message"]
        reply = chat_with_ai(user_msg)

        session["chat_history"].append({
            "user": user_msg,
            "bot": reply
        })

    return render_template("chat.html", chat=session["chat_history"])

# ---------- RUN APP ----------
if __name__ == "__main__":
    app.run(debug=True)