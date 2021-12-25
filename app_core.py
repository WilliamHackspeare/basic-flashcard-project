from flask import Flask,session,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db = SQLAlchemy(app)
app.secret_key = '1q2#$cf%g2^g&g$fdd6763g^RFD$%F45E%EV5'