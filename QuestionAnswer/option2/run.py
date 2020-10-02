from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from database import Question, Answer

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vmh.sqlite3')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class QuestionSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('question_id', 'question_content', 'question_vote', 'question_tag', 'is_open')


question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)


class AnswerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('answer_id', 'answer_question', 'answer_content', 'answer_vote')


answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)

############################################################################################################
# endpoint to create new questions
@app.route("/questions", methods=["POST"])
def add_questions():
    question_content = request.json['question_content']
    question_vote = 0
    question_tag = request.json['question_tag']
    is_open = 1
    
    new_question = Question(question_content, question_vote, question_tag, is_open)

    db.session.add(new_question)
    db.session.commit()

    return question_schema.jsonify(new_question)

# endpoint to show all questionss
@app.route("/questions", methods=["GET"])
def get_question():
    all_questions = Question.query.all()
    result = questions_schema.dump(all_questions)
    return jsonify(result)


# endpoint to get questions detail by id
@app.route("/questions/<id>", methods=["GET"])
def question_detail(id):
    question = Question.query.get(id)
    return question_schema.jsonify(question)


# endpoint to update questions
@app.route("/questions/<id>", methods=["PUT"])
def question_update(id):
    question_udp = db.session.query(Question).filter(Question.question_id==id).first()

    question_content = request.json['question_content']
    question_vote = request.json['question_vote']
    question_tag = request.json['question_tag']
    is_open = request.json['is_open']
    print(request.json)

    question_udp.question_content = question_content
    question_udp.question_vote = question_vote
    question_udp.question_tag = question_tag
    question_udp.is_open = is_open

    db.session.commit()
    return question_schema.jsonify(question_udp)

# endpoint to delete questions
@app.route("/questions/<id>", methods=["DELETE"])
def question_delete(id):
    question_del = db.session.query(Question).filter(Question.question_id==id).first()
    db.session.delete(question_del)
    db.session.commit()

    return question_schema.jsonify(question_del)

############################################################################################################
# endpoint to show all questions open
@app.route("/questionsopen", methods=["GET"])
def get_questionopen():
    question_open = db.session.query(Question).filter(Question.is_open)
    result = questions_schema.dump(question_open)
    return jsonify(result)

# endpoint to create answer for questions
@app.route("/answer/<id_ques>", methods=["POST"])
def add_answerquestion(id_ques):
    answer_question = id_ques
    answer_content = request.json['answer_content']
    answer_vote = 0
    
    new_answerquestion = Answer(answer_question, answer_content, answer_vote)

    db.session.add(new_answerquestion)
    db.session.commit()

    return answer_schema.jsonify(new_answerquestion)

# endpoint to upvote/downvote questions
@app.route("/question_updownvote/<id>", methods=["PUT"])
def question_updownvote(id):
    question_udp = db.session.query(Question).filter(Question.question_id==id).first()

    question_vote = question_udp.question_vote
    question_vote = question_vote + int(request.json['question_vote'])
    print(request.json)

    question_udp.question_vote = question_vote

    db.session.commit()
    return question_schema.jsonify(question_udp)

# endpoint to upvote/downvote answers
@app.route("/answer_updownvote/<id>", methods=["PUT"])
def answer_updownvote(id):
    answer_udp = db.session.query(Answer).filter(Answer.answer_id==id).first()

    answer_vote = answer_udp.answer_vote
    answer_vote = answer_vote + int(request.json['answer_vote'])

    answer_udp.answer_vote = answer_vote

    db.session.commit()
    return answer_schema.jsonify(answer_udp)

if __name__ == '__main__':
    app.run(debug=True)