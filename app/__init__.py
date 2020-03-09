from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager
import os




from flask_mail import Mail




app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['MAIL_SERVER']='mail.privateemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'support@eazycrypto.live'
app.config['MAIL_PASSWORD'] = 'David071182'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = app.testing
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAIL_DEBUG'] = app.debug

mail = Mail(app)

app.config['SECRET_KEY'] = 'dJU^3+9maH$v'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# 'sqlite:///database.db'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes
