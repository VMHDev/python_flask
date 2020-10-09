DROP TABLE IF EXISTS question;
CREATE TABLE question (
    question_id       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    question_content  STRING,
    question_vote     INTEGER DEFAULT (0),
    question_tag      INTEGER,
    is_open           BOOLEAN
);

DROP TABLE IF EXISTS tag;
CREATE TABLE tag (
    tag_id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tag_name  STRING
);

DROP TABLE IF EXISTS answer;
CREATE TABLE answer (
    answer_id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    answer_question  INTEGER,
    answer_content   STRING,
    answer_vote      INTEGER DEFAULT (0)
);

INSERT INTO tag (tag_name)  VALUES  ('Basic');
INSERT INTO tag (tag_name)  VALUES  ('Python');
INSERT INTO tag (tag_name)  VALUES  ('Java');
INSERT INTO tag (tag_name)  VALUES  ('C/C++');

INSERT INTO question (question_content, question_vote, question_tag, is_open)  VALUES  ('1 + 1 =', 0, 1, 1);
INSERT INTO answer (answer_question, answer_content, answer_vote)  VALUES  (1, '2', 0);

INSERT INTO question (question_content, question_vote, question_tag, is_open)  VALUES  ('2 + 2 =', -1, 1, 1);
INSERT INTO answer (answer_question, answer_content, answer_vote)  VALUES  (1, '4', 1);
INSERT INTO answer (answer_question, answer_content, answer_vote)  VALUES  (1, '5', -1);

INSERT INTO question (question_content, question_vote, question_tag, is_open)  VALUES  ('3 + 3 =', 2, 1, 1);
INSERT INTO answer (answer_question, answer_content, answer_vote)  VALUES  (1, '6', 3);