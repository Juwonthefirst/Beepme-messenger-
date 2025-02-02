import shelve
from flask import Flask, request, render_template
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
app=Flask(__name__)
ph=PasswordHasher()
db_location="/storage/emulated/0/Python/Beepme_messenger/database/user_database/user_database"

@app.route("/")
@app.route("/login/")
def home():
	return render_template("login.html")

		
@app.route("/signup/")
def signup_page():
	return render_template("signup.html")

		
@app.route("/welcome/", methods=["POST"])
def create_user():	
	try:
		username=(request.form.get("username")).strip(). capitalize()
		email=(request.form.get("email")).strip().lower()
		password=(request.form.get("password")).strip()
		
		user_db=shelve.open(db_location)
		username_avail=not username in user_db.keys()
		email_free=email not in user_db["email_list"]
		valid_email="@gmail.com" in email
		pass_okay=(len(password) >=  8) and (password.isalnum())
		if username_avail and email_free and valid_email and pass_okay:
			hashed_password = ph.hash(password)
			user_db.update({username:{"email": email,"pass":hashed_password, "friends":[],"settings":{}}})
			list=user_db["email_list"]
			list.append(email)
			user_db["email_list"]=list
			return render_template ("home.html", user=username)				
		else:
			error = "working"
			return render_template("signup_error.html", error=error, user=username, email=email)
	except:
		error = "working"
		return render_template("signup_error.html", error=error, user=username, email=email)
	user_db.close()

@app.route("/home/", methods=["POST"])
def login_user():
	try:
		password=request.form.get("password").strip()
		username=request.form.get("username").strip().capitalize()
		user_db=shelve.open(db_location)
		if username in user_db.keys():
			try:
				if ph.verify(user_db[username]["pass"], password):
					return render_template("home.html", user=username)
			except VerifyMismatchError:
				error="Incorrect Password"
				return render_template("login_error.html",error=error, user=username)
		else:
			error="Username doesn't exist"
			return render_template("login_error.html",error=error, user=username)
	except:
		error="An Error occurred, Please try again later"
		return render_template("login_error.html",error=error, user=username)
		
app.run(debug=True, host="0.0.0.0", port=5000)