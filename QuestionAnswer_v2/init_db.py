import sqlite3

connection = sqlite3.connect('questionanswer.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tag (tag_name) VALUES ('Advance')")

cur.execute("INSERT INTO question (question_content, question_vote, question_tag, is_open) \
             VALUES (?, ?, ?, ?)",
            ('5 + 5 =', 0, 2, 1)
            )

cur.execute("INSERT INTO answer (answer_question, answer_content, answer_vote) \
            VALUES (?, ?, ?)",
            (2, '10', 1)
            )

cur.execute("INSERT INTO answer (answer_question, answer_content, answer_vote) \
            VALUES (?, ?, ?)",
            (2, '15', -1)
            )

connection.commit()
connection.close()