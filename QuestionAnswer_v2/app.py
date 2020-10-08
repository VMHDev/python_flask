import sqlite3
import json

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from databases import get_db_connection
from questions import *
from tags import *
from answers import *

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

@app.route('/question/<int:questionid>/')
def questiondetail(questionid):
    question = get_question(questionid)
    answers = get_answerquestion(questionid)
    return render_template('question.html', question=question, answers=answers)

@app.route('/question/<int:questionid>/edit/')
def questionedit(questionid):
    question = get_question(questionid)
    return render_template('questioneidt.html', question=question)

@app.route('/question/<int:questionid>/addanswer/', methods=('GET', 'POST'))
def questionaddanswer(questionid):
    question = get_question(questionid)
    return render_template('questionaddanswer.html', question=question)

@app.route('/questionadd/', methods=('GET', 'POST'))
def questionadd():
    if request.method == 'POST':
        tag_id = request.form.get('tag_select')
        content = request.form['contentquestion']

        if not content:
            flash('Content question is required!')
        else:
            obj_questions = Questions(question_content=content, question_tagid=tag_id)
            obj_questions.ins_questions()
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
        tagname = request.form['tagname']

        if not tagname:
            flash('Name tag is required!')
        else:
            obj_tags = Tags(tag_name=tagname)
            obj_tags.ins_tags()
            return redirect(url_for('tag'))

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

#region Route Answer

#endregion

if __name__ == '__main__':
    app.run(debug=True)

    