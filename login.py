#python version 310
from pickle import FALSE
from flask import Flask, Response, render_template, request, redirect, g, session, url_for, flash
from flask_mysqldb import MySQL
# import MySQLdb
# import MySQLdb.cursors
# import mysql.connector
import os
import database
# import bcrypt
import hashlib
import json
from datetime import datetime
from json import dumps
import employee
import slry_file
import attendence
from fpdf import FPDF
import pdfkit
# import addemployee

app = Flask(__name__)
app.secret_key = os.urandom(24)

db = MySQL(app)

config = pdfkit.configuration(wkhtmltopdf=b'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')	

@app.route('/login', methods = ['GET', 'POST'])
def index():
    print('sdsd')
    if request.method == 'POST':
        print(session)
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            hash_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
            print("password_user : ",hash_pass)
            info = database.get_row_single("SELECT * FROM employee WHERE user_name=%(user)s AND password=%(password)s ", {'user' : username, 'password' : hash_pass})
            dum_info = json.dumps(info)
            print("info : ",info)
            new_info = json.loads(dum_info)
            print("info : ",new_info)
            
            #exit
            try:
                # if info['user'] == username and info['password'] == password:
                if info != None:
                    # session['user'] = request.form['username']
                    # session['password'] = request.form['password']
                    session['auth'] = new_info
                    
                    return redirect(url_for('home'))
            except:
                    return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/home')
def home():
    # data = (database.get_row_single("SELECT image FROM employee WHERE user_name = %(user)s", {'user' : session['auth']['user_name']})) 
    print("g.user : ",g.user)
    if g.isLoggedIn:
        print("session home : ", session)
        print("home id : ", request.args.get('id'))
        # return employee.display(user=session['auth']['user_name'], role=session['auth']['role'])
        return render_template('home.html', user=session['auth']['user_name'], role=session['auth']['role'], image=session['auth']['image'])
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    g.isLoggedIn = False
    # print("history : ", request)
    if 'auth' in session:
        print("hello")
        print("seesion_in_auth",session['auth'])
        g.isLoggedIn = True
        g.user = session['auth']['user_name']
    # if session == {}:
    #     render_template('login.html')
    print(g.isLoggedIn)
    print('endpoint_kj', request.endpoint)
    if g.isLoggedIn == FALSE and request.endpoint != index:
        print("hi hi")
        return redirect(url_for('index'))
        # print("after return")

@app.route('/dropsession')
def dropsession():
    session.pop('auth', None)
    g.user = None
    g.isLoggedIn = False
    print("drop",session)
    # return render_template('login.html')
    return redirect(url_for('index'))

@app.after_request
def add_header(Response):
  Response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
  return Response

@app.route('/adduser', methods = ['GET', 'POST'])
def add():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return employee.adduser(image=session['auth']['image'], user=session['auth']['user_name'])
    return redirect(url_for('index'))    

@app.route('/deluser',methods=['GET', 'POST'])
def deluser_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return employee.deluser1(request.args.get('id'))
    return redirect(url_for('index'))

@app.route('/update_get', methods=['GET', 'POST'])
def update_get_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return employee.update_get(request.args.get('id'), image=session['auth']['image'], user=session['auth']['user_name'])
    return redirect(url_for('index'))
   

@app.route('/update_post', methods=['GET', 'POST'])
def update_post_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return employee.update_post(image=session['auth']['image'], user=session['auth']['user_name'])
    return redirect(url_for('index'))
    
@app.route('/salary_update_get', methods=['GET', 'POST'])
def salary_update_get_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return slry_file.salary_update_get(request.args.get('id'), image=session['auth']['image'], user=session['auth']['user_name'])
    return redirect(url_for('index'))

@app.route('/salary_view', methods=['GET', 'POST'])
def salary_view_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return slry_file.salary_view(request.args.get('id'), role=session['auth']['role'],  image=session['auth']['image'], user=session['auth']['user_name'])
    return redirect(url_for('index'))

@app.route('/salary_update_post', methods=['GET', 'POST'])
def salary_update_post_route():
    print("i am in update method post")
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return slry_file.salary_update_post(image=session['auth']['image'], user=session['auth']['user_name'])
    return redirect(url_for('index'))

@app.route('/salary', methods=['GET', 'POST'])
def salary_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return slry_file.salary(role=session['auth']['role'], image=session['auth']['image'], user=session['auth']['user_name'], emp_id=session['auth']['emp_id'])
    return redirect(url_for('index'))

@app.route('/salary_add', methods = ['GET', 'POST'])
def salary_add_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return slry_file.salary_add(role=session['auth']['role'], image=session['auth']['image'], user=session['auth']['user_name'])
    return redirect(url_for('index'))

@app.route('/salary_delete',methods=['GET', 'POST'])
def salary_delete_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return slry_file.salary_delete(request.args.get('id'))
    return redirect(url_for('index'))

@app.route('/download_report',methods=['GET', 'POST'])
def download_report_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return slry_file.download_report(emp_id=session['auth']['emp_id'])
    return redirect(url_for('index'))

@app.route('/att')
def att_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return attendence.att(role=session['auth']['role'], image=session['auth']['image'], user=session['auth']['user_name'], emp_id=session['auth']['emp_id'])
    return redirect(url_for('index'))

@app.route('/leave', methods = ['GET', 'POST'])
def leave_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return attendence.leave(role=session['auth']['role'], image=session['auth']['image'], user=session['auth']['user_name'], emp_id=session['auth']['emp_id'])
    return redirect(url_for('index'))

@app.route('/leave_request', methods=['GET', 'POST'])
def leave_request_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return attendence.leave_request(role=session['auth']['role'], image=session['auth']['image'], user=session['auth']['user_name'], emp_id=session['auth']['emp_id'])
    return redirect(url_for('index'))

@app.route('/leave_reject',methods=['GET', 'POST'])
def leave_reject_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return attendence.leave_reject(request.args.get('id'))
    return redirect(url_for('index'))

@app.route('/leave_accept',methods=['GET', 'POST'])
def leave_accept_route():
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        return attendence.leave_accept(request.args.get('id'))
    return redirect(url_for('index'))

@app.route('/employ')
def employ_route():
    print("g.user : ",g.user)
    if g.isLoggedIn:
        print("session role user : ",session['auth']['role'])
        if session['auth']['role'] == 1:
            return employee.employ(user=session['auth']['user_name'], role =session['auth']['user_name'])
        return redirect(url_for('home'))

    return redirect(url_for('index'))

@app.route('/display')
def display_route():
    print("g.user : ",g.user)
    if g.isLoggedIn:
        print(session)
        print("home id : ", request.args.get('id'))
        return employee.display(user=session['auth']['user_name'], role=session['auth']['role'])
        # return render_template('home.html', user=session['auth']['user_name'], role=session['auth']['role'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


