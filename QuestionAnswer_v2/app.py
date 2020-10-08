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

@app.route('/question/<int:questionid>/edit/', methods=('GET', 'POST'))
def questionedit(questionid):
    question = get_question(questionid)
    
    if request.method == 'POST':
        questioncontent = request.form['questioncontent']

        if not questioncontent:
            flash('Question content is not required!')
        else:
            obj_questions = Questions(question_content=questioncontent)
            obj_questions.upd_questions(questionid)

            answers = get_answerquestion(questionid)
            return redirect(url_for('question', question=question, answers=answers))
    
    return render_template('questioneidt.html', question=question)

@app.route('/question/<int:questionid>/addanswer/', methods=('GET', 'POST'))
def questionaddanswer(questionid):
    question = get_question(questionid)

    if request.method == 'POST':
        contentanswer = request.form['contentanswer']

        if not contentanswer:
            flash('Answer is not required!')
        else:
            obj_answer = Answers(answer_question=questionid, answer_content=contentanswer)
            obj_answer.addanswer_questions(questionid)

            return redirect(url_for('questiondetail', questionid=questionid))

    return render_template('questionaddanswer.html', question=question)

@app.route('/question/<int:questionid>/addtag/', methods=('GET', 'POST'))
def questionaddtag(questionid):
    question = get_question(questionid)
    tags = get_tagall()

    if request.method == 'POST':
        tagid = request.form['tag_select']

        if not tagid:
            flash('Tag is not required!')
        else:
            obj_questions = Questions(question_tagid=tagid)
            obj_questions.addtag_questions(questionid)

            return redirect(url_for('question'))

    return render_template('questionaddtag.html', question=question, tags=tags)

@app.route('/questionadd/', methods=('GET', 'POST'))
def questionadd():
    if request.method == 'POST':
        tag_id = request.form.get('tag_select')
        content = request.form['contentquestion']

        if not content:
            flash('Content question is not required!')
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
            flash('Name tag is not required!')
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
            flash('Tag Name is not required!')
        else:
            obj_tags = Tags(tag_name=tagname)
            obj_tags.upd_tags(tagid)
            return redirect(url_for('tag'))

    return render_template('tagedit.html', tag=tag)

@app.route('/tag/<int:tagid>/delete', methods=('POST',))
def tagdelete(tagid):
    tag = get_tag(tagid)

    obj_tags = Tags()
    obj_tags.del_tags(tagid)

    flash('"{}" was successfully deleted!'.format(tag['tag_name']))
    return redirect(url_for('tag'))
#endregion

#region Route Answer

#endregion

if __name__ == '__main__':
    app.run(debug=True)

    