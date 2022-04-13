from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session, request
from flask_app import app

class Order:
    db ='Barrel_Cru'
    