from flask import render_template, flash, redirect,request,url_for,request,session,abort
import sqlite3
import sys
from flask import g
from app import app
from .forms import LoginForm
from .forms import SigninForm
from .forms import EnteryForm
from .forms import DataForm

@app.before_request
def before_request():
    g.db = sqlite3.connect("databook.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SigninForm()
	log = g.db.execute("SELECT * FROM userdata").fetchall()
	if form.validate_on_submit():
		user=form.idu.data
		pswd=form.passcode.data
		try:
			log = g.db.execute("SELECT * FROM userdata").fetchall()
			for u in log:
				if u[0] == user and u[1] == pswd:
					session['username']=user
	        			return redirect(url_for('login'))
			flash('Worng Username Or Password =%s' % form.idu.data)
		except:
			pass
		finally:
			g.db.close()
				
	return render_template('index.html',title='Home',form=form)

app.route('</user>')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = LoginForm()
	if form.validate_on_submit():
		username=form.openid.data
		pswd=form.password.data
		pswdre=form.passwordre.data
		userdata=(username,pswd)
		try:
			#g.db.execute("CREATE TABLE IF NOT EXISTS userdata(name TEXT,say TEXT)")
			log = g.db.execute("SELECT uname FROM userdata").fetchall()
			if pswd == pswdre:
				for s in log:
					if s[0] is not username: 
						g.db.execute("INSERT INTO userdata VALUES(?,?)",userdata)
						g.db.commit()	
						flash('Login requested for OpenID=%s' % form.openid.data)
	        				return redirect('/index')
			else:
				flash('Password Not match=%s' % form.openid.data)
		except sqlite3.IntegrityError:
			flash('Take Another Username , User already exist')
		finally:
			g.db.close()	
	return render_template('signup.html',title='Signup',form=form)

app.route('</user>')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = DataForm()
    if not 'username' in session:
	return abort(403)
    else:
	name=session['username']
   # g.db.execute("CREATE TABLE IF NOT EXISTS blogdata(name TEXT,say TEXT)")
    	if form.validate_on_submit():
		val=form.says.data
		blogdata=(name,val)
		try:
			g.db = sqlite3.connect("databook.db")
			g.db.execute("CREATE TABLE IF NOT EXISTS comment(user TEXT,says TEXT)")
		        g.db.execute("INSERT INTO comment VALUES(?,?)",blogdata)
			g.db.commit()        
		except:
			pass
		
		finally:
			val = g.db.execute("SELECT * FROM comment").fetchall()
	        	return render_template('login.html',val=val,title='Blog',form=form,name=name)
    	return render_template('login.html',title='Blog',form=form,name=name)

@app.route('/record')
def record():
	values = g.db.execute("SELECT * FROM comment").fetchall()
	return render_template('record.html',title='Record',values=values)

@app.route('/project')
def project():
	return render_template("project.html",title='contact')
