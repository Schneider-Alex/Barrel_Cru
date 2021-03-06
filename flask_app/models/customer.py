from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session, request
from flask_app import app
import re	# the regex module
from flask_bcrypt import Bcrypt   
from flask_app.models import company, product

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
NAME_REGEX = re.compile('^(/^[A-Za-z]+$/)')
PHONE_REGEX = re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?")

 #CREATE model
class Customer:
    db = 'Barrel_Cru'
    def __init__(self, data): 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.phone_number=data['phone_number']
        self.address=data['address']
        self.company_id=data['company_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        


#CREATE model

        # Validate 
    @staticmethod
    def validate_submission(input):
        is_valid = True
        if len(input['first_name']) < 1:
            flash('First name must enter at least 1 characters', 'register')
            is_valid = False
        if len(input['last_name']) < 1:
            flash('Last name must enter at least 1 characters', 'register')
            is_valid = False
        if not PASSWORD_REGEX.match(input['password']):
            flash('password needs to be at least 8 characters and contains at least one number, one uppercase character,  and one special character', 'register')
            is_valid = False
        if input['password'] != input['confirm_password']:
            flash('passwords do not match', 'register')
            is_valid = False
        if not PHONE_REGEX.match(input['phone_number']):
            flash('phone number must be in the form 123-456-7890', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(input['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False   
        if Customer.get_customer_by_email(input):
            flash('An account already exists with this email', 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def customer_parsed_data(data):
        print("??????????????????????????????????",data)
        parsed_data={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'].lower().strip(),
            'password' : bcrypt.generate_password_hash(data['password']),
            'phone_number': data['phone_number'],
            'address' : data['address'],
            'company_id': data['company_id']
        }
        if data['new_company_name']:
            parsed_data['new_company_name'] = data['new_company_name']
            parsed_data['company_id']=company.Company.register_company(data)
        return parsed_data

    @classmethod
    def register_customer(cls, data):
        if not cls.validate_submission(data):
            return False
        data = cls.customer_parsed_data(data)
        if data['company_id'] == '':
            data['company_id']= None 
        if data['company_id'] == 'New':
            data['company_id']=company.Company.register_company(data['new_company_name'])
        #     data['company_id']=company.Company.register_company(data(new_company_name))
        query= '''
        Insert INTO customers (first_name, last_name, email, password,phone_number,address,company_id)
        VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s,%(phone_number)s,%(address)s,%(company_id)s)
        ;'''
        coach_id = connectToMySQL(cls.db).query_db(query,data)
        return coach_id

    @classmethod
    def get_customer_by_email(cls, data):
        query= '''
        SELECT *
        FROM customers
        WHERE email = %(email)s
        ;'''
        result =  connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

#READ model
    @classmethod
    def get_all_partners(cls):  
        query = """
        SELECT *
        FROM customers
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        coaches = []
        for row in result:
            coaches.append(cls(row))
        return coaches

    @classmethod
    def get_my_cart(cls):
        cart=[]
        for i in range (0,len(session['cart']),2):
            data={}
            data={
                'id' : session['cart'][i]
            }
            query= '''
            SELECT *
            FROM products
            WHERE id = %(id)s
            ;'''
            result = connectToMySQL(cls.db).query_db(query,data)
            print(result)
            if result:
                _product=product.Product(result[0])
                _product.quantity=session['cart'][i+1]
                cart.append(_product)
        print(cart)
        return cart



    @staticmethod
    def validate_update(input):
        is_valid = True
        if len(input['first_name']) < 1:
            flash('name must enter at least 1 characters', 'login')
            is_valid = False
        if len(input['last_name']) < 1:
            flash('name must enter at least 1 characters', 'login')
            is_valid = False
        if not EMAIL_REGEX.match(input['email']): 
            flash("Invalid email address!", 'login')
            is_valid = False   
        return is_valid
        # Check to see if email already in db


    @classmethod
    def login(cls,data):
        customer = Customer.get_customer_by_email(data)
        if customer:
            if bcrypt.check_password_hash(customer.password, data['password']):
                session['customer_id'] = customer.id
                session['first_name'] = customer.first_name
                session['customer'] = 1
                if 'cart' not in session:
                    session['cart']=[]
                return True
        flash('Invalid', 'login')
        return False

        
# Make a parse data function.  Takes care of much of the logic in contollers
    @staticmethod
    def parsed_data(data):
        parsed_data={
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'].lower().strip(),
            'password' : bcrypt.generate_password_hash(data['password']),
        }
        return parsed_data
