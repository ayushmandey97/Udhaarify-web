#Flask
from flask import Flask, render_template

'''
#MySQL database
from flask_mysldb import MySQL

#For form validation etc
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

#For password encryption
from passlib.hash import sha256_crypt

#for unauthorised url accesses
from functools import wraps '''

#creating the app engine
app = Flask(__name__)

#Homepage
@app.route('/')
def homepage():
	return render_template('homepage.html')


#Script only runs if explictly told, but not if imported
if __name__ == '__main__':
	app.run(debug=True)