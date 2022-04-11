from sre_constants import SUCCESS
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import partner,product
# from flask_app.controllers import

@app.route('/product/new',methods=['POST'])
def add_new_product():
    print(request.form)
    if product.Product.create_new_product(request.form):
        session['success_action']='Creation'
        return render_template('success.html')
    return redirect('/partner/create/product')