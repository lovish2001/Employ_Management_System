from pickle import FALSE
import re
from turtle import color
from urllib import response
from click import style
# from django.forms import ValidationError
from flask import Flask, Response, render_template, request, redirect, g, session, url_for, make_response
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
from fpdf import FPDF
import pdfkit


config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
print("confid : ",config)

def salary(user,image, role, emp_id):
    if role == 1:
        headings = ("User_name", "bank", "ifsc", "pincode", "account", "phone", "date", "salary", "Action")
        data = (database.get_row_multiple("SELECT employee.emp_id, employee.role, employee.user_name, emp_salary.salary_id, emp_salary.bank, emp_salary.ifsc, emp_salary.pincode, emp_salary.account, emp_salary.phone, emp_salary.date, emp_salary.salary FROM emp_salary INNER JOIN employee ON employee.emp_id=emp_salary.emp_id order by date DESC;"))
    else:
        headings = ("User_name", "bank", "ifsc", "pincode", "account", "phone", "date", "salary", "Action")
        data = (database.get_row_multiple2("SELECT user_name, emp_salary.emp_id, bank, ifsc, pincode, salary_id, account, phone, date, salary FROM emp_salary INNER JOIN employee ON employee.emp_id=emp_salary.emp_id  WHERE employee.emp_id=%(id)s order by date DESC", {'id' : emp_id}))
        print("emp data : ",data)
        
    # image = ((database.get_row_single("SELECT user_name, image FROM employee WHERE user_name = %(user)s", {'user' : user})))

    return render_template("salary_list.html", headings = headings, data = data, role=role, image=image, user = user)

def salary_add(role, image, user):
    data = (database.get_row_multiple("SELECT emp_id, user_name FROM employee WHERE role = 2"))
    # print("request salary ", request.method)
    if request.method ==  'POST':
        if "id" in request.form and "bank" in request.form and "ifsc" in request.form and "account" in request.form and "phone" in request.form and "zip" in request.form and "salary" in request.form:
            emp_id = request.form['id']
            bank = request.form['bank']
            ifsc = request.form['ifsc']
            account = request.form['account']
            phone = request.form['phone']
            zip = request.form['zip']
            date = request.form['date']
            salary = request.form['salary']
            database.add_data("INSERT INTO emp_salary(emp_id, bank, pincode, ifsc, account, phone, date, salary) VALUES (%(id)s, %(bank)s, %(pincode)s, %(ifsc)s, %(account)s, %(phone)s, %(date)s, %(salary)s)", {'id' : emp_id, 'bank' : bank, 'pincode' : zip, 'ifsc' : ifsc, 'account' : account, 'phone': phone, 'date' : date, 'salary' : salary})
            return redirect(url_for('salary_route'))
    return render_template('salary.html', role=role, image=image, user=user, data = data)

def salary_delete(id):
    database.del_data("delete from emp_salary where salary_id = %(del)s", {'del' : id})
    return redirect(url_for('salary_route'))

def salary_update_get(id, image, user):
    data = (database.get_row_single("SELECT salary_id, bank, pincode, ifsc, account, phone, date, salary FROM emp_salary WHERE salary_id = %(id)s", {'id' : id})) 
    return render_template("salary_update.html", data = data, image = image, user = user)

def salary_update_post(image, user):
    # data = (database.get_row_single("SELECT bank, pincode, ifsc, account, phone, date, salary FROM emp_salary WHERE emp_id = %(id)s", {'id' : id})) 
    print("request update form : ",request.form)
    if request.method ==  'POST':
        print("request form : ",request.form)
        if "bank" in request.form and "ifsc" in request.form and "account" in request.form and "phone" in request.form and "zip" in request.form and "salary" in request.form:
            bank = request.form['bank']
            ifsc = request.form['ifsc']
            account = request.form['account']
            phone = request.form['phone']
            zip = request.form['zip']
            date = request.form['date']
            salary = request.form['salary']
            id = request.form['id']
            # database.add_data("INSERT INTO emp_salary(bank, pincode, ifsc, account, phone, date, salary) VALUES (%(bank)s, %(pincode)s, %(ifsc)s, %(account)s, %(phone)s, %(date)s, %(salary)s)", {'bank' : bank, 'pincode' : zip, 'ifsc' : ifsc, 'account' : account, 'phone': phone, 'date' : date, 'salary' : salary})
            updat_query = database.up_data("UPDATE emp_salary SET bank = %(bank)s, ifsc = %(ifsc)s, account = %(account)s, phone = %(phone)s, pincode = %(pincode)s, date = %(date)s, salary = %(salary)s WHERE salary_id = %(id)s", {'bank' : bank, 'pincode' : zip, 'ifsc' : ifsc, 'account' : account, 'phone': phone, 'date' : date, 'salary' : salary, 'id' : id})
            print("update query : ",updat_query)
            return redirect(url_for('salary_route'))
        # if "email" in request.form and "name" in request.form and "adress" in request.form and "pan" in request.form and "designation" in request.form:
        #     email = request.form['email']
        #     name = request.form['name']
        #     adress = request.form['adress']
        #     pan = request.form['pan']
        #     designation = request.form['designation']
        #     id = request.form['id']
        #     database.add_data("UPDATE employee SET email = %(email)s, emp_name = %(name)s, emp_address = %(adress)s, pan_no = %(pan)s, designation = %(designation)s WHERE emp_id = %(id)s", {'email' : email, 'name' : name, 'adress' : adress, 'pan': pan, 'designation' : designation, 'id' : id})
        #     return redirect(url_for('employ_route'))
    return render_template("salary_update.html",image = image, user = user)

