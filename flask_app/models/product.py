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
        self.classification_id = data["classification_id"]
        self.volume = data["volume"]
        self.inventory_quantity = data["inventory_quantity"]
        self.price = data["price"]
        self.verified=data['verified']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sold_by = ''
        self.classifcation=''


    @staticmethod
    def product_parsed_data(data):
        parsed_data = {
            'partner_id' : data["partner_id"],
            'name' : data["name"],
            'description':data['description'],
            'classification_id' : data["classification_id"],
            'volume' : data["volume"],
            'inventory_quantity' : data["inventory_quantity"],
            'price' : data["price"],
            'verified':format(int(data['verified']),"b")
        }
        return parsed_data

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

    @classmethod
    def create_new_product(cls,data):
        data = cls.product_parsed_data(data)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!', data['partner_id'])
        query = """
        Insert INTO products (name, partner_id, description, classification_id, volume,inventory_quantity,price,verified)
        VALUES (%(name)s, %(partner_id)s,%(description)s, %(classification_id)s, %(volume)s,%(inventory_quantity)s,%(price)s,%(verified)s)
        ;"""
        product_id = connectToMySQL(cls.db).query_db(query, data)
        if not product_id:
            flash('Error, Please Reenter Information')
        return product_id

    @classmethod
    def get_all_partners_products(cls):
        query = """
        SELECT * FROM products
        JOIN classifications ON products.classification_id = classifications.id
        JOIN partners ON products.partner_id = partners.id
        """
        results=connectToMySQL(cls.db).query_db(query)
        products=[]
        if results:
            for row in results:
                product=cls(row)
                if int(product.inventory_quantity) > 0:
                    product.sold_by= row['partners.name']
                    product.classification=row['type']
                    products.append(product)
        return products
    

        
        return