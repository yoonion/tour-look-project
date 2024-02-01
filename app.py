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
    comment_user_nickname = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'게시글 고유번호={self.post_pk}, 작성자 닉네임={self.comment_user_nickname} '

with app.app_context():
    db.create_all()

# 메인 (리스트 지역별 검색 가능)
@app.route("/")
def main():
    
    try: # 파라미터가 있는경우
        param = request.args["post_local_cate"] 
        if(param == '전체'):
            param = ""
    except KeyError: # 쿼리 파라미터 없는경우 예외처리
        param = ""

    if len(param) > 0:
        post_list = Post.query.filter_by(post_local_cate=param).all()
    else:
        post_list = Post.query.all()
    
    return render_template('index.html', post_list = post_list)

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
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_pwd']

        user = User.query.filter_by(user_id=user_id, user_password=user_password).first()
        if user is not None: # 쿼리 데이터가 존재하면
            session['user_pk'] = user.user_pk # user pk를 session에 저장한다.
            session['user_id'] = user_id # user id를 session에 저장한다.
            return redirect('/')
        else:
            return '회원 정보가 일치하지 않습니다.' # 쿼리 데이터가 없으면 출력
        
    else:
        return render_template('login.html')
    
# 로그아웃
@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

# 게시글 등록 페이지
@app.route("/post", methods=['GET', 'POST'])
def post_save():
    if request.method == 'POST':
        # userPk = request.form['user_pk']
        userPk = session['user_pk']
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

        return redirect(url_for('post_detail', post_pk = post.post_pk))
    else:
        return render_template('post_save.html')

# 게시글 상세 페이지
@app.route("/post/<post_pk>")
def post_detail(post_pk):
    post = Post.query.filter_by(post_pk = post_pk).first()
    
    if not post:
        response = {
            "status": 404,
            "msg":'해당 게시글을 찾을 수 없습니다.'
        }
        return jsonify(response), 404
    else:
        title = post.post_title
        content = post.post_content
        category = post.post_local_cate
        
        response = {
            "post_title": title,
            "post_content": content,
            "post_local_cate": category,
            "comments": [
                {
                    "user_nickname": "사용자 닉네임",
                    "comment_content": "사용자가 작성한 댓글 내용입니다."
                }
            ]
        }
        return render_template('post_detail.html', data = response)

if __name__ == "__main__":
    app.run(port=8000, debug=True)