from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session, request
from flask_app import app
import re	# the regex module
from flask_bcrypt import Bcrypt   
from flask_app.models import customer

class Company:
    db = 'Barrel_Cru'
    def __init__(self, data): 
        self.id = data['id']
        self.name=data['name']
    
    @staticmethod
    def company_parsed_data(data):
        parsed_data={
            'name': data['new_company_name'],
        }
        return parsed_data

    @classmethod
    def register_company(cls, data):
        data = cls.company_parsed_data(data)
        query= '''
        Insert INTO companies (name)
        VALUES (%(name)s)
        ;'''
        company_id = connectToMySQL(cls.db).query_db(query,data)
        # # session['coach']=True
        # # removed this functionality so that coaches must log in after creating account
        return company_id

    @classmethod
    def get_all_companies(cls):  
        query = """
        SELECT *
        FROM companies
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        companies = []
        if result:
            for row in result:
                companies.append(cls(row))
        return companies