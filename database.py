from ast import dump
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import mysql.connector
import os
import json
from datetime import datetime
from json import dumps
# import database

# db = MySQL(app)

def connect():
  return mysql.connector.connect(
    host ="localhost",
    user ="admin",
    passwd ="admin",
    database = "emp_mng_system"
  )

def get_row_multiple(query):
    dataBase = connect()
    cursorObject = dataBase.cursor(dictionary = True)
    cursorObject.execute(query)
    myresult = cursorObject.fetchall()
    return myresult
    # for x in myresult:
    #     print(x)

def get_row_multiple2(query, variable1):
    dataBase = connect()
    cursorObject = dataBase.cursor(dictionary = True)
    cursorObject.execute(query, variable1)
    myresult = cursorObject.fetchall()
    return myresult
    # for x in myresult:
    #     print(x)


def get_row_single(query, variable1):
    # x=query
    print("variable1 : ", variable1)
    dataBase = connect()
    # cursorObject = dataBase.connection.cursor(MySQLdb.cursors.DictCursor)
    cursorObject = dataBase.cursor(dictionary = True)
    cursorObject.execute(query, variable1)
    myresult = cursorObject.fetchone()
    # print("my result : ",myresult)
    # dataBase.close()
    return myresult

def add_data(query, variable1):
    # x=query
    # print("variable1 : ", variable1)
    dataBase = connect()
    # cursorObject = dataBase.connection.cursor(MySQLdb.cursors.DictCursor)
    cursorObject = dataBase.cursor(dictionary = True)
    cursorObject.execute(query, variable1)
    dataBase.commit()
    # dataBase.close()

def up_data(query, variable1):
    # x=query
    # print("variable1 : ", variable1)
    dataBase = connect()
    # cursorObject = dataBase.connection.cursor(MySQLdb.cursors.DictCursor)
    cursorObject = dataBase.cursor()
    cursorObject.execute(query, variable1)
    dataBase.commit()
    # dataBase.close()

def del_data(query, variable1):
    # x=query
    # print("variable1 : ", variable1)
    dataBase = connect()
    # cursorObject = dataBase.connection.cursor(MySQLdb.cursors.DictCursor)
    cursorObject = dataBase.cursor(dictionary = True)
    cursorObject.execute(query, variable1)
    dataBase.commit()
    
def update_data(query, variable3):
    # x=query
    # print("variable1 : ", variable1)
    dataBase = connect()
    # cursorObject = dataBase.connection.cursor(MySQLdb.cursors.DictCursor)
    cursorObject = dataBase.cursor(dictionary = True)
    cursorObject.execute(query, variable3)
    dataBase.commit()


# dataBase.close()