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
from . import profits, mail_temps


from .forms import RegisterForm, LoginForm, ResetPasswordForm, RequestResetForm
from .models import User, Trade, Transaction

from app import app, db, bootstrap, login_manager, mail, bcrypt




##################################default profit system vars########################################
profit_now = True
profits_amount_total = 0
loses_amount_total = 0
total = []
timenow = datetime.utcnow()


#get the price of BTC from bitinfocharts#
URL = 'https://bitinfocharts.com/cryptocurrency-prices/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id="tr_1")
listofvar = []
for i in results:
    listofvar.append(i)
betterinfo = []
for l in listofvar[5]:
    betterinfo.append(l)
BTCprice = []
for e in betterinfo[0]:
    BTCprice.append(e)

BTCprice = BTCprice[0]
# print(len(BTCprice))
if len(BTCprice) > 10:
    btc_price_clean = BTCprice[2:4]+BTCprice[5:11]

btc_price_clean = BTCprice[2:3]+BTCprice[4:11]
# btc_price_clean = 9000
#
# # print(BTCprice)
#
# print(btc_price_clean)



############################################################################################################################################################################
# file_path = os.path.abspath(os.getcwd())+"\database.db"

best_time = timenow.strftime('%M:%H %d-%m-%Y')

###### PROFIT FUNC ######


def balance_updater(balance, profits_amount_total, loses_amount_total):

    balance = float(balance) +(profits_amount_total)-(loses_amount_total)
    return  balance



def profits_updater(total):

    profits_amount_total = 0

    for p in total:
        if p.outcome == 'WIN ':
            profits_amount_total = profits_amount_total + p.amount

    return profits_amount_total


def lose_updater(total):

    loses_amount_total = 0
    for p in total:
        if p.outcome == 'LOSE':
            loses_amount_total = loses_amount_total + p.amount

    return loses_amount_total





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

            p = Transaction(action='Deposit', author=u)
            p.amount = '5000'
            p.method = 'Points'
            p.status = 'Confirmed'
            p.timestamp = datetime.utcnow()

            db.session.add(p)
            db.session.commit()




        # msg = Message('Registration completed', sender="support@eazycrypto.live",
        #               recipients=[form.email.data])
        # msg.html = render_template('mail/registration.html', user=form.username.data, password=form.password.data)
        # mail.send(msg)



        #User has been created succsessfuly###
        return redirect(url_for('login'))


    return render_template('index.html', form=form)


#### login view #####

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))

        return render_template('login.html', form=form, message='wrong login credentials, please try again')
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)




