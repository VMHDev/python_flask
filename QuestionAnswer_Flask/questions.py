from databases import get_db_connection
from werkzeug.exceptions import abort

class Questions:
    def __init__(self, question_content ='', question_vote=0, question_tagid=None, is_open=1):
        self.question_content = question_content
        self.question_vote = question_vote
        self.question_tagid = question_tagid
        self.is_open = is_open

    def ins_questions(self):
        conn = get_db_connection()
        conn.execute('  INSERT INTO question (question_content, question_vote, question_tag, is_open) \
                        VALUES (?, ?, ?, ?)'
                        ,(self.question_content, 0, self.question_tagid, 1))
        conn.commit()
        conn.close()

    def upd_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('UPDATE question SET question_content = ?'
                     'WHERE question_id = ?',
                     (self.question_content, questionid))
        conn.commit()
        conn.close()

    def del_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('DELETE FROM question WHERE question_id = ?', (questionid,))
        conn.commit()
        conn.close() 

    def addtag_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('UPDATE question SET question_tag = ?'
                     'WHERE question_id = ?',
                     (self.question_tagid, questionid))
        conn.commit()
        conn.close()     

    def close_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('UPDATE question SET is_open = ?'
                     'WHERE question_id = ?',
                     (0, questionid))
        conn.commit()
        conn.close()

    def open_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('UPDATE question SET is_open = ?'
                     'WHERE question_id = ?',
                     (1, questionid))
        conn.commit()
        conn.close()

    def upvote_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('UPDATE question SET question_vote = question_vote + 1 '
                     'WHERE question_id = ?',
                     (questionid, ))
        conn.commit()
        conn.close()

    def downvote_questions(self, questionid):
        conn = get_db_connection()
        conn.execute('UPDATE question SET question_vote = question_vote - 1 '
                     'WHERE question_id = ?',
                     (questionid, ))
        conn.commit()
        conn.close()

###########################################################################################################################
def get_questionall():
    conn = get_db_connection()
    questions = conn.execute('  SELECT q.question_id, q.question_content, q.question_vote, q.is_open, tag_name, IFNULL(a.answer_content, \'No answer\') AS answer_content, IFNULL(a.answer_vote, 0) AS answer_vote \
                                FROM question AS q \
                                LEFT JOIN answer AS a on a.answer_question = q.question_id \
                                LEFT JOIN tag AS t ON t.tag_id = q.question_tag \
                                WHERE q.is_open = 1 \
                                GROUP BY q.question_id \
                                HAVING a.answer_vote =  max(a.answer_vote) OR a.answer_vote IS NULL \
                                ORDER BY q.question_vote DESC').fetchall()
    conn.close()
    if questions is None:
        abort(404)
    return questions

def get_question(question_id):
    conn = get_db_connection()
    
    question = conn.execute('   SELECT q.question_id, q.question_content, q.question_vote, t.tag_name, a.answer_content, a.answer_vote, q.is_open \
                                FROM question AS q \
                                LEFT JOIN answer AS a on a.answer_question = q.question_id \
                                LEFT JOIN tag AS t ON t.tag_id = q.question_tag \
                                WHERE q.question_id = ?',(question_id,)
                            ).fetchone()
    # Chú ý thứ tự trong mệnh đề Select ảnh hưởng đến hàm questiondetail
    conn.close()
    if question is None:
        abort(404)
    return question