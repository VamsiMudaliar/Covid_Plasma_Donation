from flask import Flask,request,render_template,redirect,url_for,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app=Flask(__name__,template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///Users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

app.secret_key="Vampire"
'''app.permanent_session_lifetime = timedelta(minutes=5)
'''
db=SQLAlchemy(app)

#eng=create_engine('sqlite:///Users.sqlite3')

class Users(db.Model):
	_id=db.Column("id",db.Integer,primary_key=True)
	name=db.Column("name",db.String(100))
	email=db.Column("email",db.String(100))
	phone=db.Column("phone",db.String(10))
	password=db.Column("password",db.String(12))
	def __init__(self,name,email,phone_number,password):
		self.name=name
		self.email=email
		self.phone=phone_number
		self.password=password


class Hospital(db.Model):
	_id=db.Column("h_id",db.Integer,primary_key=True);
	hname=db.Column("hname",db.String(100));
	phone=db.Column("phone",db.String(10));
	location=db.Column("location",db.String(200));
	website=db.Column("website",db.String(200));
	branch=db.Column("branch",db.String(100));
	password=db.Column("password",db.String(100));

	def __init__(self,hname,phone,location,website,branch,password):
		self.hname=hname
		self.phone=phone
		self.location=location
		self.website=website
		self.branch=branch
		self.password=password


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/loginUser",methods=["POST","GET"])
def login():
	if request.method=="POST":
		session.permanent=True
		email=request.form['email']
		password=request.form['password']

		found_user_email = db.session.query(Users._id).filter_by(email=email).scalar() is not None

		found_user_password = db.session.query(Users._id).filter_by(password=password).scalar() is not None
		if found_user_email and found_user_password:
			session['email']=email
			return redirect(url_for('home'))

		flash(u"Invalid Email or Password ", "error")
	return render_template('login.html')



@app.route("/signupUser",methods=["POST","GET"])
def User_signup():

	if request.method=="POST":
		name=request.form['name']
		email=request.form['email']
		phone=request.form['phone']
		password=request.form['password']
		print(name,email,phone,password)
		found_user = Users.query.filter_by(name=name).first()
		if found_user:
			flash(" Account Already Exists"," info ")
			return redirect(url_for('login'))			
			
		else:
			usr=Users(name,email,phone,password)
			db.session.add(usr)
			db.session.commit()

		flash(" Account Created Successfully"," info ")

		return redirect(url_for('login'))
	return render_template('signup.html')


@app.route("/loginHospital",methods=["POST","GET"])
def Hospital_login():
	if request.method=="POST":
		session.permanent=True
		name=request.form['name']
		branch=request.form['branch']
		password=request.form['password']
		
		found_user_name = db.session.query(Hospital._id).filter_by(hname=name).scalar() is not None

		found_user_branch = db.session.query(Hospital._id).filter_by(branch=branch).scalar() is not None

		found_user_password = db.session.query(Hospital._id).filter_by(password=password).scalar() is not None
		
		if found_user_name and found_user_branch and found_user_password:
			session['name']=name

			return redirect(url_for('home'))

	return render_template("hos_login.html")


@app.route("/signupHospital",methods=["POST","GET"])
def  Hospital_signup():
	if request.method=="POST":
		name=request.form['name']
		website=request.form['website']
		phone=request.form['phone']
		branch=request.form['branch']
		password=request.form['password']
		location=request.form['location']

		found_user = Hospital.query.filter_by(hname=name).first()

		if found_user:
			flash(" Account Already Exists"," info ")
			return redirect(url_for('login'))			
			
		else:
			usr=Hospital(name,phone,location,website,branch,password)
			db.session.add(usr)
			db.session.commit()

		flash(" Account Created Successfully"," info ")

		return redirect(url_for('Hospital_login'))
	else:
		return render_template('Hospital_signup.html')

@app.route("/logout")
def logging_out():
	session.pop("email",None);

	flash("See you soon !!","info")

	return redirect(url_for("login"));



if __name__=="__main__":
	app.run(debug=True)

