#Flask
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

#MySQL database
from flask_mysqldb import MySQL

#For form validation etc
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, FieldList, BooleanField, FormField, DateField

#For password encryption
from passlib.hash import sha256_crypt

#for unauthorised url accesses
from functools import wraps 

#for sending emails
from flask_mail import Mail, Message

#for getting the current date
import datetime

#for string to dictionary conversions
import ast

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



@app.route('/dashboard_menu/')
@is_logged_in
def dashboard_menu():
	user_owes = request.args.get('user_owes')
	user_is_owed = request.args.get('user_is_owed')
	net_amount = request.args.get('net_amount')
	friends_user_owes = ast.literal_eval(request.args.get('friends_user_owes'))
	friends_user_is_owed_by = ast.literal_eval(request.args.get('friends_user_is_owed_by'))

	return render_template('dashboard_menu.html',user_owes = user_owes, user_is_owed = user_is_owed, net_amount = net_amount, friends_user_owes = friends_user_owes, friends_user_is_owed_by = friends_user_is_owed_by)

@app.route('/all_transactions')
@is_logged_in
def all_transactions():
	return render_template('all_transactions.html')

@app.route('/first_button')
@is_logged_in
def first():
	return render_template('firstbtn.html')

@app.route('/second_button')
@is_logged_in
def second():
	return render_template('secondbtn.html')

@app.route('/add-friend-html')
@is_logged_in
def add_friend_html():
	return render_template('add-friend.html')






#Homepage
@app.route('/')
def homepage():
	return render_template('home.html')


#Dashboard
@app.route('/dashboard/')
@is_logged_in
def dashboard():
	cur = mysql.connection.cursor()
	
	user_owes = 0
	user_is_owed = 0

	username = session['username']
	
	#Getting the amount user owes in total
	result = cur.execute("select sum(amount) from debt where sender = %s", [username])
	if result > 0:
		data = cur.fetchone()
		user_owes = int(data['sum(amount)'])


	#Getting the amount is owed by friends
	result = cur.execute("select sum(amount) from debt where receiver = %s", [username])
	if result > 0:
		data = cur.fetchone()
		user_is_owed = int(data['sum(amount)'])




	net_amount = user_is_owed - user_owes
	friends_user_owes = {} #Friend dictionary whom the user owes 
	friends_user_is_owed_by = {} #Friend dictionary who owe the user

	#Adding friends to whom the user owes to dictionary
	result = cur.execute("select receiver, amount from debt where sender = %s", [username])
	if result > 0:
		data = cur.fetchall()
		for row in data:
			friends_user_owes[row['receiver']] = row['amount']

	#Adding friends who owe the user, to the dictionary
	result = cur.execute("select sender, amount from debt where receiver = %s", [username])
	if result > 0:
		data = cur.fetchall()
		for row in data:
			friends_user_is_owed_by[row['sender']] = row['amount']


	cur.close()
	#Get the total balance while templating
	return render_template('dashboard.html', user_owes = user_owes, user_is_owed = user_is_owed, net_amount = net_amount, friends_user_owes = friends_user_owes, friends_user_is_owed_by = friends_user_is_owed_by)



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

			if username != session['username']:
				#Now add the user to the database, handling two way friendships
				cur.execute("insert into friends (friend1, friend2) values(%s, %s)", (session['username'], username))
				cur.execute("insert into friends (friend2, friend1) values(%s, %s)", (session['username'], username))
				
				mysql.connection.commit()
				flash('Friend added successfully!','success')
			
			else:
				flash('Cannot add yourself as a friend!','danger')
		else:
			flash('Friend already added cannot be added again!','danger')
	else:
		flash('Requested username does not exist!','danger')

	return redirect(url_for('add_friend_html'))









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





#Settle up
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
				
				
				if person_paying == 'friend':
					cur_amt = cur_amt + amount
				elif person_paying == 'user':
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

				flash('Transaction recorded successfully!', 'success')
				return redirect(url_for('dashboard'))

			


			result = cur.execute('select amount from debt where sender = %s and receiver = %s',(friend, session['username']))
			if result > 0:
				#The friend owes this cur_amt to the user already
				data = cur.fetchone()
				cur_amt = data['amount']

				
				if person_paying == 'user':
					cur_amt = cur_amt + amount
				elif person_paying == 'friend':
					cur_amt = cur_amt - amount
				

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
				cur.execute('insert into debt (sender, receiver, amount) values (%s, %s, %s)', (friend,session['username'],amount))
			else:
				cur.execute('insert into debt (sender, receiver, amount) values (%s, %s, %s)', (session['username'],friend,amount))

			mysql.connection.commit()
			cur.close()

			flash('Transaction noted!','success')
			return redirect(url_for('dashboard'))


	return render_template('settle_up.html')


#ADD A BILL

class PaidByForm(Form):
	paid_by = StringField()
	paid_by_amount = IntegerField()	

class SplitByForm(Form):
	split_by = StringField()
	split_by_amount = IntegerField()

class PeopleInBill(Form):
	person_in_bill = StringField()

class AddBillForm(Form):
	#Description
	desc = StringField(validators = [validators.DataRequired()])
	#Amount
	amt = IntegerField(validators = [validators.DataRequired()])
	#Notes
	notes = TextAreaField()
	#Date
	date = DateField()

	#People in the bill
	people_in_bill = FieldList(FormField(PeopleInBill), min_entries = 1)

	#PAID BY
	paid_by_list = FieldList(FormField(PaidByForm), min_entries = 1)
	paid_equally = BooleanField("Paid Equally?")

	#SPLIT BY
	split_by_list = FieldList(FormField(SplitByForm), min_entries = 1)
	split_equally = BooleanField("Split Equally?")
	
def mincashflow(amount, people_in_bill, final_string, counter = 0):
	
	'''
	
	Finding the indexes of minimum and maximum values in amount[] amount[mxCredit] indicates the maximum amount to be given
	(or credited) to any person . And amount[mxDebit] indicates the maximum amount to be taken (or debited) from any person.
	So if there is a positive value in amount[], then there must be a negative value
	
	'''
	mxDebit, mxCredit = get_index(amount)

	# If both amounts are 0, then all amounts are settled
	if (amount[mxCredit] == 0 and amount[mxDebit] == 0) or (amount[mxDebit] > -1 and amount[mxDebit] < 0) or (amount[mxCredit] > 0 and amount[mxCredit] < 1):
		return

	#Find the minimum of two amounts
	minimum = minOf2(-amount[mxDebit], amount[mxCredit])
	
	amount[mxCredit] -= minimum;
	amount[mxDebit] += minimum;

	# If minimum is the maximum amount to be
	s = str(people_in_bill[mxDebit])+ " has to pay " + str(minimum) + " to " + str(people_in_bill[mxCredit])
	logger(s)
	final_string.append(s)


	#Add
	add_debt(payer = people_in_bill[mxDebit],spender = people_in_bill[mxCredit],amt = minimum)
	
	'''
	
	Recur for the amount array.  Note that it is guaranteed that
	the recursion would terminate as either amount[mxCredit] 
	or  amount[mxDebit] becomes 0
	
	'''
	mincashflow(amount, people_in_bill, final_string)

def get_index(l):
	min_index = 0
	max_index = 0

	minimum = l[0]
	maximum = l[0]

	for i in range(1,len(l)):
		if l[i] >= maximum:
			maximum = l[i]
			max_index = i

		if l[i] <= minimum:
			minimum = l[i]
			min_index = i
	
	return (min_index, max_index)



def minOf2(a,b):
	return a if a <= b else b 

