# import_sc.py
import os, csv, sqlite3, pathlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "questions.db")

# 1) створюємо БД за схемою
with open(os.path.join(BASE_DIR, "init_db.sql"), "r", encoding="utf-8") as f:
    schema = f.read()
con = sqlite3.connect(DB_PATH)
con.executescript(schema)
con.commit()

# 2) імпортуємо SC-питання з CSV
csv_path = os.path.join(BASE_DIR, "questions_sc.csv")
with open(csv_path, newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    rows = list(rdr)

cur = con.cursor()
added = 0
for r in rows:
    subject = r["subject"].strip()
    year = int(r["year"]) if r["year"].strip() else None
    topic = r["topic"].strip() or None
    text = r["text"].strip()
    opts = [r["option1"].strip(), r["option2"].strip(), r["option3"].strip(), r["option4"].strip()]
    correct_index = int(r["correct_index"])
    source = (r.get("source") or "").strip() or None

    cur.execute("""INSERT INTO questions
        (subject,year,topic,type,text,correct_index,correct_text,explanation,source)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (subject,year,topic,"SC",text,correct_index,None,None,source))
    qid = cur.lastrowid
    for i, opt in enumerate(opts, start=1):
        cur.execute("INSERT INTO choices (question_id,idx,text) VALUES (?,?,?)",
                    (qid, i, opt))
    added += 1

con.commit()
con.close()
print(f"OK: додано SC-питань: {added}. Файл БД: {DB_PATH}")
