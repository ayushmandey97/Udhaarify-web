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

'''
#configuring mail settings
from mail_config import mail_configure
mail_configure(app)
mail = Mail(app)
'''

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



#To send mail invites
'''
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
'''




#Adding friends
@app.route('/dashboard/add-friend', methods = ['POST'])
@is_logged_in
def add_friend():
	username = request.form['username']
	cur = mysql.connection.cursor()
	result = cur.execute("select * from users where username = %s", [username])
	if result > 0:
		result = cur.execute("select * from friends where friend1 = %s and friend2 = %s",(session['username'],username))
		
		if result == 0:
			#Now add the user to the database, handling two way friendships
			cur.execute("insert into friends (friend1, friend2) values(%s, %s)", (session['username'], username))
			cur.execute("insert into friends (friend2, friend1) values(%s, %s)", (session['username'], username))
			
			mysql.connection.commit()
			flash('Friend added successfully!','success')

		else:
			flash('Friend already added cannot be added again!','danger')
	else:
		flash('Requested username does not exist!','danger')

	cur.close()
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




#Settle up
import settle_up
@app.route('/dashboard/settleup', methods = ['GET','POST'])
@is_logged_in
def settleup():
	if request.method == 'POST':
		friend = request.form['username']
		amount = int(request.form['amount'])
		person_paying = request.form['radio']
		
		#Dont allow settling up if user not a friend
		cur = mysql.connection.cursor()
		result = cur.execute('select * from friends where friend1 = %s and friend2 = %s', (session['username'], friend))
		if result == 0:
			flash('Cannot settle up with person not added as friend!','danger')
			return redirect(url_for('dashboard'))


		#getting the sender and receiver
		if person_paying == session['username']:
			receiver = friend
			sender = session['username']
		
		elif person_paying == friend:
			receiver = session['username']
			sender = friend




		#handling cases for different payment methods
		if request.form['payment_method'] == 'online':
			print("Implement Stripe payment method.")
			#TO BE COMPLETED

		elif request.form['payment_method'] == 'cash':
			result = cur.execute('select amount from debt where sender = %s and receiver = %s',(session['username'], friend))
			if result > 0:
				#user owes this cur_amt to the friend already
				
				data = cur.fetchone()
				cur_amt = data['amount']
				
				
				if person_paying == 'user':
					cur_amt = cur_amt + amount
				elif person_paying == 'friend':
					cur_amt = cur_amt - amount
					
					if cur_amt < 0:
						#Now friend owes the user
						cur_amt = cur_amt*-1;
						cur.execute('update debt set sender = %s, receiver = %s, amount = %s where sender = %s and receiver = %s', (friend,session['username'], cur_amt, session['username'], friend))
					
					elif cur_amt > 0:
						#User still owes friend
						cur.execute('update debt set amount = %s where sender = %s and receiver = %s', (cur_amt, session['username'], friend))
					
					else:
						#case where remaining amount is zero
						cur.execute('delete from debt where sender = %s and receiver = %s', (session['username'], friend))

				mysql.connection.commit()
				cur.close()

				flash('Transaction noted successfully!', 'success')
				return redirect(url_for('dashboard'))


			result = cur.execute('select amount from debt where sender = %s and receiver = %s',(friend, session['username']))
			if result > 0:
				#The friend owes this cur_amt to the user already
				data = cur.fetchone()
				cur_amt = data['amount']

				
				if person_paying == 'user':
					cur_amt -= amount
				elif person_paying == 'friend':
					cur_amt += amount
				

				if cur_amt < 0:
					#Now User owes the Friend
					cur_amt = cur_amt*-1;
					cur.execute('update debt set sender = %s, receiver = %s, amount = %s where sender = %s and receiver = %s', (session['username'],friend, cur_amt, friend, session['username']))
				
				elif cur_amt > 0:
					#Friend still owes User
					cur.execute('update debt set amount = %s where sender = %s and receiver = %s', (cur_amt, friend, session['username']))
				
				else:
					#case where remaining amount is zero
					cur.execute('delete from debt where sender = %s and receiver = %s', (friend, session['username']))

				mysql.connection.commit()
				cur.close()

				flash('Transaction noted succesfully', 'success')
				return redirect(url_for('dashboard'))

			#No old debt exists between user and the friend at this point
			if person_paying == 'friend':
				cur.execute('insert into debt (sender, receiver, amount) values (%s, %s)', (friend,session['username'],amount))
			else:
				cur.execute('insert into debt (sender, receiver, amount) values (%s, %s)', (session['username'],friend,amount))

			mysql.connection.commit()
			cur.close()

			flash('Transaction noted!','success')
			return redirect(url_for('dashboard'))


	return render_template('settle_up.html')





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