def add_debt(payer, spender, amt):
	cur = mysql.connection.cursor()
	result = cur.execute("select max(bill_id) from bill_details")
	if result > 0:
		data = cur.fetchone()
		bill_id = data['max(bill_id)']
		cur.execute('insert into bill_payers (bill_id, bill_payer, amount) values (%s, %s, %s)', (bill_id, payer, amt))
		cur.execute('insert into bill_spenders (bill_id, bill_spender, amount) values (%s, %s, %s)', (bill_id, spender, amt))
		cur.execute('insert into debt (sender, receiver, amount) values (%s, %s, %s)', (spender, payer, amt))
		mysql.connection.commit()
		cur.close()


@app.route('/dashboard/add-a-bill', methods = ['GET', 'POST'])
@is_logged_in
def add_bill():
	form = AddBillForm(request.form)
	msg = ""
	if request.method == 'POST':

		#Basic bill datails
		total_amount = form.amt.data
		description = form.desc.data
		notes = form.notes.data
		current_date = form.date.data

		#If date not provided by the user, the current date is set
		if current_date == None:
			current_date = datetime.date.today()

		#Putting bill details into the database
		cur = mysql.connection.cursor()
		cur.execute('insert into bill_details (bill_amount, description, notes, date) values (%s, %s, %s, %s)', (total_amount, description, notes, current_date))
		mysql.connection.commit()
		cur.close()

		#Getting the people in the bill
		people_in_bill = []
		for entry in form.people_in_bill.entries:
			people_in_bill.append(entry.data['person_in_bill'])
		size = len(people_in_bill)
		
		#Paying details
		paid_by = []
		paid_by_amounts = []
		paid_equally = False
		for entry in form.paid_by_list.entries:
			paid_by.append(entry.data['paid_by'])
			paid_by_amounts.append(entry.data['paid_by_amount'])

		paid_equally = form.paid_equally.data

		#Spliting details
		split_by = []
		split_by_amounts = []
		split_equally = False
		for entry in form.split_by_list.entries:
			split_by.append(entry.data['split_by'])
			split_by_amounts.append(entry.data['split_by_amount'])

		split_equally = form.split_equally.data

		#if equally paid or split
		eql_paid_amt = total_amount/len(paid_by)
		eql_split_amt = total_amount/len(split_by)

		#Array storing net worth
		amount = [0]*size
		

		'''

		msg = ""
		for index, i in enumerate(split_by):
			msg += str(i)

		logger(msg)
		#logger("EXTRA PAY: " + str(paid_by_amounts[paid_by.index("ayushman")]))
		#logger("EXTRA SPLIT: " + str(split_by_amounts[split_by.index("dheeraj")]))
		'''
		
		msg = str(total_amount) + " " + str(description) + " " + str(current_date)
		for i in people_in_bill:
			msg += i

		logger(msg)

		#Adding the amounts to net worth for people who have paid
		for index, i in enumerate(people_in_bill):
			if i in paid_by:
				if paid_equally != 'True':
					amount[index] += paid_by_amounts[paid_by.index(i)]
				else:
					amount[index] += eql_paid_amt


		#Subtracting the amounts to networth for people who have spent in the bill
		for index, i in enumerate(people_in_bill):
			if i in split_by:
				if split_equally != 'True':
					amount[index] -= split_by_amounts[split_by.index(i)]
				else:
					amount[index] -= eql_split_amt
	
		#using minimum cashflow algorithm to calculate the the minimum number of transactions required 
		final_string = []
		counter = 0
		
		mincashflow(amount = amount, people_in_bill = people_in_bill, final_string = final_string)
		
		cur = mysql.connection.cursor()
		cur.execute("select max(bill_id) from bill_details")
		data = cur.fetchone()
		bill_id = data['max(bill_id)']

		
		return render_template('bill_transactions.html', transactions = final_string, bill_id = bill_id)

	return render_template('add_a_bill.html', form = form)


def logger(msg):
	print("************************************")
	print("\n\n\n")
	print(msg)
	print("\n\n\n")
	print("************************************")


#Script only runs if explictly told, but not if imported
if __name__ == '__main__':
	app.secret_key = 'secret_key'
	app.run(debug=True)