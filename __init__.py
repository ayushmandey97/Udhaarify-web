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


#To avoid manual url changes to view unauthorized dashboard
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, please log in first.', 'danger')
			return redirect(url_for('homepage'))
	return wrap



@app.route('/dashboard_menu')
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
	user_owes = request.args.get('user_owes')
	user_is_owed = request.args.get('user_is_owed')
	net_amount = request.args.get('net_amount')
	return render_template('firstbtn.html',user_owes = user_owes, user_is_owed = user_is_owed, net_amount = net_amount)

@app.route('/second_button')
@is_logged_in
def second():
	return render_template('secondbtn.html')

@app.route('/add-friend-html')
@is_logged_in
def add_friend_html():
	return render_template('add-friend.html')

@app.route('/delete_account', methods = ['GET', 'POST'])
@is_logged_in
def delete_account():
	if request.method == 'POST':
		password_candidate = request.form['password']
		cur = mysql.connection.cursor()
		cur.execute("select * from users where username = %s", [session['username']])
		data = cur.fetchone()
		password = data['password']

		if sha256_crypt.verify(password_candidate, password):
			result = cur.execute("select * from debt where sender = %s", [session['username']])
			if result > 0:
				flash("Clear existing debts first before deleting!", "danger")
				return redirect(url_for('delete_account'))
			else:
				cur.execute("delete from users where username = %s", [session['username']])
				cur.execute("delete from friends where friend1 = %s or friend2 = %s", (session['username'], session['username']))
				mysql.connection.commit()
				cur.close()
				flash("Successfully deleted profile!", 'success')
				
				session['username'] = None
				session['logged_in'] = False

				return redirect(url_for('homepage'))

		else:
			flash("Incorrect password, cannot delete profile!", "danger")
			return redirect(url_for('delete_account'))

	return render_template('delete_account.html')

@app.route('/change_password', methods = ['GET', 'POST'])
@is_logged_in
def change_password():

	if request.method == 'POST':
		password_candidate = request.form['password']

		#Obtained checks in js to avoid the mismatch of the following data fields
		new_password = request.form['new_password'] 
		confirm_password = request.form['confirm_password']

		if new_password != confirm_password:
			flash('Mismatching passwords!', 'danger')
			return redirect(url_for('change_password'))

		cur = mysql.connection.cursor()
		cur.execute("select * from users where username = %s", [session['username']])
		data = cur.fetchone()
		password = data['password']
		
		if sha256_crypt.verify(password_candidate, password):
			cur.execute('update users set password = %s where username = %s', (sha256_crypt.encrypt(new_password), session['username']))
			mysql.connection.commit()
			flash("Password successfully changed, login again!", 'success')
			return redirect(url_for('homepage'))
		else:
			flash("Incorrect password!", 'danger')
			return redirect(url_for('change_password'))

		return redirect(url_for('change_password'))
	return render_template('change_password.html')

