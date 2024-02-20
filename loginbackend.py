from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import date
import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
import calendar
from procconectar import conectUserDatabase
import mysql.connector as connector


loginbackend_api = Blueprint('loginbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)

@loginbackend_api.route("/api/configuredatabasegeneral",methods=['POST','GET'])
def registerbackend_configuredatabasegeneral():
    
    aerror = False
    salida = {}
    
    
    if aerror == False:
       try:
          mydb = connector.connect(host="127.0.0.1",user="root",password="00100267590")
          mycursor = mydb.cursor()
          mycursor.execute("create database if not exists general")


          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "CREATE TABLE IF NOT EXISTS Users (id varchar(255),parent varchar(255),email varchar(255),password varchar(255));"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS Vendedores (id varchar(255),email varchar(255),password varchar(255),promcode varchar(255), fecha date);"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS Planes (name varchar(255),id varchar(255),product_id varchar(255));"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS soporte (email varchar(255) UNIQUE PRIMARY KEY,password varchar(255),permisos varchar(255));"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS transacciones(fecha date,paypal varchar(255), id varchar(255), total varchar(255),realizada varchar(255))"
          mycursor.execute(sql)
          
          

          conectar.close()
          res = make_response("Success",200)
          return res
       except Exception as e:
          print(e)
          aerror = True
       
    if aerror == True:
       res = make_response(jsonify({"Error": "error"}),400)
       return res; 

@loginbackend_api.route("/api/registerbackend_validateemail",methods=['POST','GET'])
def registerbackend_validateemail():
    
    aerror = False
    error = {}
    row = request.get_json()

    if "@" not in row["email"] or len(row["email"])<3:
       aerror = True
       aerror = "Email invalido"
   

    if len(row["password"]) < 5:
       aerror = True
       error = "Contraseña debe tener mas de 5 letras"

    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from users where email = "+"'"+row['email']+"'"
          mycursor.execute(sql)
          misusers = mycursor.fetchall()
 
          if len(misusers) == 0:     
             res = make_response(jsonify({"userExist":False}),200)
             return res 
          else:
             aerror = True
             error = {"userExist":True}
       
       
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

 
@loginbackend_api.route("/api/registerbackend_registrar",methods=['POST','GET'])
def registerbackend_registrar():
    
    aerror = False
    salida = {}
    row = request.get_json()

    if "@" not in row["email"] or len(row["email"])<3:
       aerror = True
       aerror = "Email invalido"
   

    if len(row["password"]) < 5:
       aerror = True
       error = "Contraseña debe tener mas de 5 letras"
    
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor()
          sql = "insert into Users(id,parent,email,password) values(%s,%s,%s,%s)"
          val = (row["id"],row["parent"],row["email"],row["password"])
          mycursor.execute(sql,val)
          conectar.commit()
          
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor()

          sql = "insert into Users(id,parent,nombre,apellido,email,password,permissions) values(%s,%s,%s,%s,%s,%s,%s)"
          val = (row["id"],row["parent"],"","",row["email"],row["password"],"administrator")
          mycursor.execute(sql,val)
          connectionUser.commit()

          sql = "insert into Company(nombre,direccion,telefono,pais) values(%s,%s,%s,%s)"
          val = ('','','','')
          mycursor.execute(sql,val)
          connectionUser.commit()

          sql = "insert into facturas(plan,suscriptionid,total,fecha) values(%s,%s,%s,%s)"
          date = datetime.datetime.today()
          val = ("demo",'',0,date)
          mycursor.execute(sql,val)
          connectionUser.commit()



          res = make_response(jsonify({"success":"success"}),200)
          return res 
              
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

def diff_month(d1, d2):
    return (d1 - d2).days

@loginbackend_api.route("/api/loginbackend_login",methods=['POST','GET'])
def loginbackend_login():
    
    aerror = False
    salida = {}
    row = request.get_json()
    daysdif = ""
    
    if "@" not in row["email"]:
       aerror = True
       aerror = "Email invalido"
   

    if len(row["password"]) < 5:
       aerror = True
       error = "Contraseña debe tener mas de 5 letras"
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from users where email = "+"'"+row['email']+"' and password = "+"'"+row['password']+"'"
          mycursor.execute(sql)
          miuser = mycursor.fetchall()
          salida["miuser"] = miuser

          if mycursor.rowcount != 0:
             connectionUser = conectUserDatabase(miuser[0]["parent"])
             mycursor = connectionUser.cursor(dictionary=True)
             sql = "select * from facturas order by id desc limit 1"
             mycursor.execute(sql)
             ultFactura = mycursor.fetchall()
             
             if ultFactura[0]["plan"] == "demo":
               end_date = ultFactura[0]["fecha"] + datetime.timedelta(days=15)
               daysdif = diff_month(end_date,datetime.date.today())     
               salida["diffday"] = daysdif
             else:
               salida["diffday"] = "notdemo"

             salida["plan"] = ultFactura[0]["plan"]

             
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "Usuario no encontrado. Revise usuario y clave"
       
       
          conectar.close()
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 