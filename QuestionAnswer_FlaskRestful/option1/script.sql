CREATE TABLE question (
    question_id       INTEGER NOT NULL,
    question_content  STRING,
    question_vote     INTEGER DEFAULT (0),
    question_tag      INTEGER,
    is_open           BOOLEAN,
    PRIMARY KEY (
        question_id
    )
);

CREATE TABLE tag (
    tag_id    INTEGER NOT NULL,
    tag_name  STRING,
    PRIMARY KEY (
        tag_id
    )
);

CREATE TABLE answer (
    answer_id        INTEGER NOT NULL,
    answer_question  INTEGER,
    answer_content   STRING,
    answer_vote      INTEGER DEFAULT (0),
    PRIMARY KEY (
        answer_id
    )
);

INSERT INTO tag (tag_name)  VALUES  ('Basic');
INSERT INTO question (question_content, question_vote, question_tag, is_open)  VALUES  ('1 + 1 =', 0, 1, 1);
INSERT INTO answer (answer_question, answer_content, answer_vote)  VALUES  (1, '2', 0);