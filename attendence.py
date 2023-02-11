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

def att(role, image, user, emp_id):
    data = (database.get_row_multiple2("SELECT from_date, to_date FROM attendence where attendence.emp_id=%(id)s and status = 1", {'id' : emp_id}))
    print("attendence data : ",data)
    print("data length : ",len(data))
    data_dict = {}
    for i in range(len(data)):
        split_date = data[i]['from_date'].split('-')
        split_date2 = data[i]['to_date'].split('-')
        if(data_dict.get(split_date[0])):
            if(not data_dict[split_date[0]].get(split_date[1])):
                data_dict[split_date[0]][split_date[1]] =[]
        else:
            data_dict[split_date[0]] ={}
            data_dict[split_date[0]][split_date[1]] =[]
        split_date[2] = int(split_date[2])
        split_date2[2] = int(split_date2[2])
        while(split_date[2] <= split_date2[2]):
            data_dict[split_date[0]][split_date[1]].append(split_date[2])
            split_date[2] += 1
    # print("attendence  data : ", data)
    print("data_dict : ",data_dict)
    return render_template('att.html', role=role, image=image, user = user, data = data_dict)

def leave(role, image, user, emp_id):
    data = (database.get_row_multiple("SELECT emp_id, user_name FROM employee WHERE role = 2"))
    print("leave request method : ", request.method)
    if request.method ==  'POST':
        print("hi i am in leave post method")
        if "type" in request.form and "from_date" in request.form and "to_date" in request.form and "half" in request.form and "duration" in request.form and "applied_on" in request.form and "purpose" in request.form:
            print("i am in leave request conditon")
            # emp_id = request.form['id']
            type = request.form['type']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            half = request.form['half']
            duration = request.form['duration']
            applied_on = request.form['applied_on']
            purpose = request.form['purpose']
            database.add_data("INSERT INTO attendence(emp_id, leave_type, from_date, to_date, applied_on, halfday, duration, status, purpose) VALUES (%(id)s, %(type)s, %(from_date)s, %(to_date)s, %(applied_on)s, %(halfday)s, %(duration)s, %(status)s, %(purpose)s)", {'id' : emp_id, 'type' : type, 'from_date' : from_date, 'to_date' : to_date, 'applied_on' : applied_on, 'halfday': half, 'duration' : duration, 'status' : 0, 'purpose' : purpose})
            return redirect(url_for('att_route'))
    return render_template("leave.html", data = data, image = image, user = user, role = role, emp_id=emp_id)

def leave_request(role, image, user, emp_id):
    if role == 1:
        headings = ("User_name", "leave Type", "From Date", "To Date", "Applied On", "Halfday", "Duration", "status", "purpose", "Action")
        data = (database.get_row_multiple("SELECT employee.emp_id, employee.role, employee.user_name, attendence.leave_id, attendence.leave_type, attendence.from_date, attendence.to_date, attendence.applied_on, attendence.halfday, attendence.duration, attendence.status, attendence.purpose FROM attendence INNER JOIN employee ON employee.emp_id=attendence.emp_id;"))
    else:
        headings = ("User_name", "leave Type", "From Date", "To Date", "Applied On", "Halfday", "Duration", "purpose", "status")
        data = (database.get_row_multiple2("SELECT employee.role, employee.user_name, attendence.leave_id, attendence.leave_type, attendence.from_date, attendence.to_date, attendence.applied_on, attendence.halfday, attendence.duration, attendence.status, attendence.purpose FROM attendence INNER JOIN employee ON attendence.emp_id = employee.emp_id where attendence.emp_id=%(id)s;", {'id' : emp_id}))
    return render_template("leave_request.html",headings=headings, data = data, image = image, user = user, role = role, emp_id=emp_id)


def leave_reject(id):
    database.add_data("UPDATE attendence SET  status = %(status)s WHERE leave_id = %(id)s", {'status' : 2, 'id' : id})
    return redirect(url_for('att_route'))

def leave_accept(id):
    database.add_data("UPDATE attendence SET  status = %(status)s WHERE leave_id = %(id)s", {'status' : 1, 'id' : id})
    return redirect(url_for('att_route'))