#REGISTRATION
class RegisterForm(Form):
	name = StringField('', [validators.Length(min=1, max=50)])
	username = StringField('', [validators.Length(min=4, max=25)])
	email = StringField('', [validators.Length(min=6, max=50)])
	password = PasswordField('', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('')

class LoginForm(Form):
	username = StringField('', [validators.Length(min=4, max=25)])
	password = PasswordField('')

#Homepage
@app.route('/', methods = ['GET', 'POST'])
def homepage():
	form = RegisterForm(request.form)
	form2 = LoginForm(request.form)

	if request.method == 'POST':
		method = request.form['method']
		if method == 'login':
			logger("login!")
			#get form fields
			username = request.form['username']
			password_candidate = request.form['password']

			logger(str(username))
			#creating a cursor
			cur = mysql.connection.cursor()
			result = cur.execute('select * from users where username = %s', [username])
			if result > 0:
				data = cur.fetchone()
				password = data['password']

				#comparing candidate with hashed password
				if sha256_crypt.verify(password_candidate, password):
					#Passes
					session['logged_in'] = True
					session['username'] = username

					flash('Successfully logged in!', 'success')
					return redirect(url_for('dashboard'))


				else:
					flash("Invalid credentials", 'danger')
					return redirect(url_for('homepage'))

				cur.close()

			else:
				flash("Username not found", 'danger')
				return redirect(url_for('homepage'))


		elif method == 'register':
			logger('register!')
			name = form.name.data
			email = form.email.data
			username = form.username.data
			password = sha256_crypt.encrypt(str(form.password.data)) #creating password hash

			cur = mysql.connection.cursor()
			cur.execute('insert into users(name, email, username, password) values(%s, %s, %s, %s)', (name, email, username, password))
			mysql.connection.commit()
			cur.close()

			flash('Successfully registered!', 'success')
			session['logged_in'] = True
			session['username'] = username

			return redirect(url_for('dashboard'))

	return render_template('home.html', form=form, form2=form2)



@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('Successfully logged out.','success')
	return redirect(url_for('homepage'))


#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
	cur = mysql.connection.cursor()
	
	user_owes = 0
	user_is_owed = 0

	username = session['username']
	
	#Getting the amount user owes in total
	result = cur.execute("select sum(amount) from debt where sender = %s", [username])
	data = cur.fetchone()
	if data['sum(amount)'] != None:
		user_owes = int(data['sum(amount)'])


	#Getting the amount is owed by friends
	result = cur.execute("select sum(amount) from debt where receiver = %s", [username])
	data = cur.fetchone()
	if data['sum(amount)'] != None:
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


@app.route('/profile')
@is_logged_in
def profile():
	cur = mysql.connection.cursor()
	result = cur.execute("select name, username, email from users where username = %s", [session['username']])
	if result > 0:
		data = cur.fetchone()
		
		name = data['name']
		username = data['username']
		email = data['email']

	else:
		flash("User does not exist!")
	
	return render_template('profile.html', name = name, username = username, email = email)


@app.route('/show_bills/<int:id>')
@is_logged_in
def show_bills(id):
	cur = mysql.connection.cursor()
	res = cur.execute('select * from bill_details where bill_id = %s', [id])
	if res > 0:
		data = cur.fetchone()
		amount = data['bill_amount']
		description = data['description']
		notes = data['notes']
		date = data['date']

	logger(str(amount))
	result = cur.execute('select * from bill_payers where bill_id = %s', [id])
	payer_dict = {}

	if result>0:
		data = cur.fetchall()
		for row in data:
			if row['bill_payer'] not in payer_dict.keys():
				payer_dict[row['bill_payer']] = row['amount']
			else:
				payer_dict[row['bill_payer']] += row['amount']

	result = cur.execute('select * from bill_spenders where bill_id = %s', [id])
	spender_dict = {}

	if result>0:
		data = cur.fetchall()
		for row in data:
			if row['bill_spender'] not in spender_dict.keys():
				spender_dict[row['bill_spender']] = row['amount']
			else:
				spender_dict[row['bill_spender']] += row['amount']

	msg = ""
	for i in payer_dict:
		msg += str(i) + ":" + str(payer_dict[i])
	logger(msg)
	msg = ""
	for i in spender_dict:
		msg += str(i) + ":" + str(spender_dict[i])
	logger(msg)
	return render_template('show_bills.html', amount=amount, desc=description, notes=notes, date=date, payer_dict=payer_dict, spender_dict=spender_dict, bill_id=id)



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
				return redirect(url_for('settleup'))

			
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
				return redirect(url_for('settleup'))
				
			
			#No old debt exists between user and the friend at this point
			if person_paying == 'friend':
				cur.execute('insert into debt (sender, receiver, amount) values (%s, %s, %s)', (friend,session['username'],amount))
			else:
				cur.execute('insert into debt (sender, receiver, amount) values (%s, %s, %s)', (session['username'],friend,amount))

			mysql.connection.commit()
			cur.close()

			flash('Transaction noted!','success')
			return redirect(url_for('settleup'))


	return render_template('settleup.html')


#ADD A BILL

class PaidByForm(Form):
	paid_by = StringField("")
	paid_by_amount = IntegerField("")	

class SplitByForm(Form):
	split_by = StringField("")
	split_by_amount = IntegerField("")

class PeopleInBill(Form):
	person_in_bill = StringField("")

class AddBillForm(Form):
	#Description
	desc = StringField("Description", validators = [validators.DataRequired()])
	#Amount
	amt = IntegerField("Amount", validators = [validators.DataRequired()])
	#Notes
	notes = TextAreaField("Notes")
	#Date
	date = DateField("Date")

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
	s = str(people_in_bill[mxDebit])+ " has to pay " + str(int(minimum)) + " to " + str(people_in_bill[mxCredit])
	logger(s)
	final_string.append(s)


	#Add
	add_debt(spender = people_in_bill[mxDebit], payer = people_in_bill[mxCredit], amt = minimum)
	
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
		
		#Equivalent to settle up
		redundancy_check(sender=spender, receiver=payer, amt=amt)
		
		mysql.connection.commit()
		cur.close()


def redundancy_check(sender, receiver, amt):
	cur = mysql.connection.cursor()
	result = cur.execute('select amount from debt where sender = %s and receiver = %s',(sender, receiver))
	if result > 0:
		#sender already owes to receiver
		data = cur.fetchone()
		cur_amt = data['amount']
		
		cur_amt += amt
		cur.execute('update debt set amount = %s where sender = %s and receiver = %s', (cur_amt, sender, receiver))
		mysql.connection.commit()
		return

	
	result = cur.execute('select amount from debt where sender = %s and receiver = %s',(receiver, sender))

	if result > 0:
		logger("Case2")
		#receiver already owes the sender
		data = cur.fetchone()
		cur_amt = data['amount']
		cur_amt -= amt
		logger(str(cur_amt))
		if cur_amt < 0:
			#Now sender owes the receiver
			cur_amt = cur_amt*-1;
			cur.execute('update debt set sender = %s, receiver = %s, amount = %s where sender = %s and receiver = %s', (sender,receiver, cur_amt, receiver, sender))
		
		elif cur_amt > 0:
			#receiver still owes the sender
			cur.execute('update debt set amount = %s where sender = %s and receiver = %s', (cur_amt, receiver, sender))
		
		else:
			#case where remaining amount is zero
			cur.execute('delete from debt where sender = %s and receiver = %s', (receiver, sender))

		mysql.connection.commit()
		return
		
	
	#No old debt exists between user and the friend at this point
	cur.execute('insert into debt (sender, receiver, amount) values (%s, %s, %s)', (sender, receiver, amt))
	mysql.connection.commit()
	return



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
			msg += str(entry.data['paid_by_amount']) + " "

		paid_equally = form.paid_equally.data

		#Spliting details
		split_by = []
		split_by_amounts = []
		split_equally = False

		for entry in form.split_by_list.entries:
			split_by.append(entry.data['split_by'])
			split_by_amounts.append(entry.data['split_by_amount'])
			msg += str(entry.data['split_by_amount']) + " "

		split_equally = form.split_equally.data

		#if equally paid or split
		eql_paid_amt = total_amount/len(paid_by)
		eql_split_amt = total_amount/len(split_by)

		#Array storing net worth
		amount = [0]*size

		#Adding the amounts to net worth for people who have paid
		for index, i in enumerate(people_in_bill):
			if i in paid_by:
				if paid_equally != True:
					amount[index] += paid_by_amounts[paid_by.index(i)]
				else:
					amount[index] += eql_paid_amt


		#Subtracting the amounts to networth for people who have spent in the bill
		for index, i in enumerate(people_in_bill):
			if i in split_by:
				if split_equally != True:
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