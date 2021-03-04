from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import kullanicilar, sirketler

#Kullanıcı oluşturma Formu
class K_KayitFormu(FlaskForm):
    k_adi = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=10)]) #Kullanıcı Adı, boş bırakılamaz, en az 2 en fazla da 10 karakterden oluşabilir.
    k_eposta = StringField('Eposta', validators=[DataRequired(), Email()]) #Kullanıcının eposta adresi alanı
    k_parola = PasswordField('Parola', validators=[DataRequired()]) #Kullanıcı için parola alanı
    confirm_password = PasswordField('Parola\'yı Tekrar girin lütfen', validators=[DataRequired(), EqualTo('K_Parola')]) #Parolanın girilen parola ile eşitliğini kontrol ediyor  

    submit = SubmitField('Kullanıcı Oluştur')

    def validate_K_Adi(self, k_adi):
        kullanici = kullanicilar.query.filter_by(k_adi=k_adi.data).first()
        if kullanici:
            raise ValidationError('Bu isimde bir kullanıcı mevcut, lütfen başka bir kullanıcı adı giriniz.')
        
    def validate_K_EPosta(self, K_EPosta):
        kullanici = Kullanicilar.query.filter_by(K_EPosta=K_EPosta.data).first()
        if kullanici:
            raise ValidationError('Bu isimde bir eposta mevcut, lütfen başka bir eposta adresi giriniz.')

#Kullanıcı giriş  Formu
class K_GirisFormu(FlaskForm):
    K_EPosta = StringField('Eposta', validators=[DataRequired(), Email()]) #Kullanıcının eposta adresi alanı
    K_Parola = PasswordField('Parola', validators=[DataRequired()]) #Kullanıcı için parola alanı
    remember = BooleanField('Beni Hatırla')

    submit = SubmitField('Sisteme Gir')

#Kullanıcı Güncelleme Formu
class K_KayitGuncelle(FlaskForm):
    k_adi = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=10)]) #Kullanıcı Adı, boş bırakılamaz, en az 2 en fazla da 10 karakterden oluşabilir.
    k_eposta = StringField('Eposta', validators=[DataRequired(), Email()]) #Kullanıcının eposta adresi alanı

    picture = FileField('Profil Resmini Güncelle', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Profilimi Güncelle')

    def validate_K_Adi(self, k_adi):
        if k_adi.data != current_user.k_adi:
            kullanici = Kullanicilar.query.filter_by(k_adi=k_adi.data).first()
            if kullanici:
                raise ValidationError('Bu isimde bir kullanıcı mevcut, lütfen başka bir kullanıcı adı giriniz.')
        
    def validate_K_EPosta(self, K_EPosta):
        if K_EPosta.data != current_user.K_EPosta:
            kullanici = Kullanicilar.query.filter_by(K_EPosta=K_EPosta.data).first()
            if kullanici:
                raise ValidationError('Bu isimde bir eposta mevcut, lütfen başka bir eposta adresi giriniz.')

#Yeni Şirket Oluştur
class YeniSirket(FlaskForm):
    Company = StringField('Şirket Adı', validators=[DataRequired()])
    Temsilci = StringField('Temsilci', validators=[DataRequired()])
    Tms_Eposta = StringField('Temsilci Eposta', validators=[DataRequired()])
    City = StringField('Şehir', validators=[DataRequired()])
    Country = StringField('Ülke', validators=[DataRequired()])
    Domain = StringField('Domain', validators=[DataRequired()])
    Hostname = StringField('Hostname', validators=[DataRequired()])
    PubIP = StringField('IP adresi', validators=[DataRequired()])
    RevPuan = StringField('Puan', validators=[DataRequired()])
    submit = SubmitField('Kaydet')
