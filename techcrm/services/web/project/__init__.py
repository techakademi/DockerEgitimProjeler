from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbroot:rootman@postgres-db:5432/techakademicrm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'e8642220f18191912969a2a63abff056' #python komutu ile python'u çalıştırdıktan sonra, import secrets sonrasında ise secrets.token_hex(16) komutu ile yeni bir secret key oluşturuyoruz.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'K_Giris'
login_manager.login_message_category = 'info'

from project import routes