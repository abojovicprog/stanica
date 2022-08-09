from asyncio import proactor_events
from crypt import methods
from textwrap import wrap
from datetime import date, datetime
from distutils.log import error
from operator import contains
from dateutil.relativedelta import relativedelta
from email.policy import default
from os import sep, terminal_size
from re import L
from flask import Flask, request, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lica.db' ##glavna baza
app.config['SQLALCHEMY_BINDS'] = {'poternica' : 'sqlite:///poternica.db',
                                  'login' : 'sqlite:///login'} # baza za lica sa poternicom

db = SQLAlchemy(app)

#model za glavnu bazu
class Lice(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    datum_rodjenja = db.Column(db.String(100), nullable=False)
    jmbg = db.Column(db.String(100), nullable=False)
    brojlk = db.Column(db.String(100), nullable=False)
    pol = db.Column(db.String(100), nullable=False)
    mesto_rodjenja = db.Column(db.String(100), nullable=False)
    prebivaliste = db.Column(db.String(100), nullable=False)
    link_slike = db.Column(db.String(255), nullable=False)
    datum_lk = db.Column(db.DateTime)
    datum_isteka_lk = db.Column(db.DateTime)
    poternica = db.Column(db.Boolean)
    porodica = db.Column(db.String(255))

#model za bazu sa poternicom
class Poternica(db.Model): 
    __bind_key__ = 'poternica'
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    datum_rodjenja = db.Column(db.String(100), nullable=False)
    jmbg = db.Column(db.String(100), nullable=False)
    brojlk = db.Column(db.String(100), nullable=False)
    pol = db.Column(db.String(100), nullable=False)
    mesto_rodjenja = db.Column(db.String(100), nullable=False)
    prebivaliste = db.Column(db.String(100), nullable=False)
    link_slike = db.Column(db.String(255), nullable=False)
    datum_lk = db.Column(db.DateTime)
    datum_isteka_lk = db.Column(db.DateTime)
    poternica = db.Column(db.Boolean)
    krivicno_delo = db.Column(db.String(255))

class LoginCred(db.Model):
    __bind_key__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Boolean, default=False)

###################### metode za pristupanje stranicama sa index-a #####################################

