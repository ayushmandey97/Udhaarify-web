def mail_configure(app):
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = 'noreply.udhaarify@gmail.com'
	app.config['MAIL_PASSWORD'] = 'joblessdheeraj'
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True