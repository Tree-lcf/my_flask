from flask import Flask, request, make_response, render_template, redirect, url_for, session
import config
from models import db, User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "填写错误"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        pw1 = request.form.get('password1')
        pw2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return "该手机号已注册"
        else:
            if pw1 != pw2:
                return "密码两次设定不等"
            else:
                user = User(telephone=telephone, username=username, password=pw1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()
