from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import partner
# from flask_app.controllers import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/partner/login')
def partners_login_page():
    session['login']="partner"
    return render_template('login.html')

@app.route('/partner/register', methods=['POST'])
def register_partner():
    if partner.Partner.register_partner(request.form):
        print('partner has registered')
        # partner.Partner.login(request.form)
        return render_template('dashboard.html')
    return redirect('/partner/login')

@app.route('/partner/login', methods=['POST'])
def login_partner():
    if partner.Partner.login(request.form):
        return render_template('dashboard.html')
    return redirect('/partner/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

