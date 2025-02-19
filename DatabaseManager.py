import sqlite3


class Database:
	def __init__(self, db_location="database.db"):
		self.database=db_location

		
	def connect(self):
		return sqlite3.connect(self.database,check_same_thread=False)

	
	def create_user(self,name,email,password):
		with self.connect() as db:
			cursor=db.cursor()
			cursor.execute("INSERT INTO users (username,email,pass) VALUES(?,?,?)",(name,email, password))
			db.commit()


	def fetch_user(self, area,user_detail,search=None):
		match area:
			case "pass" | "username" | "email":
				if search == None:
					search = area
				with self.connect() as db:
					cursor=db.cursor()
					return cursor.execute(f"SELECT {area} FROM users WHERE {search}= ?",(user_detail,)).fetchone()
			case _:
				raise TypeError

	
	def store_message(self, sender, receiver, message):
		with self.connect() as db:
			cursor=db.cursor()
			cursor.execute("INSERT INTO messages (sender, receiver, message) VALUES (?,?,?)",(sender, receiver, message))
			db.commit()


	def fetch_message(self,user, friend):
		with self.connect() as db:
			cursor=db.cursor()
			return cursor.execute("SELECT message FROM messages WHERE sender= ? AND receiver= ?",(friend,user)).fetchall()
	
	