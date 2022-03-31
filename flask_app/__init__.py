from flask import Flask, session
app = Flask(__name__)
from dotenv import load_dotenv 
import os

load_dotenv()
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
