import sqlite3
import json

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('questionanswer.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_question(question_id):
    conn = get_db_connection()
    question = conn.execute('   SELECT q.question_id, q.question_content, q.question_vote, t.tag_name, a.answer_content, a.answer_vote \
                                FROM question AS q \
                                LEFT JOIN answer AS a on a.answer_question = q.question_id \
                                LEFT JOIN tag AS t ON t.tag_id = q.question_tag \
                                WHERE q.question_id = ?',(question_id,)
                            ).fetchone()
    conn.close()
    if question is None:
        abort(404)
    return question

def get_answerquestion(question_id):
    conn = get_db_connection()
    answer = conn.execute(' SELECT a.answer_id, a.answer_content, a.answer_vote, q.question_content, q.question_vote \
                            FROM answer AS a \
                            LEFT JOIN question AS q on q.question_id = a.answer_question \
                            WHERE a.answer_question = ?',(question_id,)
                         ).fetchall()
    conn.close()
    if answer is None:
        abort(404)
    return answer

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    questions = conn.execute('  SELECT q.question_id, q.question_content, a.answer_content, a.answer_vote \
                                FROM question AS q \
                                LEFT JOIN answer AS a on a.answer_question = q.question_id \
                                GROUP BY a.answer_question \
                                HAVING a.answer_vote =  max(a.answer_vote)').fetchall()
    conn.close()
    return render_template('index.html', questions=questions)


@app.route('/<int:question_id>')
def question(question_id):
    question = get_question(question_id)
    answers = get_answerquestion(question_id)
    return render_template('question.html', question=question, answers=answers)

@app.route('/tagadd/', methods=('GET', 'POST'))
def tagadd():
    return render_template('tagadd.html')

@app.route('/questionadd/', methods=('GET', 'POST'))
def questionadd():
    return render_template('questionadd.html')

if __name__ == '__main__':
    app.run(debug=True)

    