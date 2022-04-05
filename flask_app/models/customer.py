from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session, request
from flask_app import app
import re	# the regex module
from flask_bcrypt import Bcrypt   
# from flask_app.models import 

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
NAME_REGEX = re.compile('^(/^[A-Za-z]+$/)')

 #CREATE model
class Customer:
    db = 'Barrel_Cru'
    def __init__(self, data): 
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        # self.password = data['password']
        self.phone_number=data['phone_number']
        self.address=data['address']
        self.company=data['customer_company_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#CREATE model

        # Validate 
    @staticmethod
    def validate_submission(input):
        is_valid = True
        if len(input['name']) < 1:
            flash('name must enter at least 1 characters', 'register')
            is_valid = False
        if not PASSWORD_REGEX.match(input['password']):
            flash('password needs to be at least 8 characters and contains at least one number, one uppercase character,  and one special character', 'register')
            is_valid = False
        if input['password'] != input['confirm_password']:
            flash('passwords do not match', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(input['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False   
        if Customer.get_partner_by_email(input):
            flash('An account already exists with this email', 'register')
            is_valid = False
        return is_valid

    @classmethod
    def register_customer(cls, data):
        if not cls.validate_submission(data):
            return False
        data = cls.parsed_data(data)
        query= '''
        Insert INTO customers (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s)
        ;'''
        coach_id = connectToMySQL(cls.db).query_db(query,data)
        session['coach_id'] = coach_id
        session['first_name'] = data['first_name']
        # # session['coach']=True
        # # removed this functionality so that coaches must log in after creating account
        return coach_id

    @classmethod
    def get_partner_by_email(cls, data):
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
    def get_coach_by_id(cls, id):
        data= {'id': id}
        query = '''SELECT * FROM coaches WHERE id = %(id)s;'''
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])




    @classmethod
    def update_coach(cls, data):
        print('here I am')
        query = """
        UPDATE coaches
        SET first_name = %(first_name)s, last_name = %(last_name)s,  email = %(email)s
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result


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
        # if len(input['bio']) < 1:
        #     flash('bio must enter at least 20 characters')
        #     is_valid = False
        # if len(input['coach_city']) < 1:
        #     flash('city must enter at least 1 characters')
        #     is_valid = False
        ##validation for state selector
        return is_valid
        # Check to see if email already in db


    @classmethod
    def login(cls,data):
        coach = Coach.get_coach_by_email(data)
        if coach:
            # this should change!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if bcrypt.check_password_hash(coach.password, data['password']):
                session['coach_id'] = coach.id
                session['first_name'] = coach.first_name
                session['coach'] = 1
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