from werkzeug.exceptions import abort

from databases import get_db_connection

class Answers:
    def __init__(self, answer_question=None, answer_content='', answer_vote=0):
        self.answer_question = answer_question
        self.answer_content = answer_content
        self.answer_vote = answer_vote

    def addanswer_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('  INSERT INTO answer (answer_question, answer_content, answer_vote) \
                        VALUES (?, ?, ?)'
                    ,(self.answer_question, self.answer_content, 0))
        conn.commit()
        conn.close() 
    
    def udp_answer(self, answerid):
        conn = get_db_connection()
        conn.execute('UPDATE answer SET answer_question = ?, answer_content = ?, answer_vote = ?'
                     'WHERE answer_id = ?',
                     (self.answer_question, self.answer_content, 0, answerid))
        conn.commit()
        conn.close() 

    def upvote_answers(self, answerid):
        conn = get_db_connection()
        conn.execute('UPDATE answer SET answer_vote = answer_vote + 1 '
                     'WHERE answer_id = ?',
                     (answerid, ))
        conn.commit()
        conn.close()

    def downvote_answers(self, answerid):
        conn = get_db_connection()
        conn.execute('UPDATE answer SET answer_vote = answer_vote - 1 '
                     'WHERE answer_id = ?',
                     (answerid, ))
        conn.commit()
        conn.close()

###########################################################################################################################
def get_answerquestion(question_id):
    conn = get_db_connection()
    answer = conn.execute(' SELECT a.answer_id, a.answer_content, a.answer_vote, q.question_content, q.question_vote \
                            FROM answer AS a \
                            LEFT JOIN question AS q on q.question_id = a.answer_question \
                            WHERE a.answer_question = ? \
                            ORDER BY a.answer_vote DESC',(question_id,)
                         ).fetchall()
    conn.close()
    if answer is None:
        abort(404)
    return answer