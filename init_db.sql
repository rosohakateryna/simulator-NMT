DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS choices;
DROP TABLE IF EXISTS match_pairs;

CREATE TABLE questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,           -- math/ukr/history/...
  year INTEGER,
  topic TEXT,
  type TEXT NOT NULL,              -- 'SC' | 'OA' | 'MA'
  text TEXT NOT NULL,
  correct_index INTEGER,           -- для SC (1..N)
  correct_text TEXT,               -- для OA (варіанти через ; )
  explanation TEXT,                -- пояснення (опціонально)
  source TEXT
);

-- варіанти для SC
CREATE TABLE choices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL,
  idx INTEGER NOT NULL,            -- 1..N
  text TEXT NOT NULL,
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);

-- пари для MA (знадобиться на наступному етапі)
CREATE TABLE match_pairs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL,
  left_text TEXT NOT NULL,
  right_text TEXT NOT NULL,
  pair_key TEXT NOT NULL,
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
