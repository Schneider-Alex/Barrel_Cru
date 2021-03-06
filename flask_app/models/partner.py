from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session, request
from flask_app import app
import re  # the regex module
from flask_bcrypt import Bcrypt

# from flask_app.models import

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASSWORD_REGEX = re.compile(
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
)
NAME_REGEX = re.compile("^(/^[A-Za-z]+$/)")
PHONE_REGEX = re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?")

# CREATE model
class Partner:
    db = "Barrel_Cru"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.email = data["email"]
        self.password = data["password"]
        self.phone_number = data["phone_number"]
        self.address = data["address"]
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']

    # CREATE model

    # Validate
    @staticmethod
    def validate_submission(input):
        is_valid = True
        if len(input["name"]) < 1:
            flash("name must be at least 1 characters", "register")
            is_valid = False
        if not PASSWORD_REGEX.match(input["password"]):
            flash(
                "password needs to be at least 8 characters and contains at least one number, one uppercase character,  and one special character",
                "register",
            )
            is_valid = False
        if input["password"] != input["confirm_password"]:
            flash("passwords do not match", "register")
            is_valid = False
        if not PHONE_REGEX.match(input["phone_number"]):
            flash("phone number must be in the form 123-456-7890", "register")
            is_valid = False
        if not EMAIL_REGEX.match(input["email"]):
            flash("Invalid email address!", "register")
            is_valid = False
        if Partner.get_partner_by_email(input):
            flash("An account already exists with this email", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def parsed_data(data):
        parsed_data = {
            "name": data["name"],
            "email": data["email"].lower().strip(),
            "password": bcrypt.generate_password_hash(data["password"]),
            "phone_number": data["phone_number"],
            "address": data["address"],
        }
        return parsed_data

    @classmethod
    def register_partner(cls, data):
        if not cls.validate_submission(data):
            return False
        data = cls.parsed_data(data)
        query = """
        Insert INTO partners (name, email, password, phone_number, address)
        VALUES (%(name)s, %(email)s,%(password)s, %(phone_number)s, %(address)s)
        ;"""
        partner_id = connectToMySQL(cls.db).query_db(query, data)
        # partner=cls(Partner.get_partner_by_email(data['email']))
        # session["partner_id"] = partner.id
        # session["name"] = partner.name
        # session["partner"] = 1
        return partner_id

    @classmethod
    def get_partner_by_email(cls, data):
        query = """
        SELECT *
        FROM partners
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    # READ model
    @classmethod
    def get_all_partners(cls):
        query = """
        SELECT *
        FROM partners
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        coaches = []
        for row in result:
            coaches.append(cls(row))
        return coaches


    @staticmethod
    def validate_update(input):
        is_valid = True
        if len(input["first_name"]) < 1:
            flash("name must enter at least 1 characters", "login")
            is_valid = False
        if len(input["last_name"]) < 1:
            flash("name must enter at least 1 characters", "login")
            is_valid = False
        if not EMAIL_REGEX.match(input["email"]):
            flash("Invalid email address!", "login")
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
    def login(cls, data):
        print('running log in')
        partner = Partner.get_partner_by_email(data)
        if partner:
            if bcrypt.check_password_hash(partner.password, data["password"]):
                session["partner_id"] = partner.id
                session["name"] = partner.name
                session["partner"] = 1
                return True
        flash("Invalid", "login")
        return False
