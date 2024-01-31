from flask import Flask, render_template

app = Flask(__name__)

# 메인
@app.route("/")
def main():
    return render_template('index.html')

# 회원가입 페이지
@app.route("/signup")
def signup():
    return render_template('signup.html')

# 로그인 페이지
@app.route("/login")
def login():
    return render_template('login.html')

# 게시글 리스트 페이지
@app.route("/posts")
def post_list():
    return render_template('post_list.html')

# 게시글 등록 페이지
@app.route("/post")
def post_save():
    return render_template('post_save.html')

# 게시글 상세 페이지
@app.route("/post/<post_id>")
def post_detail(post_id):
    return render_template('post_detail.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)