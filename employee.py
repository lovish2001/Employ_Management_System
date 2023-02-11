from pickle import FALSE
import re
# from django.forms import ValidationError
from flask import Flask, Response, render_template, request, redirect, g, session, url_for
from flask_mysqldb import MySQL
# import MySQLdb
# import MySQLdb.cursors
# import mysql.connector
import os
import database
import login
# import bcrypt
import hashlib
import json
from datetime import datetime
from json import dumps
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = os.urandom(24)
cwd = os.getcwd()
app.config['IMAGE_UPLOADS'] = '\\static\\profiles\\'
path = cwd + app.config['IMAGE_UPLOADS']
db = MySQL(app)


def employ(user, role):
    headings = ("Emp_id", "User_name", "email", "name", "Adress", "Pan no.", "Designation", "Action")
    data = (database.get_row_multiple("SELECT emp_id, user_name, email, emp_name, emp_address, pan_no, role, designation FROM employee WHERE role = 2"))
    print("emp data : ",data)
    image = ((database.get_row_single("SELECT user_name, image FROM employee WHERE user_name = %(user)s", {'user' : user})))
    return render_template("emp.html", headings = headings, data = data, image=image, role=role)

def adduser(image, user):
    print("adduser request : ", request.method)
    if request.method ==  'POST':
        if "user" in request.form and "password" in request.form and "email" in request.form and "name" in request.form and "address" in request.form and "pan" in request.form and "designation" in request.form:
                print("in request of user")
            # try:
                username = request.form['user']
                password = request.form['password']
                email = request.form['email']
                name = request.form['name']
                adress = request.form['address']
                pan = request.form['pan']
                designation = request.form['designation']
                image=request.files['image']
                filename = secure_filename(image.filename)
                hash_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
                # print("filename : ", filename)
                # print("saved_image : ", saved_image)
                # print("image saved at : ",image_save_at)
                if username == "":
                    login.flash("user_name must be unique and not empty!!")
                    return render_template("adduser.html")

                if filename == "":
                    database.add_data("INSERT INTO employee(user_name, password, email, emp_name, emp_address, pan_no, designation , role) VALUES (%(user)s, %(password)s, %(email)s, %(name)s, %(adress)s, %(pan)s, %(designation)s, %(role)s)", { 'user' : username, 'password' : hash_pass, 'email' : email, 'name' : name, 'adress' : adress, 'pan': pan, 'designation' : designation, 'role' : 2})
                    return redirect(url_for('employ_route'))
                else:
                    image.save(os.path.join(path, filename))
                    saved_image = app.config['IMAGE_UPLOADS'] + filename
                    database.add_data("INSERT INTO employee(user_name, password, email, emp_name, emp_address, pan_no, designation , role, image) VALUES (%(user)s, %(password)s, %(email)s, %(name)s, %(adress)s, %(pan)s, %(designation)s, %(role)s, %(image)s)", { 'user' : username, 'password' : hash_pass, 'email' : email, 'name' : name, 'adress' : adress, 'pan': pan, 'designation' : designation, 'role' : 2, 'image' : saved_image})
                    return redirect(url_for('employ_route'))
            # except:
            #     login.flash("user_name must be unique and not empty!!")
            #     return render_template("adduser.html")
    return render_template("adduser.html", image = image, user = user)

def deluser1(id):
    database.del_data("delete from employee where emp_id = %(del)s", {'del' : id})
    return redirect(url_for('employ_route'))

def update_get(id, image, user):
    data = (database.get_row_single("SELECT emp_id, user_name, email, emp_name, emp_address, pan_no, designation, image FROM employee WHERE emp_id = %(id)s", {'id' : id})) 
    return render_template("update.html", data = data, image = image, user = user)

def update_post(image, user):
    print("request form : ",request.form)
    if request.method ==  'POST':
        print("request form : ",request.form)
        if "email" in request.form and "name" in request.form and "adress" in request.form and "pan" in request.form and "designation" in request.form:
            try:
                email = request.form['email']
                name = request.form['name']
                adress = request.form['adress']
                pan = request.form['pan']
                designation = request.form['designation']
                id = request.form['id']
                image=request.files['image']
                filename = secure_filename(image.filename)
                if filename == '':
                     database.add_data("UPDATE employee SET email = %(email)s, emp_name = %(name)s, emp_address = %(adress)s, pan_no = %(pan)s, designation = %(designation)s WHERE emp_id = %(id)s", {'email' : email, 'name' : name, 'adress' : adress, 'pan': pan, 'designation' : designation, 'id' : id})
                     return redirect(url_for('employ_route'))
                else:
                    image.save(os.path.join(path, filename))                
                    saved_image = app.config['IMAGE_UPLOADS'] + filename
                    database.add_data("UPDATE employee SET email = %(email)s, emp_name = %(name)s, emp_address = %(adress)s, pan_no = %(pan)s, designation = %(designation)s, image = %(image)s WHERE emp_id = %(id)s", {'email' : email, 'name' : name, 'adress' : adress, 'pan': pan, 'designation' : designation, 'image': saved_image, 'id' : id})
                    return redirect(url_for('employ_route'))
                # if username == "":
                #     login.flash("user_name must be unique and not empty!!")
                #     return render_template("update.html")
                # database.add_data("UPDATE employee SET email = %(email)s, emp_name = %(name)s, emp_address = %(adress)s, pan_no = %(pan)s, designation = %(designation)s, image = %(image)s WHERE emp_id = %(id)s", {'email' : email, 'name' : name, 'adress' : adress, 'pan': pan, 'designation' : designation, 'image': saved_image, 'id' : id})
                # return redirect(url_for('employ_route'))
            except:
                login.flash("user_name must be unique and not empty!!")
                return render_template("update.html")


    return render_template("update.html",image = image, user = user)

def display(user, role):
    data = (database.get_row_single("SELECT role, emp_id, user_name, email, emp_name, emp_address, pan_no, designation, image FROM employee WHERE user_name = %(user)s", {'user' : user})) 

    return render_template('display.html', data = data, user = user)



