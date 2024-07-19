import random
import string

from flask import Blueprint, render_template, jsonify, redirect, url_for, session

from exts import mail, db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect('/')
            else:
                print('密码错误')
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get('email')
    source = string.digits
    captcha = random.sample(source, 4)
    print(captcha)
    captcha = "".join(captcha)
    message = Message(subject="注册验证码", recipients=[email], body=f"您的验证码是{captcha}")
    mail.send(message)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({
        'code': 200,
        'message': 'Successfully',
        'data': None
    })


@bp.route('/mail/test')
def mail_test():
    message = Message(subject="邮箱测试", recipients=["3115729294@qq.com"], body="这是一封测试邮件")
    mail.send(message)
    return "邮件发送成功"
