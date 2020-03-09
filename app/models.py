from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import time



from app import app, db, bootstrap, login_manager, mail



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    balance = db.Column(db.Float, default=5000.00)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    real = db.Column(db.Integer, default=0)
    recent_profits = db.Column(db.Float, default=0)
    recent_loses = db.Column(db.Float, default=0)
    trades = db.relationship('Trade', backref='author', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='author', lazy='dynamic')
    daily_limit = db.Column(db.Integer, default=0)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)




    def __repr__(self):
        return '<User %r>' % (self.username)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    level = db.Column(db.Integer(), default=1)
    asset = db.Column(db.String(40))
    position = db.Column(db.String(20))
    amount = db.Column(db.Float())
    outcome = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Trade %r>' % (self.asset)
# email = StringField('email', validators=[InputRequired(), Length(min=3, max=80)])

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(50), default='Pending')
    action = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Pending")
    method = db.Column(db.String(50), default="BTC")
    amount = db.Column(db.String(50), default="Varifying Block")
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Transaction %r>' % (self.method)
