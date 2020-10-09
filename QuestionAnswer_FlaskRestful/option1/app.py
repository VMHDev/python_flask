from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import os

basedir = os.path.abspath(os.path.dirname(__file__))
strDatabase = 'sqlite:///' + os.path.join(basedir, 'quizz.sqlite3')

db_connect = create_engine(strDatabase)
app = Flask(__name__)
api = Api(app)

class ListQuestions(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from question")
        result = {'list question': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        Question_content = request.json['question_content']
        Question_tag = request.json['question_tag']
        query = conn.execute("insert into question(question_id, question_content, question_vote, question_tag, is_open) values(null,'{0}', 0, {1}, 1)"
                            .format(Question_content, Question_tag))

        query = conn.execute("select * from question order by question_id desc limit 1")
        result = {'Insert Successs': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(ListQuestions, '/questions')

class Questions(Resource):
    def get(self, Question_id):
        conn = db_connect.connect()
        query = conn.execute("select * from question where question_id =%d "  %int(Question_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def put(self, Question_id):
        conn = db_connect.connect()
        print(request.json)
        Question_content = request.json['question_content']
        Question_vote = request.json['question_vote']
        Question_tag = request.json['question_tag']
        Is_open = request.json['is_open']
        query = conn.execute("UPDATE question SET question_content = '{0}', \
                                                  question_vote = {1}, \
                                                  question_tag = {2}, \
                                                  is_open = {3} \
                              WHERE question_id = %d"
                            .format(Question_content, Question_vote, Question_tag, Is_open) %int(Question_id))

        query = conn.execute("select * from question where question_id =%d "  %int(Question_id))
        result = {'Update Successs': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    def delete(self, Question_id):
        conn = db_connect.connect()
        print(request.json)
        query = conn.execute("DELETE FROM question WHERE question_id = %d" %int(Question_id))

        query = conn.execute("select * from question where question_id =%d "  %int(Question_id))
        result = {'Delete Successs': Question_id}
        return jsonify(result)

api.add_resource(Questions, '/questions/<Question_id>')

######################################################################################################################
class QuestionsOpen(Resource):
    # Lấy danh sách các câu hỏi đang mở
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from question where is_open = 1")
        result = {'list question': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(QuestionsOpen, '/questionsopen')

class AnswerQuestions(Resource):
    # Lấy danh sách các câu trả lời của câu hỏi
    def get(self, Question_id):
        conn = db_connect.connect()
        query = conn.execute("select * from answer where answer_question = %d "  %int(Question_id))
        result = {'list answer': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

    # Thêm câu trả lời cho câu hỏi
    def post(self, Question_id):
        conn = db_connect.connect()
        print(request.json)
        Answer_question = Question_id
        Answer_content = request.json['answer_content']
        query = conn.execute("insert into answer(answer_id, answer_question, answer_content, answer_vote) values(null, {0}, '{1}', 0)"
                            .format(Answer_question, Answer_content))

        query = conn.execute("select * from answer order by answer_id desc limit 1")
        result = {'Insert Successs': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(AnswerQuestions, '/answerquestions/<Question_id>')

class QuestionsUpDownVote(Resource):
    # Upvote/Downvote câu hỏi
    def put(self, Question_id):
        conn = db_connect.connect()
        print(request.json)

        Question_vote = request.json['question_vote']

        query = conn.execute("UPDATE question SET question_vote = question_vote + {0} WHERE question_id = %d"
                            .format(Question_vote) %int(Question_id))

        query = conn.execute("select * from question where question_id =%d "  %int(Question_id))
        result = {'Update Successs': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(QuestionsUpDownVote, '/questionsupdownvote/<Question_id>')

class AnswerUpDownVote(Resource):
    # Upvote/Downvote câu trả lời
    def put(self, Answer_id):
        conn = db_connect.connect()
        print(request.json)

        Answer_vote = request.json['answer_vote']

        query = conn.execute("UPDATE answer SET answer_vote = answer_vote + {0} WHERE answer_id = %d"
                            .format(Answer_vote) %int(Answer_id))

        query = conn.execute("select * from answer where answer_id =%d "  %int(Answer_id))
        result = {'Update Successs': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(AnswerUpDownVote, '/answerupdownvote/<Answer_id>')

if __name__ == '__main__':
    app.run()