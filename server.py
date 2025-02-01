import shelve
from flask import Flask, request, render_template
app=Flask(__name__)
from argon2 import PasswordHasher()

@app.route("/")
def home():
	return render_template("login.html")
	
@app.route("/signup/", method=["POST"])
def create_user():	
	username=request.form.get("username")
	email=request.form.get("email")
	password=request.form.get("password")
	return render_template("loading.html")
	user_db=shelve.open("/database/user_database/user_database")
	if not username in user_db.keys():
		if email not in user_db["email_list"]:
			user_db["email_list"].append(email)
			if (len(password) >=  8) and (email.isalnum()):
				ph=PasswordHasher()
				hashed_password = ph.hash(password)
				user_db.update({username:{"email": email,"pass":hashed_password}})
				return render_template ("home.html", username=user)				
			else:
				error ="Your password has to be 8 characters long and only have letters and numbers"
				return render_template("signup_error.html", error=error)
			user_db.close()
		else:
			error="Email address already in use"
			return render_template("signup_error.html",error=error)
	else:
		error="Username already in use"
		return render_template("signup_error.html",error=error)
	return True

@app.route("/login/", method=["POST"])
def login_user