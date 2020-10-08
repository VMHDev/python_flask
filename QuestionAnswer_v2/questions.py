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

###########################################################################################################################
def get_questionall():
    conn = get_db_connection()
    questions = conn.execute('  SELECT q.question_id, q.question_content,  tag_name, IFNULL(a.answer_content, \'No answer\') AS answer_content, IFNULL(a.answer_vote, 0) AS answer_vote \
                                FROM question AS q \
                                LEFT JOIN answer AS a on a.answer_question = q.question_id \
                                LEFT JOIN tag AS t ON t.tag_id = q.question_tag \
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