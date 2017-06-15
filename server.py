from flask import Flask, render_template, redirect, session, flash, request
from mysqlconnection import MySQLConnector
import os, binascii,re,md5
app=Flask(__name__)
app.secret_key="123"
mysql=MySQLConnector(app,'registration')
@app.route('/')
def index():
    session['status']="loggedoff"
    # print "Index route"
    users=mysql.query_db('SELECT * FROM users')
    # print"query", users
    return render_template('registration.html')

@app.route('/registration', methods=['POST'])
def create_user():
    # print "create user route"
    # print request.form
    #Validation*******************************************
    def validation(r_form):
        error_count=[]
        # print "validation"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #check if email exists in database
        query='SELECT * FROM users WHERE email=:email'
        data={
        'email': r_form['email']
        }
        q=mysql.query_db(query,data)
        # print q
        if len(q)> 1:
            error_count+=['Please enter another email, email exists']
        #check length of first_name, last_name
        if len(r_form['first_name'])<2 or len(r_form['last_name'])<2:
            error_count+=["name fields can't be less than 2 charaters in length"]
        #check email
        if not EMAIL_REGEX.match(r_form['email']):
            error_count+=['The inputed email format is incorrect']
        #password
        if len(r_form['password']) < 8 :
            error_count+=['Password incorrect, needs to be at least 8 characters in length']
        #check if passwords match
        if r_form['password']!=r_form['c_password']:
            error_count+=["Passwords don't match"]
        return error_count
    # print "error count is " ,validation(request.form)
    error_flashes=validation(request.form)
    print "errorrrrrrrrr" ,error_flashes
    for e in error_flashes:
        flash(e,"registration")
    if len(error_flashes)>0:
        return redirect('/')
    else:
        r_password=request.form['password']
        flash('Signed up succesfully','green')
        salt =  binascii.b2a_hex(os.urandom(15))
        hashed_pw=md5.new(r_password + salt).hexdigest()
        query='INSERT INTO users(first_name,last_name,email,password,salt,created_at,updated_at) VALUES (:first_name,:last_name,:email,:password,:salt,now(),now())'
        data={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw,
        'salt': salt
        }
        mysql.query_db(query,data)
        # print 'checking input---------', mysql.query_db('SELECT * FROM users')
        session['status']="registered"
        return redirect('/success')

@app.route('/success')
def success():
    # print"success"
    return render_template('success.html')


@app.route('/login', methods=['POST'])
def login():
    # print request.form
    def login_validation(r_form):

        query='SELECT * FROM users WHERE email=:email'
        data={
        'email': r_form['email'],
        }
        q=mysql.query_db(query,data)
        if len(q) < 1:
            flash("email doesn't exist please sign up", "login")
            return redirect('/')
        else:
            hashed_pw=md5.new(r_form['password'] + q[0]['salt']).hexdigest()
            if hashed_pw!=q[0]['password']:
                flash('incorrect password', 'login')
                return redirect('/')
            else:
                print "Good! password"
                flash("You've logged in succesfully", "logged in")
                session['status']="logged in"
                return redirect('/success')

    return login_validation(request.form)
    return redirect('/')

@app.route('/logout')
def logout():
    print "logout route"
    session['status']="loggedoff"
    return redirect('/')


app.run(debug=True)
