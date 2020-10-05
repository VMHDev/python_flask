from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vmh.sqlite3')
db = SQLAlchemy(app)


class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_content = db.Column(db.Text)
    question_vote = db.Column(db.Integer)
    question_tag = db.Column(db.Integer)
    is_open = db.Column(db.Boolean)

    def __init__(self, question_content, question_vote, question_tag, is_open):
        self.question_content = question_content
        self.question_vote = question_vote
        self.question_tag = question_tag
        self.is_open = is_open

class Answer(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    answer_question = db.Column(db.Integer)
    answer_content = db.Column(db.Text)
    answer_vote = db.Column(db.Integer)


    def __init__(self, answer_question, answer_content, answer_vote):
        self.answer_question = answer_question
        self.answer_content = answer_content
        self.answer_vote = answer_vote

class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text)


    def __init__(self, tag_name):
        self.tag_name = tag_name