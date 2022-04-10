from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session, request
from flask_app import app
import re  # the regex module

class Product:
    db = "Barrel_Cru"

    def __init__(self, data):
        self.id = data["id"]
        self.partner_id = data["partner_id"]
        self.name = data["name"]
        self.description=data['description']
        self.classification_id = data["classification"]
        self.volume = data["volume"]
        self.inventory_quantity = data["inventory_quantity"]
        self.price = data["price"]
        self.verified=data['verified']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def  get_all_classifications(cls):
        query = """
            SELECT *
            FROM classifications
            ;"""
        result = connectToMySQL(cls.db).query_db(query)
        if not result:
            result = 'No Categories Listed'
        return result
