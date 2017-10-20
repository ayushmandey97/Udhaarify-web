#Flask
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

#MySQL database
from flask_mysqldb import MySQL

#For form validation etc
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

#For password encryption
from passlib.hash import sha256_crypt

#for unauthorised url accesses
from functools import wraps 

#for sending emails
from flask_mail import Mail, Message

#creating the app engine
app = Flask(__name__)


#configuring sql settings
from sql_config import configure
configure(app)
mysql = MySQL(app)

#configuring mail settings
from mail_config import mail_configure
mail_configure(app)
mail = Mail(app)

#To avoid manual url changes to view unauthorized dashboard
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, please log in first.', 'danger')
			return redirect(url_for('login'))
	return wrap

#Homepage
@app.route('/')
def homepage():
	return render_template('home.html')



#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	return render_template('dashboard.html')

#Add friends through mail invite
@app.route('/dashboard/sendinvite', methods = ['POST'])
@is_logged_in
def invite():
	email = request.form['email']
	msg = Message('Hey, come join me at Udhaarify', sender = 'noreply.udhaarify@gmail.com', recipients = ['%s'%email])
	msg.body = "Hey, so there's this great bill splitting and expense tracking app what you should totally try out, just try it out, it will help us avoid a lot of hassles \n Here's the link: http/localhost:5000/register"
	mail.send(msg)
	flash("Invite successfully sent!", 'success')
	return redirect(url_for('dashboard'))


#LOGIN
@app.route('/login', methods = ['GET' , 'POST'])
def login():
	if request.method == 'POST':
		#get form fields
		username = request.form['username']
		password_candidate = request.form['password']

		#creating a cursor
		cur = mysql.connection.cursor()
		result = cur.execute('select * from users where username = %s', [username])
		if result > 0:
			data = cur.fetchone()
			password = data['password']

			#comparing hashes
			if sha256_crypt.verify(password_candidate, password):
				#Passes
				session['logged_in'] = True
				session['username'] = username

				flash('Successfully logged in!', 'success')
				return redirect(url_for('dashboard'))


			else:
				error = "Invalid password"
				return render_template('login.html', error=error)

			cur.close()

		else:
			error = "Username not found"
			return render_template('login.html', error=error)

	return render_template('login.html')








#REGISTRATION
class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
	confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data)) #creating password hash

		cur = mysql.connection.cursor()
		cur.execute('insert into users(name, email, username, password) values(%s, %s, %s, %s)', (name, email, username, password))
		mysql.connection.commit()
		cur.close()

		flash('Successfully registered! Log in to continue.', 'success')
		return redirect(url_for('login'))


	return render_template('register.html', form = form)

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('Successfully logged out.','success')
	return redirect(url_for('login'))




#Script only runs if explictly told, but not if imported
if __name__ == '__main__':
	app.secret_key = 'secret_key'
	app.run(debug=True)