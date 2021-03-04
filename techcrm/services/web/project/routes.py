import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from project import app, db, bcrypt 
from project.forms import K_KayitFormu, K_GirisFormu, K_KayitGuncelle, YeniSirket
from project.models import kullanicilar, sirketler
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/anasayfa')
def anasayfa():
    sirket_sayisi = sirketler.query.count()
    kullanici_sayisi = kullanicilar.query.count()
    topten_sayisi = sirketler.query.filter(sirketler.revpuan == '10').count()
    return render_template('index.html',sirket_sayisi=sirket_sayisi, kullanici_sayisi=kullanici_sayisi, topten_sayisi=topten_sayisi)
    return render_template('index.html')

@app.route('/hakkinda')
def hakkinda():
    return render_template('about.html', title='Hakkımızda')

@app.route('/tumsirketler')
def tumsirketler():
    page = request.args.get('page', 1, type=int)
    Sirketler = sirketler.query.paginate(page=page, per_page=4)
    return render_template('sirketler.html', Sirketler=Sirketler)

@app.route('/K_Kayit', methods=['GET', 'POST'])
def K_Kayit():
    if current_user.is_authenticated:
        return redirect(url_for('anasayfa'))
    form = K_KayitFormu()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.K_Parola.data).decode('utf-8')
        kullanici = kullanicilar(kullanicilaradi=form.kullanicilarAdi.data, kullanicilareposta=form.kullanicilarEPosta.data, kullanicilarparola=hashed_password)
        db.session.add(kullanici)
        db.session.commit()
        flash(f'Hesap Başarılı bir şekilde olşturuldu', 'success')
        return redirect(url_for('kullanicilarGiris'))
    return render_template('K_Kayit.html', title='Kullanıcı Oluştur', form=form)

@app.route('/K_Giris', methods=['GET', 'POST'])
def K_Giris():
    if current_user.is_authenticated:
        return redirect(url_for('anasayfa'))
    form = K_GirisFormu()
    if form.validate_on_submit():
        kullanici = kullanicilar.query.filter_by(k_eposta=form.K_EPosta.data).first()
        # if kullanici and bcrypt.check_password_hash(kullanici.k_parola, form.K_Parola.data): 
        login_user(kullanici, remember=form.remember.data)
        next_page = request.args.get('next')               
        return redirect(next_page) if next_page else redirect(url_for('anasayfa'))
    else:
        flash('Login başarısız, lütfen kontrol edin', 'danger')
    return render_template('K_Giris.html', title='Kullanıcı Girişi', form=form)

@app.route('/Logout')
def Logout():
    logout_user()
    return redirect(url_for('anasayfa'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route('/Account', methods=['GET', 'POST'])
@login_required
def Account():
    form = K_KayitGuncelle()
    if form.validate_on_submit():
         if form.picture.data:
             picture_file = save_picture(form.picture.data)
             current_user.image_file = picture_file
         current_user.k_adi = form.k_adi.data
         current_user.k_eposta = form.k_eposta.data
         db.session.commit()
         flash('Profiliniz Güncellendi', 'success')
         return redirect(url_for('Account'))
    elif request.method == 'GET':
        form.k_adi.data = current_user.k_adi
        form.k_eposta.data = current_user.k_eposta
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Hesabım', image_file=image_file, form=form)


@app.route('/sirket/yeni', methods=['GET', 'POST'])
@login_required
def Yeni_sirket():
    form = YeniSirket()
    if form.validate_on_submit():
        sirket = Sirketler(Company=form.Company.data, Temsilci=form.Temsilci.data, Tms_Eposta=form.Tms_Eposta.data, City=form.City.data, Country=form.Country.data, Domain=form.Domain.data, Hostname=form.Hostname.data, PubIP=form.PubIP.data, RevPuan=form.RevPuan.data, kullanici=current_user)
        db.session.add(sirket)
        db.session.commit()
        flash('Müşteri Kayıt Edildi', 'success')
        return redirect(url_for('tumsirketler'))
    return render_template('yeni_sirket.html', title='Yeni Musteri Oluştur', form=form, legend ='Yeni Müşteri Oluştur')

@app.route('/sirket/<int:sirket_id>')
def sirket(sirket_id):
    sirket = sirketler.query.get_or_404(sirket_id)
    return render_template('sirket.html', sirket=sirket)

@app.route('/sirket/<int:sirket_id>/update', methods=['GET', 'POST'])
@login_required
def update_sirket(sirket_id):
    sirket = sirketler.query.get_or_404(sirket_id)
    # if sirket.kullanici != current_user:
    #     abort(403)
    form = YeniSirket()
    if form.validate_on_submit():
        sirket.company = form.Company.data 
        sirket.temsilci = form.Temsilci.data  
        sirket.tms_Eposta = form.Tms_Eposta.data  
        sirket.city = form.City.data  
        sirket.country = form.Country.data  
        sirket.domain = form.Domain.data  
        sirket.hostname = form.Hostname.data  
        sirket.pubip = form.PubIP.data  
        sirket.revpuan = form.RevPuan.data  
        db.session.commit()
        flash('Müşteri Güncellendi', 'success')
        return redirect(url_for('sirket', sirket_id=sirket.id))

    elif request.method == 'GET':
        form.Company.data = sirket.company
        form.Temsilci.data = sirket.temsilci
        form.Tms_Eposta.data = sirket.tms_eposta
        form.City.data = sirket.city
        form.Country.data = sirket.country
        form.Domain.data = sirket.domain
        form.Hostname.data = sirket.hostname
        form.PubIP.data = sirket.pubip
        form.RevPuan.data = sirket.revpuan
    return render_template('yeni_sirket.html', title='Musteriyi Güncelle', form=form, legend ='Müşteriyi Güncelle')

@app.route('/sirket/<int:sirket_id>/delete', methods=['POST'])
@login_required
def delete_sirket(sirket_id):
    sirket = sirketler.query.get_or_404(sirket_id)
    # if sirket.kullanici != current_user:
    #     abort(403)
    db.session.delete(sirket)
    db.session.commit()
    flash('Müşteri Başarılı bir şekilde Silindi.', 'success')
    return redirect(url_for('tumsirketler'))
