# <div align = "center">Demo Python Restful API Service<br/> Question & Answer</div>
## Xây dựng API cho phép
- Tạo câu hỏi
- Xem câu hỏi đang mở
- Thêm câu trả lời cho câu hỏi
- Danh sách câu trả lời cho câu hỏi
- Upvote/Downvote cho câu hỏi/câu trả lời

## Option 1:
- Sử dụng:
    - Flask 1.1.2
    - SQLAlchemy 1.3.18
    - Flask-RESTful 0.3.8
    - Python 3.8.3
    - Database: SQLLite 3.32.3
    - IDE: Visual Code
- Để tạo database chạy file excute.py
- File thực thi app.py
- Tham khảo: https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq

### Tạo câu hỏi
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/POST_Question.png?raw=true)

### Xem câu hỏi đang mở
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/QuestionsOpen.png?raw=true)

### Thêm câu trả lời cho câu hỏi
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/AddAnswerQuestions.png?raw=true)

### Danh sách câu trả lời cho câu hỏi
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/GetAnswerQuestions.png?raw=true)

### Upvote/Downvote cho câu hỏi
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/QuestionsUpDownVote.png?raw=true)

### Upvote/Downvote cho câu trả lời
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/AnswerUpDownVote.png?raw=true)

### Khác
#### GET
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/GET_Question.png?raw=true)

#### POST
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/POST_Question.png?raw=true)

#### PUT
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/PUT_Question.png?raw=true)

#### DELETE
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option1/DELETE_Question.png?raw=true)

## Option 2:
- Sử dụng:
    - Flask 1.1.2
    - Flask-SQLAlchemy 2.4.4
    - Python 3.8.3
    - Database: SQLLite 3.32.3
    - IDE: Visual Code
- Để tạo database chạy tập lệnh:
    - python
    - from database import db
    - db.create_all()
- File thực thi run.py
- Tham khảo: https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12

### Tạo câu hỏi
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/POST_questions.png?raw=true)

### Xem câu hỏi đang mở
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/questionsopen.png?raw=true)

### Thêm câu trả lời cho câu hỏi
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/addanswerquestions.png?raw=true)

### Upvote/Downvote cho câu hỏi
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/question_updownvote.png?raw=true)

### Upvote/Downvote cho câu trả lời
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/answer_updownvote.png?raw=true)

### Khác
#### GET
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/GET_questions.png?raw=true)

#### GET DETAILS
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/GETDetails_questions.png?raw=true)

#### POST
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/POST_questions.png?raw=true)

#### PUT
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/PUT_questions.png?raw=true)

#### DELETE
![image](https://github.com/VMHDev/python_flask/blob/master/screenshot/questionanswer/option2/DELETE_questions.png?raw=true)