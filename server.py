from flask import Flask, render_template, redirect, session, flash, request
from mysqlconnection import MySQLConnector
import os, binascii,re,md5
app=Flask(__name__)
app.secret_key="123"
mysql=MySQLConnector(app,'registration' )
@app.route('/')
def index():
    print "Index route"
    return render_template('registration.html')

@app.route('/registration', methods=['POST'])
def create_user():
    print "create user route"
    print request.form
    return redirect('/')

@app.route('/login',methods=['POST'])
def login():
    print "login route"
    print request.form
    return redirect('/')

@app.route('/logout')
def logout():
    print "logout route"
    return redirect('/')

app.run(debug=True)
