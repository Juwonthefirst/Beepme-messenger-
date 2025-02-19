import  os,sqlite3
from flask import Flask, request, render_template
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from DatabaseManager import Database
app=Flask(__name__)
ph=PasswordHasher()
db=Database()
error_dict={
				"username_unavail":"Username already in use", 					"email_not_free":"E-mail already in use",								"invalid_email":"Invalid E-mail", 												"pass_not_okay":"Password needs to be 8 characters long and only have alphabet and numbers"
					}

@app.route("/")
@app.route("/login/")
def home():
	return render_template("login.html")

		
@app.route("/signup/")
def signup_page():
	return render_template("signup.html")
	

@app.route("/home/inbox/")
def check_inbox():
	return render_template("inbox.html",friends=["Juwon34","Juwon33","Juwon35"])
	
			
@app.route("/welcome/", methods=["POST"])
def create_user():
	try:
		username=(request.form.get("username")).strip(). capitalize()
		email=(request.form.get("email")).strip().lower()
		password=(request.form.get("password")).strip()
		name=db.fetch_user("username", username)
		address=db.fetch_user("email", email)		
		username_avail=(name== None,"username_unavail")
		email_free=(address == None,"email_not_free")
		valid_email=("@gmail.com" in email,"invalid_email")
		pass_okay=((len(password) >=  8) and (password.isalnum()),"pass_not_okay")
		
		if username_avail[0] and email_free[0] and valid_email[0] and pass_okay[0]:
			hashed_password = ph.hash(password)
			db.create_user(username,email,hashed_password)
			return render_template ("home.html", user=username,friends=["Juwon34","Juwon33"])		
					
		else:
			error = [error_dict.get(no_error[1]) for no_error in [username_avail,email_free,valid_email,pass_okay] if not no_error[0]]
			return render_template("signup_error.html", errors=error, user=username, email=email)
	except ValueError:
		error=["Unknown error, Please try again later"]
		return render_template("signup_error.html", errors=error, user=username, email=email)


@app.route("/home/", methods=["POST"])
def login_user():
	try:
		password=request.form.get("password").strip()
		username=request.form.get("username").strip().capitalize()
		stored_password=db.fetch_user("pass",username,search="username")
		if stored_password != None:
			try:
				if ph.verify(stored_password[0], password):
					return render_template("home.html", user=username,friends=["Juwon34","Juwon33"])
			except VerifyMismatchError:
				error="Incorrect Password"
				return render_template("login_error.html",error=error, user=username)
		else:
			error="Username doesn't exist"
			return render_template("login_error.html",error=error, user=username)
	except ValueError:
		error="An Error occurred, Please try again later"
		return render_template("login_error.html",error=error, user=username)


@app.route("/home/message",methods=["POST"])
def send_message(): 
	try:
		user=request.form.get("user")
		friend=request.form.get("friend").strip().capitalize()
		message=request.form.get("message").strip()
		db.store_message(user, friend, message)
		return render_template ("home.html",status="Message sent")
	except ValueError:
		return render_template("home.html", status="Message not sent")
	
	
@app.route("/home/inbox/messages", methods=["GET"])
def check_message():
	friend=request.form.get("friend")
	user="Juwon33"
	messages=db.fetch_message(user,friend)
	print(messages)
	return render_template("inbox.html",user="Juwon33",messages=messages,friends=["Juwon34","Juwon33","Juwon35"])
			
		
app.run(debug= True,host="0.0.0.0", port=5000)