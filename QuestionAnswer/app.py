import sqlite3

from flask import Flask, render_template

def get_db_connection():
    conn = sqlite3.connect('questionanswer.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    questions = conn.execute('  SELECT question_content, answer_content, answer_vote \
                                FROM question AS q \
                                LEFT JOIN answer AS a on a.answer_question = q.question_id \
                                GROUP BY a.answer_question \
                                HAVING a.answer_vote =  max(a.answer_vote)').fetchall()
    conn.close()
    return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)

    