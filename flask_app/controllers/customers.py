from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.controllers.partners import dashboard
from flask_app.models import customer, company,product
# from flask_app.controllers import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/loginpage/customer',methods=['POST','GET'])
def customers_login_page():
    session['login']="customer"
    return render_template('login.html',companies=company.Company.get_all_companies())

@app.route('/customer/register', methods=['POST'])
def register_customer():
    print(request.form)
    if customer.Customer.register_customer(request.form):
        print('customer has registered')
        customer.Customer.login(request.form)
        return redirect('/dashboard')
    return redirect('/loginpage/customer')

@app.route('/customer/login',methods=['POST'])
def login_customer():
    if customer.Customer.login(request.form):
        return redirect('/dashboard')
    return redirect('/loginpage/customer')

@app.route('/customer/add_to_cart', methods=['POST'])
def add_product_to_cart():
    product.Product.add_to_cart(request.form)
    return redirect('/dashboard')