@app.route('/dashboard')
@login_required
def dashboard():


    # lasttradingday = (current_user.last_login.day)
    # lasttradingday = str(lasttradingday)
    # print(lasttradingday)

    # previous_trades = Trade.query.order_by(Trade.timestamp.desc()).paginate(page=page, per_page=40)

    my_name = current_user.username
    my_email = current_user.email
    balance = current_user.balance
    real = current_user.real
    last_login = datetime.utcnow()
    last_login_day = last_login.day

    page = request.args.get('transactionpage', 1, type=int)
    transactionhistory = []
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).filter_by(user_id=current_user.id)paginate(page=page, per_page=5)


    for t in transactions.items:
        # print(trade.user_id)
        if t.user_id == current_user.id:

            # print(trade)
            transactionhistory.append(t)

    page = request.args.get('page', 1, type=int)



    tradinghistory = []
    old_trades = Trade.query.order_by(Trade.timestamp.desc()).paginate(page=page, per_page=20)

    for trade in old_trades.items:
        # print(trade.user_id)
        if trade.user_id == current_user.id:
            # print(trade)
            tradinghistory.append(trade)



    if current_user.daily_limit < 5:

        trades = []


        total = trademkr(current_user.id)
        too_many = 0
        for t in total:
            if too_many <= 10:
                trades.append(t)
                too_many += 1

        profits_amount_total = profits_updater(total)
        loses_amount_total = lose_updater(total)

        balance = balance_updater(balance, profits_amount_total, loses_amount_total)


        for user in User.query.all():
            if user.id == current_user.id:
                profits_amount_total = float(profits_amount_total)
                loses_amount_total = float(loses_amount_total)
                user.balance = balance
                user.recent_loses = loses_amount_total
                user.recent_profits = profits_amount_total

                if current_user.last_login.day == last_login.day:

                    user.daily_limit = user.daily_limit + 1

                elif current_user.last_login.day < last_login_day:
                    user.daily_limit = 0



                user.last_login = last_login
                db.session.add(user)
                db.session.commit()




        # Forematting

        balance_in_btc = balance/float(btc_price_clean)
        balance = str(balance)
        balance = balance[0:7]
        profits_amount_total = str(profits_amount_total)
        profits_amount_total = profits_amount_total[0:7]
        loses_amount_total = str(loses_amount_total)
        loses_amount_total = loses_amount_total[0:7]
        demo_message = ''
        last_login = last_login.strftime('%H:%M %d-%H-%y')

        if real == 0:
            demo_message = "This  is a DEMO account. The system is automated. First deposit will transform this account into a LIVE account automatically. We respect our investors privacy, no verification documents required, any account transaction is done with Crytpo-currencies. "




        return render_template('dashboard.html',transactions=transactions, transactionhistory=transactionhistory, old_trades=old_trades, tradinghistory = tradinghistory, trades=trades, last_login=last_login, my_name=my_name, my_email=my_email, balance=balance, profits_amount_total=profits_amount_total, loses_amount_total=loses_amount_total,btc_price_clean=btc_price_clean,balance_in_btc=balance_in_btc, demo_message=demo_message)



    trades = []
    recenttrades = []
    total_old_trades = Trade.query.order_by(Trade.timestamp.desc())
    counter = 0

    for trade in total_old_trades:
        # print(trade.user_id)
        if counter <= 10:
            # print(trade)
            trades.append(trade)
            counter += 1

    for user in User.query.all():

        if user.id == current_user.id:

            if current_user.last_login.day < last_login_day:
                    user.daily_limit = 0

            db.session.add(user)
            db.session.commit()




    profits_amount_total = current_user.recent_profits
    loses_amount_total = current_user.recent_loses


    balance = current_user.balance

    balance_in_btc = balance/float(btc_price_clean)
    balance = str(balance)
    balance = balance[0:7]
    profits_amount_total = str(profits_amount_total)
    profits_amount_total = profits_amount_total[0:7]
    loses_amount_total = str(loses_amount_total)
    loses_amount_total = loses_amount_total[0:7]
    demo_message = ''


    last_login = last_login.strftime('%H:%M %d-%m-%Y UTC')




    if real == 0:
        demo_message = "This  is a DEMO account. The system is automated. First deposit will transform this account into a LIVE account automatically. We respect our investors privacy, no verification documents required, any account transaction is done with Crytpo-currencies. "




    return render_template('dashboard.html', transactions=transactions, transactionhistory=transactionhistory, old_trades=old_trades,tradinghistory = tradinghistory, trades=trades, last_login=last_login, my_name=my_name, my_email=my_email, balance=balance, profits_amount_total=profits_amount_total, loses_amount_total=loses_amount_total,btc_price_clean=btc_price_clean,balance_in_btc=balance_in_btc, demo_message=demo_message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/deposit",  methods=["GET","POST"])
@login_required
def deposit():


    if request.method == "POST":
        req = request.form

        msg = Message('Deposit Submitted', sender="support@eazycrypto.live",
                      recipients=[current_user.email])
        msg.html = render_template('mail/deposit.html', user=current_user.username)
        mail.send(msg)

        u = User.query.get(current_user.id)
        p = Transaction(action='Deposit', author=u)
        p.timestamp = datetime.utcnow()
        # print(p.timestamp)
        db.session.add(p)
        db.session.commit()

        return render_template("simple/depsub.html")

    my_name = current_user.username
    my_email = current_user.email
    balance = current_user.balance
    balance = str(balance)
    balance = balance[0:9]


    return render_template("simple/deposit.html", my_name=my_name, my_email=my_email, balance=balance)


@app.route("/withdraw",  methods=["GET","POST"])
@login_required
def withdraw():

    if request.method == "POST":
        req = request.form

        wd_amount = req['amount']

        msg = Message('WD Submitted', sender="support@eazycrypto.live",
                      recipients=[current_user.email])
        msg.html = render_template('mail/widthraw.html', user=current_user.username, withdraw=wd_amount)

        mail.send(msg)


        u = User.query.get(current_user.id)
        p = Transaction(action='WD', author=u)
        p.amount = wd_amount
        p.timestamp = datetime.utcnow()
        # print(p.timestamp)
        db.session.add(p)
        db.session.commit()

        return render_template("simple/wdsub.html")

    my_name = current_user.username
    my_email = current_user.email
    balance = current_user.balance
    balance = str(balance)
    balance = balance[0:9]

    return render_template("simple/withdraw.html", my_name=my_name, my_email=my_email, balance=balance)


#################################auth.py###########################






@app.route("/depsubmit")
def depsubmit():

    return render_template("simple/depsub.html")

@app.route("/wdsubmit")
def wdsubmit():

    return render_template("simple/wdsub.html")

@app.route("/logged_out")
def logged_out():

    return render_template("auth/loggedout.html")


@app.route("/education")
def academy():

    return render_template("simple/education.html")

@app.route("/about")
def about():

    return render_template("simple/about.html")

@app.route("/news")
def news():

    return render_template("simple/news.html")

@app.route("/exchange")
def exchange():

    return render_template("simple/exchange.html")

@app.route("/contact")
def contact():


    return render_template("simple/contact.html")



############################################ admin ###############################



admin_confirmed = False
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():

    if request.method == "POST":
        req = request.form
        if req['password'] == "c!Ep7E6SJtj9":
            global admin_confirmed
            admin_confirmed = True
            return redirect(url_for('admin'))


        return render_template('admin/login.html')

    return render_template('admin/login.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin():

    if request.method == "POST":
        global profit_now

        req = request.form
        if req['trade'] == 'go':

            profit_now = True
        elif req['trade'] == 'stop':

            profit_now = False



    global admin_confirmed
    admin_confirmed = admin_confirmed
    if admin_confirmed == True:

        admin_users_list = []
        for user in User.query.all():
            admin_users_list.append(user)




        return render_template("admin/index.html", admin_users_list=admin_users_list)
    return render_template('admin/login.html')


##################### forgot password ##############


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='support@eazycrypto.live',
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