@app.route('/')
def pocetak():
    return render_template('login.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template('admin.html')

@app.route('/dodaj_login', methods=['POST', 'GET'])
def dodaj_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_forma = request.form.get('admin')
        if admin_forma:
            admin = True
        else:
            admin = False
        login = LoginCred(username=username, password=password, admin=admin)
        if not LoginCred.query.filter_by(username=username, password=password).all():
            try:
                db.session.add(login)
                db.session.commit()
                return render_template('greska.html', greska='Podaci za prijavu uspesno dodati')
            except:
                return render_template('greska.html', greska='Nije moguce dodati podatke za prijavu')
        else:
            return render_template('greska.html', greska='Vec postoji osoba sa istim podacima')
        
    else:
        pass


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form['username']
    password = request.form['password']
    if request.method == 'POST':
        login = LoginCred.query.filter_by(username=username, password=password).first()
        if login:
            return render_template('index.html', admin=login.admin)
        else:
            return render_template('greska.html', greska='Prijava nije uspela')
    else:
        return render_template('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/pretraga', methods=['POST', 'GET'])
def pretraga():
        return render_template('pretraga.html')

@app.route('/novo_lice', methods=['POST', 'GET'])
def novo_lice():
    if request.method == 'POST':
        pass
    else:
        return render_template('novo_lice.html')

@app.route('/poternica_spisak', methods=['POST', 'GET'])
def poternica_spisak():
    poternica = Poternica.query.order_by(Poternica.id).all()
    if len(poternica) > 0:
        return render_template('lica_sa_poternicom.html', poternica=poternica) 
    else:
        return render_template('greska.html', greska='Trenutno ne postoje lica za kojima je raspisana poternica.')

@app.route('/repr/<string:jmbg>', methods=['POST', 'GET'])
def repr(jmbg):
    trazeno_lice = Lice.query.filter_by(jmbg=jmbg).first()
    if request.method == 'POST':
        try:
            id = trazeno_lice.id
            ime = trazeno_lice.ime
            prezime = trazeno_lice.prezime
            datum = trazeno_lice.datum_rodjenja
            jmbg = trazeno_lice.jmbg
            brojlk = trazeno_lice.brojlk
            pol = trazeno_lice.pol
            mesto_rodjenja = trazeno_lice.mesto_rodjenja
            prebivaliste = trazeno_lice.prebivaliste
            link_slike = trazeno_lice.link_slike
            datum_lk = trazeno_lice.datum_lk
            datum_isteka_lk = trazeno_lice.datum_isteka_lk
            poternica = trazeno_lice.poternica
            porodica = trazeno_lice.porodica
            return render_template('repr.html', id=id, ime=ime, prezime=prezime, datum_rodjenja=datum, jmbg=jmbg, brojlk=brojlk, pol=pol, mesto_rodjenja=mesto_rodjenja, prebivaliste=prebivaliste, datum_lk=datum_lk, datum_isteka_lk=datum_isteka_lk, link_slike=link_slike, poternica=poternica, porodica=porodica)
        except:
            return render_template('greska.html', greska='Nije moguce ispisati podatke o licu')
    else:
        return redirect('/')

@app.route('/pretrazi_ime/<int:jmbg>', methods=['POST', 'GET'])
def pretrazi_ime(jmbg):
    return render_template('pretrazi_ime.html', jmbg=jmbg)

############################# CRUD za glavnu bazu #################################################
@app.route('/dodaj', methods=['GET', 'POST'])
def dodaj():
    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        datum = request.form['datum']
        jmbg = request.form['jmbg']
        brojlk = request.form['brojlk']
        pol = request.form['pol']
        mesto_rodjenja = request.form['mesto_rodjenja']
        prebivaliste = request.form['prebivaliste']
        slika = request.form['link_slike']
        datum_lk = datetime.today()
        datum_isteka_lk = datum_lk + relativedelta(years=5)
        poternica = False
        porodica = ""
        if not Lice.query.filter_by(jmbg=jmbg).all() and not Lice.query.filter_by(brojlk=brojlk).all():
            novo_lice = Lice(ime = ime, prezime = prezime, datum_rodjenja = datum, jmbg = jmbg, brojlk = brojlk, pol = pol, mesto_rodjenja = mesto_rodjenja, prebivaliste = prebivaliste, datum_lk=datum_lk, datum_isteka_lk=datum_isteka_lk, link_slike=slika, poternica=poternica, porodica=porodica)
        else:
            return render_template('greska.html', greska='Osoba vec postoji')
        
        try:
            db.session.add(novo_lice)
            db.session.commit()
        except:
            return render_template('greska.html', greska='Greska pri dodavanju lica')
        return redirect('/')
        

    else:
        return render_template('novo_lice.html')


@app.route('/obrisi/<string:jmbg>', methods=['GET', 'POST'])
def brisanje(jmbg):
    print(jmbg)
    lice_za_brisanje = Lice.query.filter_by(jmbg=jmbg).first()
    poternica_za_brisanje =  Poternica.query.filter_by(jmbg=jmbg).first()
    if request.method == 'GET': 
        try:
            if poternica_za_brisanje is not None:
                db.session.delete(poternica_za_brisanje)
                db.session.commit()
            if lice_za_brisanje is not None:
                db.session.delete(lice_za_brisanje)
                db.session.commit()
            return render_template('greska.html', greska='Podaci o licu uspesno obrisani.')
        except:
            return render_template('greska.html', greska='Nije moguce obrisati podatke o licu.')
    else:
        return 'sajk'
        



@app.route('/pretrazi_po_jmbg', methods=['GET', 'POST'])
def pretrazi_po_jmbg():
    trazeni_jmbg = request.form['trazeni_jmbg']
    trazeno_lice = Lice.query.filter_by(jmbg=trazeni_jmbg).first()
    if request.method == 'POST':
        try:
            id = trazeno_lice.id
            ime = trazeno_lice.ime
            prezime = trazeno_lice.prezime
            datum = trazeno_lice.datum_rodjenja
            jmbg = trazeno_lice.jmbg
            brojlk = trazeno_lice.brojlk
            pol = trazeno_lice.pol
            mesto_rodjenja = trazeno_lice.mesto_rodjenja
            prebivaliste = trazeno_lice.prebivaliste
            link_slike = trazeno_lice.link_slike
            datum_lk = trazeno_lice.datum_lk
            datum_isteka_lk = trazeno_lice.datum_isteka_lk
            poternica = trazeno_lice.poternica
            porodica = trazeno_lice.porodica
            print(id, ime, prezime, datum, jmbg, brojlk, pol, mesto_rodjenja, prebivaliste, link_slike, datum_lk, datum_isteka_lk, poternica, porodica)
            return render_template('repr.html', id=id, ime=ime, prezime=prezime, datum_rodjenja=datum, jmbg=jmbg, brojlk=brojlk, pol=pol, mesto_rodjenja=mesto_rodjenja, prebivaliste=prebivaliste, datum_lk=datum_lk, datum_isteka_lk=datum_isteka_lk, link_slike=link_slike, poternica=poternica, porodica=porodica)
        except:
            return render_template('greska.html', greska='Ne postoji lice sa trazenim JMBG')
    else:
        return redirect('/')

@app.route('/pretrazi_po_brojlk', methods=['POST', 'GET'])
def pretrazi_po_brojlk():
    trazeni_brojlk = request.form['trazeni_brojlk']
    trazeno_lice = Lice.query.filter_by(brojlk=trazeni_brojlk).first()
    if request.method == 'POST':
        try:    
            id = trazeno_lice.id
            ime = trazeno_lice.ime
            prezime = trazeno_lice.prezime
            datum = trazeno_lice.datum_rodjenja
            jmbg = trazeno_lice.jmbg
            brojlk = trazeno_lice.brojlk
            pol = trazeno_lice.pol
            mesto_rodjenja = trazeno_lice.mesto_rodjenja
            prebivaliste = trazeno_lice.prebivaliste
            link_slike = trazeno_lice.link_slike
            datum_lk = trazeno_lice.datum_lk
            datum_isteka_lk = trazeno_lice.datum_isteka_lk
            poternica = trazeno_lice.poternica
            porodica = trazeno_lice.porodica
            return render_template('repr.html', id=id, ime=ime, prezime=prezime, datum_rodjenja=datum, jmbg=jmbg, brojlk=brojlk, pol=pol, mesto_rodjenja=mesto_rodjenja, prebivaliste=prebivaliste, datum_lk=datum_lk, datum_isteka_lk=datum_isteka_lk, link_slike=link_slike, poternica=poternica, porodica=porodica)
        except:
            return render_template('greska.html', greska='Ne postoji osoba sa trazenim brojem licne karte')
    else:
        return redirect('/')
    
@app.route('/pretraga_po_imenu_dodaj', methods=['GET', 'POST'])
def pretraga_po_imenu_dodaj():
    jmbg = request.form['jmbg']
    print(jmbg)
    trazeno_imeprezime = request.form['trazeno_ime']
    print(trazeno_imeprezime)
    imeprezime = trazeno_imeprezime.split(" ")
    trazena_lica = Lice.query.filter_by(ime=imeprezime[0]).all()
    spisak = []
    for lica in trazena_lica:   
        if lica.ime.startswith(imeprezime[0]):
            if lica.prezime.startswith(imeprezime[1]):
                spisak.append(lica)
    if request.method == 'POST':
        try:
            return render_template('spisak_porodica.html', jmbg=jmbg, lica=spisak)
        except:
            return render_template('greska.html', greska='nj')

@app.route('/pretraga_po_imenu', methods=['GET', 'POST'])
def pretraga_po_imenu():
    trazeno_imeprezime = request.form['trazeno_ime']
    print(trazeno_imeprezime)
    imeprezime = trazeno_imeprezime.split(" ")
    trazena_lica = Lice.query.filter_by(ime=imeprezime[0]).all()
    spisak = []
    for lica in trazena_lica:   
        if lica.ime.startswith(imeprezime[0]):
            if lica.prezime.startswith(imeprezime[1]):
                spisak.append(lica)
    if request.method == 'POST':
        try:
            return render_template('spisak_lica_prikaz.html', lica=spisak)
        except:
            return render_template('greska.html', greska='nj')  

@app.route('/dodaj_porodicu', methods=['POST', 'GET'])
def dodaj_porodicu():
    if request.method == 'POST':
        jmbg_porodica = request.form['jmbg_porodica']
        jmbg_lica = request.form['jmbg_lica']
        lice = Lice.query.filter_by(jmbg=jmbg_lica).first()
        if lice.porodica is None:    
            lice.porodica = f"{jmbg_porodica}g"
        else:
            lice.porodica += f"{jmbg_porodica}g"
        print(lice.porodica)
        try:
            db.session.commit()
            return render_template('greska.html', greska='chil')
        except:
            return render_template('greska.html', greska='aaaaaaa')
    else:
        return redirect('/')
@app.route('/spisak_porodica/<string:porodica>', methods=['POST', 'GET'])
def spisak_porodica(porodica):
    spisak = []
    porodica_jmbg = porodica.split('g')
    for clan in porodica_jmbg:
        lice = Lice.query.filter_by(jmbg=clan).first()
        spisak.append(lice)
    return render_template('spisak_porodica.html', lica=spisak)

############################################ CRUD za poternicu #########################################################

@app.route('/unos_dela/<int:id>', methods=['POST', 'GET'])
def prikaz_unos_dela(id):
    return render_template('dodaj_poternicu.html', id=id)

@app.route('/poternica_dodaj/<int:id>', methods=['POST', 'GET'])
def poternica_dodaj(id):
    delo = request.form['krivicno_delo']
    trazeno_lice = Lice.query.get_or_404(id)
    id = trazeno_lice.id
    ime = trazeno_lice.ime
    prezime = trazeno_lice.prezime
    datum = trazeno_lice.datum_rodjenja
    jmbg = trazeno_lice.jmbg
    brojlk = trazeno_lice.brojlk
    pol = trazeno_lice.pol
    mesto_rodjenja = trazeno_lice.mesto_rodjenja
    prebivaliste = trazeno_lice.prebivaliste
    link_slike = trazeno_lice.link_slike
    datum_lk = trazeno_lice.datum_lk
    datum_isteka_lk = trazeno_lice.datum_isteka_lk
    poternica = trazeno_lice.poternica
    lice_za_poternicu = Poternica(id=id, ime=ime, prezime=prezime, datum_rodjenja=datum, jmbg=jmbg, brojlk=brojlk, pol=pol, mesto_rodjenja=mesto_rodjenja, prebivaliste=prebivaliste, datum_lk=datum_lk, datum_isteka_lk=datum_isteka_lk, link_slike=link_slike, poternica=poternica, krivicno_delo=delo)
    if request.method == 'POST':
        trazeno_lice.poternica = 1
        try:    
            db.session.add(lice_za_poternicu)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('greska.html', greska='Nije moguce dodati lice na spisak lica sa poternicom')
    else:
        return redirect('/')
    
@app.route('/poternica_ukloni/<int:id>', methods=['POST', 'GET'])
def poternica_ukloni(id):
    trazeno_lice = Poternica.query.get_or_404(id)
    jmbg = trazeno_lice.jmbg
    lice_baza = Lice.query.filter_by(jmbg=jmbg).first()
    lice_baza.poternica = 0
    if request.method == 'GET':
        try:    
            db.session.delete(trazeno_lice)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('greska.html', greska='Nije moguce ukloniti lice sa spiska lica sa poternicom')
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
