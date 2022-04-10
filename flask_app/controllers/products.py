from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import partner,product
# from flask_app.controllers import

@app.route('/product/new')
def add_new_product():
    
    return render_template('create_products.html',categories=categories)