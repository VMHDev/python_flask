from werkzeug.exceptions import abort

from databases import get_db_connection

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