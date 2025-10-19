# app.py
import os, sqlite3, random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "nmt-secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "questions.db")

SUBJECTS = {"math":"Математика","ukr":"Українська мова","history":"Історія України"}

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def get_random_sc(subject=None):
    con = db(); cur = con.cursor()
    if subject in SUBJECTS:
        cur.execute("SELECT * FROM questions WHERE type='SC' AND subject=? ORDER BY RANDOM() LIMIT 1", (subject,))
    else:
        cur.execute("SELECT * FROM questions WHERE type='SC' ORDER BY RANDOM() LIMIT 1")
    q = cur.fetchone()
    if not q: 
        con.close(); return None
    cur.execute("SELECT idx, text FROM choices WHERE question_id=? ORDER BY idx", (q["id"],))
    opts = cur.fetchall()
    con.close()
    return dict(q) | {"options": opts}

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST" and "subject" in request.form:
        subj = request.form["subject"]
        session["subject"] = subj
        session["score"] = 0
        session["total"] = 0
        return redirect(url_for("quiz"))
    return render_template("index.html", subjects=SUBJECTS, stats=None)

@app.route("/quiz", methods=["GET","POST"])
def quiz():
    subject = session.get("subject")
    feedback = None

    # перевірка попередньої відповіді
    if request.method == "POST" and "answer" in request.form and session.get("q"):
        chosen = int(request.form["answer"])
        correct = session["q"]["correct_index"]
        session["total"] += 1
        if chosen == correct:
            session["score"] += 1
            feedback = ("✅ Правильно!", True)
        else:
            feedback = (f"❌ Неправильно. Правильна: {correct}", False)

    # нове випадкове SC-питання
    q = get_random_sc(subject)
    session["q"] = q

    stats = {
        "subject_name": SUBJECTS.get(subject, "Усі"),
        "score": session.get("score",0),
        "total": session.get("total",0)
    }
    return render_template("quiz.html", q=q, feedback=feedback, stats=stats)

if __name__ == "__main__":
    app.run(debug=True)
