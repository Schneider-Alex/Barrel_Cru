from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import partner, product
# from flask_app.controllers import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/loginpage/partner',methods=['POST','GET'])
def partners_login_page():
    session['login']="partner"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    print(session['cart'])
    return render_template('dashboard.html',all_products=product.Product.get_all_partners_products())



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/partner/register', methods=['POST'])
def register_partner():
    if partner.Partner.register_partner(request.form):
        partner.Partner.login(request.form)
        return redirect('/dashboard')
    return redirect('/loginpage/partner')

@app.route('/partner/login', methods=['POST'])
def login_partner():
    if partner.Partner.login(request.form):
        return redirect('/dashboard')
    return redirect('/loginpage/partner')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/partner/create/product')
def load_new_product_page():
    classifications=product.Product.get_all_classifications()
    return render_template('create_products.html',classifications=classifications)
    

