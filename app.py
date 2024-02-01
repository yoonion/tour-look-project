from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.secret_key = 'secret-key'

db = SQLAlchemy(app)

# Table
class User(db.Model):
    user_pk = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_nickname = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'username={self.user_id}, pwd={self.user_password}'

class Post(db.Model):
    post_pk = db.Column(db.Integer, primary_key=True)
    user_pk = db.Column(db.Integer, nullable=False)
    post_title = db.Column(db.String(255), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    post_local_cate = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'제목={self.post_title}, 작성자 고유번호={self.user_pk}'

class Comment(db.Model):
    comment_pk = db.Column(db.Integer, primary_key=True)
    post_pk = db.Column(db.Integer, nullable=False)
    comment_user_pk = db.Column(db.Integer, nullable=False)
    comment_content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'게시글 고유번호={self.post_pk}, 작성자 고유번호={self.user_pk}'

with app.app_context():
    db.create_all()

# 메인
@app.route("/")
def main():
    return render_template('index.html')

# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userid = request.form['user_id']
        password = request.form['user_password']
        nickname = request.form['user_nickname']

        user = User(user_id = userid, user_password = password, user_nickname = nickname)
        db.session.add(user)
        db.session.commit()

        response = {
            "msg": "회원가입 성공!",
        }

        return jsonify(response), 200
    else:
        return render_template('signup.html')

# 로그인 페이지
@app.route("/login")
def login():
    return render_template('login.html')

# 게시글 등록 페이지
@app.route("/post", methods=['GET', 'POST'])
def post_save():
    if request.method == 'POST':
        userPk = request.form['user_pk']
        title = request.form['post_title']
        content = request.form['post_content']
        category = request.form['post_local_cate']

        post = Post(user_pk = userPk, post_title = title, post_content = content, post_local_cate = category)
        db.session.add(post)
        db.session.commit()

        context = {
            "post_title": title,
            "post_content": content,
            "post_local_cate": category,
            "comments": []
        }

        return render_template('post_detail.html', response = context)
    else:
        return render_template('post_save.html')

# 게시글 상세 페이지
@app.route("/post/<post_id>")
def post_detail(post_id):
    return render_template('post_detail.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)