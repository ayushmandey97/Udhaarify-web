def configure(app):
	app.config['MYSQL_HOST'] = 'localhost'
	app.config['MYSQL_USER'] = 'root'
	app.config['MYSQL_PASSWORD'] = 'ayushman.dey97'
	app.config['MYSQL_DB'] = 'udhaarify_web'
	app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
