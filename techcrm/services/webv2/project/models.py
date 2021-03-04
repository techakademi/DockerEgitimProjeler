from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_kullanici(kullanici_id):
    return kullanicilar.query.get(int(kullanici_id))

class kullanicilar(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    k_adi = db.Column(db.String(20), unique=True, nullable=False)
    k_eposta = db.Column(db.String(120), unique=True, nullable=False)
    k_parola = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    sirketler = db.relationship('sirketler', backref='kullanici', lazy=True)

    def __repr__(self):
        return f"Kullanici('{self.k_adi}', '{self.k_eposta}', '{self.image_file}',)"


class sirketler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50), nullable=False)
    temsilci = db.Column(db.String(50), nullable=False)
    tms_eposta = db.Column(db.String(50), unique=True, nullable=False) 
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    domain = db.Column(db.String(50), nullable=False)
    hostname = db.Column(db.String(50), nullable=False)
    pubip = db.Column(db.String, nullable=False)
    revpuan = db.Column(db.String, nullable=False)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanicilar.id'), nullable=False)
    
    def __repr__(self):
        return f"sirketler('{self.company}', '{self.tms_eposta}', '{self.temsilci}', '{self.tms_eposta}', '{self.city}', '{self.country}', '{self.domain}', '{self.hostname}', '{self.pubip}', '{self.revpuan}')"