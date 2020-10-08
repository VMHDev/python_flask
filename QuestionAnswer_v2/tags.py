from werkzeug.exceptions import abort

from databases import get_db_connection

class Tags:
    def __init__(self, tag_name =''):
        self.tag_name = tag_name

    def ins_tags(self):
        conn = get_db_connection()
        conn.execute('INSERT INTO tag (tag_name) VALUES (?)',(self.tag_name,))
        conn.commit()
        conn.close()
    
    def upd_tags(self, tagid):
        conn = get_db_connection()
        conn.execute('UPDATE tag SET tag_name = ?'
                     'WHERE tag_id = ?',
                     (self.tag_name, tagid))
        conn.commit()
        conn.close()        

###########################################################################################################################
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