def salary_view(id, role, image, user):
    data = (database.get_row_single("SELECT salary_id, bank, pincode, ifsc, account, phone, date, salary FROM emp_salary WHERE salary_id = %(id)s", {'id' : id})) 
    print("request update form : ",request.form)
    if request.method ==  'POST':
        print("request form : ",request.form)
        if "bank" in request.form and "ifsc" in request.form and "account" in request.form and "phone" in request.form and "zip" in request.form and "salary" in request.form:
            bank = request.form['bank']
            ifsc = request.form['ifsc']
            account = request.form['account']
            phone = request.form['phone']
            zip = request.form['zip']
            date = request.form['date']
            salary = request.form['salary']
            id = request.form['id']
            # database.add_data("INSERT INTO emp_salary(bank, pincode, ifsc, account, phone, date, salary) VALUES (%(bank)s, %(pincode)s, %(ifsc)s, %(account)s, %(phone)s, %(date)s, %(salary)s)", {'bank' : bank, 'pincode' : zip, 'ifsc' : ifsc, 'account' : account, 'phone': phone, 'date' : date, 'salary' : salary})
            updat_query = database.up_data("UPDATE emp_salary SET bank = %(bank)s, ifsc = %(ifsc)s, account = %(account)s, phone = %(phone)s, pincode = %(pincode)s, date = %(date)s, salary = %(salary)s WHERE salary_id = %(id)s", {'bank' : bank, 'pincode' : zip, 'ifsc' : ifsc, 'account' : account, 'phone': phone, 'date' : date, 'salary' : salary, 'id' : id})
            print("update query : ",updat_query)
            return redirect(url_for('salary_route'))
    return render_template("salary_view.html",image = image, role = role, user = user, data = data)

def download_report(emp_id):
        headings = ("bank", "ifsc", "pincode", "account", "phone", "date", "salary")
        data = (database.get_row_multiple2("SELECT user_name, emp_salary.emp_id, bank, ifsc, pincode, account, phone, date, salary FROM emp_salary INNER JOIN employee ON employee.emp_id=emp_salary.emp_id  WHERE employee.emp_id=%(id)s order by date", {'id' : emp_id}))
        print("emp data : ",data)
        pdf = FPDF()
        pdf.add_page()
        color = pdf.set_fill_color(1, 255, 255)
        pdf.set_font('Times', 'B', 14.0)
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.cell(page_width, 0.0, 'Salary Data', align='C')
        pdf.ln(10)
        pdf.set_font('courier', '', 12)
        col_width = page_width/7
        pdf.ln(1)
        th = pdf.font_size
        
        # for header in headings:
        
        pdf.cell(col_width, th, 'Bank', border=1)
        pdf.cell(col_width + 3, th, 'IFSC No.', border=1)
        pdf.cell(col_width - 7, th, 'Pincode', border=1)
        pdf.cell(col_width + 10, th, 'Account N0.', border=1)
        pdf.cell(col_width, th, 'Phone', border=1)
        pdf.cell(col_width, th, 'Date', border=1)
        pdf.cell(col_width - 5, th, 'Salary', border=1)
        pdf.ln(th)


        for row in data:
            pdf.cell(col_width, th, row['bank'], border=1)
            pdf.cell(col_width + 3, th, str(row['ifsc']), border=1)
            pdf.cell(col_width - 7, th, str(row['pincode']), border=1)
            pdf.cell(col_width + 10, th, str(row['account']), border=1)
            pdf.cell(col_width, th, str(row['phone']), border=1)
            pdf.cell(col_width, th, str(row['date']), border=1)
            pdf.cell(col_width - 5, th, str(row['salary']), border=1)
            pdf.ln(th)
        
        pdf.ln(10)
        pdf.set_font('Times', '', 10.0)
        pdf.cell(page_width, 0.0, '-end of report-', align='C')
        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=download_report_route.pdf'})

# def download_report(emp_id):
#     if request.method == 'POST':
#         headings = ("User_name", "bank", "ifsc", "pincode", "account", "phone", "date", "salary")
#         data = (database.get_row_multiple2("SELECT user_name, emp_salary.emp_id, bank, ifsc, pincode, salary_id, account, phone, date, salary FROM emp_salary INNER JOIN employee ON employee.emp_id=emp_salary.emp_id  WHERE employee.emp_id=%(id)s order by date", {'id' : emp_id}))
#         print("emp data : ",data)


#         render =  render_template("pdf.html", headings = headings, data = data)
#         pdf = pdfkit.from_string(render, False)
#         response = make_response(pdf)
#         response.headers['content-Type'] = 'application/pdf'
#         response.headers['content-Disposition'] = 'inline filename=download_report_route.pdf'
#         return response
#     return redirect(url_for('salary_route'))