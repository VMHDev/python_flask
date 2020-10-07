import sqlite3
import json

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('questionanswer.db')
    conn.row_factory = sqlite3.Row
    return conn

#region Function Question
def get_questionall():
    conn = get_db_connection()
    questions = conn.execute('  SELECT q.question_id, q.question_content, IFNULL(a.answer_content, \'No answer\') AS answer_content, IFNULL(a.answer_vote, 0) AS answer_vote \
                                FROM question AS q \
                                LEFT JOIN answer AS a on a.answer_question = q.question_id \
                                GROUP BY q.question_id \
                                HAVING a.answer_vote =  max(a.answer_vote) OR a.answer_vote IS NULL \
                                ORDER BY q.question_content').fetchall()
    conn.close()
    if questions is None:
        abort(404)
    return questions

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
#endregion

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

#region Function Tag
def get_tagall():
    conn = get_db_connection()
    tags = conn.execute(' SELECT tag_id, tag_name FROM tag ').fetchall()
    conn.close()
    if tags is None:
        abort(404)
    return tags

def get_tag(tag_id):
    conn = get_db_connection()
    tag = conn.execute('SELECT tag_id, tag_name FROM tag \
                        WHERE tag_id = ?',(tag_id,)
                       ).fetchone()
    conn.close()
    if tag is None:
        abort(404)
    return tag
#endregion

#=========================================================================================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'QuestionAnswerFlask'

@app.route('/')
def index():
    return redirect(url_for('question'))

#region Route Question
@app.route('/question/')
def question():
    questions = get_questionall()
    return render_template('index.html', questions=questions)

@app.route('/<int:question_id>/')
def questiondetail(question_id):
    question = get_question(question_id)
    answers = get_answerquestion(question_id)
    return render_template('question.html', question=question, answers=answers)

@app.route('/questionadd/', methods=('GET', 'POST'))
def questionadd():
    if request.method == 'POST':
        tag_id = request.form.get('tag_select')
        content = request.form['contentquestion']

        if not content:
            flash('Content question is required!')
        else:
            conn = get_db_connection()
            conn.execute('  INSERT INTO question (question_content, question_vote, question_tag, is_open) \
                            VALUES (?, ?, ?, ?)'
                            ,(content, 0, tag_id, 1))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    tags = get_tagall()
    return render_template('questionadd.html', tags=tags)
#endregion

#region Route Tag
@app.route('/tag/')
def tag():
    tags = get_tagall()
    return render_template('tag.html', tags=tags)

@app.route('/tagadd/', methods=('GET', 'POST'))
def tagadd():
    if request.method == 'POST':
        tag_name = request.form['tagname']

        if not tag_name:
            flash('Name tag is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO tag (tag_name) VALUES (?)',(tag_name,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('tagadd.html')

@app.route('/tag/<int:tagid>', methods=('GET', 'POST'))
def tagedit(tagid):
    tag = get_tag(tagid)

    if request.method == 'POST':
        tagname = request.form['tagname']

        if not tagname:
            flash('Tag Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE tag SET tag_name = ?'
                         'WHERE tag_id = ?',
                         (tagname, tagid))
            conn.commit()
            conn.close()
            return redirect(url_for('tag'))

    return render_template('tagedit.html', tag=tag)

@app.route('/tag/<int:tagid>/delete', methods=('POST',))
def tagdelete(tagid):
    tag = get_tag(tagid)
    conn = get_db_connection()
    conn.execute('DELETE FROM tag WHERE tag_id = ?', (tagid,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(tag['tag_name']))
    return redirect(url_for('tag'))
#endregion

if __name__ == '__main__':
    app.run(debug=True)

    