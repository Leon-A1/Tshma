from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from flask_mail import Mail, Message

from .forms import RegisterForm, LoginForm, ResetPasswordForm, RequestResetForm
from .models import User, Post

from app import app, db, bootstrap, login_manager, mail, bcrypt




####### VIEWS #######


@app.route('/', methods=['GET', 'POST'])
def index():
    
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # active_users = User.query.all()
        # for active in active_users:
        #
        #     if new_user.username == active.username or :
        #         return
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(username=form.username.data).first()
        if user:


            u = User.query.get(user.id)

            p = Post(content="Hey everyone just signed up", author=u)
            p.timestamp = datetime.utcnow()

            db.session.add(p)
            db.session.commit()

            return render_template('login.html', message="account has been created")




        # msg = Message('Registration completed', sender="support@eazycrypto.live",
        #               recipients=[form.email.data])
        # msg.html = render_template('mail/registration.html', user=form.username.data, password=form.password.data)
        # mail.send(msg)



        #User has been created succsessfuly###
        return render_template('index', form=form , message="something went wrong please try again")


    return render_template('index.html', form=form)


#### login view #####

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))

        return render_template('login.html', form=form, message='wrong login credentials, please try again')

    return render_template('login.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        req = request.form
        content = req['content']
        # msg = Message('subject', sender="",
        #               recipients=[current_user.email])
        # msg.html = render_template('mail template', user=current_user.username)
        # mail.send(msg)
        
        u = User.query.get(current_user.username)
        u.last_login = datetime.utcnow()
        p = Post(content=content, author=u)
        p.timestamp = datetime.utcnow()
        db.session.add(p, u)
        db.session.commit()

        return render_template("simple/postsubmitted.html")

    username = current_user.username
    last_login = current_user.last_login
    
    num_of_posts = []
    
    Posts = Post.query.order_by(Post.timestamp.desc()).filter_by(user_id=current_user.id).all()
    for p in Posts:
        num_of_posts.append(p)
    
    num_of_posts = len(num_of_posts)
    last_login = last_login.strftime('%H:%M %d-%H-%y')


    return render_template("profile.html", num_of_posts=num_of_posts, Posts=Posts, username=username,last_login=last_login )




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/contact")
def contact():


    return render_template("simple/contact.html")



##################### forgot password ##############


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='',
                  recipients=[user.email])
    msg.html = render_template('mail/resetpassword.html', token=token)

    mail.send(msg)



@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        return redirect(url_for('login'))
    return render_template('simple/reset_request.html', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('simple/reset_token.html', form=form)
