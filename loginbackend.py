from countryinfo import CountryInfo
import requests
from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import date
import datetime
import json
from flask_mysql_connector import MySQL
import configuracionservidor 
import calendar
from procconectar import conectUserDatabase
import smtplib
from email.message import EmailMessage
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
          mydb = connector.connect(host="general.c78ou26kqg7e.us-east-1.rds.amazonaws.com",user="root",password="00100267590",port = 3306)
          mycursor = mydb.cursor()
          mycursor.execute("create database if not exists general")

          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "CREATE TABLE IF NOT EXISTS users (id varchar(255),parent varchar(255),email varchar(255),password varchar(255));"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS vendedores (id varchar(255),email varchar(255),password varchar(255),promcode varchar(255), fecha date);"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS Planes (name varchar(255),id varchar(255),product_id varchar(255));"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS soporte (email varchar(255) UNIQUE PRIMARY KEY,password varchar(255),permisos varchar(255));"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS transacciones(fecha date,paypal varchar(255), id varchar(255), total varchar(255),realizada varchar(255))"
          mycursor.execute(sql)

          sql = "CREATE TABLE IF NOT EXISTS Currencies(fecha date,Country varchar(255), valor varchar(255))"
          mycursor.execute(sql)


          res = make_response("Success",200)
          return res
       except Exception as e:
          print(e)
          aerror = True
       
    if aerror == True:
       res = make_response(jsonify({"Error": "error"}),400)
       return res; 

@loginbackend_api.route("/api/registerbackend_sendcode",methods=['POST','GET'])
def registerbackend_sendcode():
    
    row = request.get_json()
        
    email = row["email"]
    code = row["code"]
    print(code)

    msg = EmailMessage()
    msg['Subject'] = 'PrestaQuiK Contacto'
    msg['From'] = "support@prosecomsrl.com"
    msg['To'] = email
    msg.set_content('''
                    <!DOCTYPE html>
                      <html>
                        <body style="background-color: white; ">
                            <p>Gracias por registrarte en PrestaQuiK</p> 
                            <p>Su código de registro es: <strong>'''+str(code)+''''</strong> </p>
                            <br></br>
                            <p>Administración PrestaQuiK</p>
                    

                       </body>
                      </html>''', subtype='html')

    try:
      server = smtplib.SMTP_SSL('smtp.mail.us-east-1.awsapps.com', 465)
      server.ehlo()
      server.login('support@prosecomsrl.com', 'mr@00100267590')
      text = msg.as_string()
      server.sendmail("support@prosecomsrl.com", email, text)
      print('Email sent to %s' "email_recipient")
    except Exception as e:
      print(e)
      print("SMTP server connection error")

    return str(code)

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
             print(misusers)
             res = make_response(jsonify({"userExist":False}),200)
             return res 
          else:
             print(misusers)
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
          sql = "insert into users(id,parent,email,password) values(%s,%s,%s,%s)"
          val = (row["id"],row["parent"],row["email"],row["password"])
          mycursor.execute(sql,val)
          conectar.commit()
          
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor()

          sql = "insert into users(id,parent,nombre,apellido,email,password,permissions) values(%s,%s,%s,%s,%s,%s,%s)"
          val = (row["id"],row["parent"],"","",row["email"],row["password"],"administrator")
          mycursor.execute(sql,val)
          connectionUser.commit()

          sql = "insert into company(nombre,direccion,telefono,pais) values(%s,%s,%s,%s)"
          val = ('','','',row["country"])
          mycursor.execute(sql,val)
          connectionUser.commit()

          sql = "insert into facturas(plan,suscriptionid,total,fecha) values(%s,%s,%s,%s)"
          date = datetime.datetime.today()
          val = ("demo",'',0,date)
          mycursor.execute(sql,val)
          connectionUser.commit()

          print(json.loads(row["country"])["label"])   
          conectar = mysql.connection
          mycursor = conectar.cursor()
          currency = CountryInfo(json.loads(row["country"])["label"]).currencies()[0]
          sql = "select * from Currencies where country = "+"'"+currency+"'"
          mycursor.execute(sql)
          country = mycursor.fetchone()

          if country == None:
            url = "https://api.apilayer.com/fixer/latest?symbols="+currency+"&base=USD"
            payload = {}
            headers= {
              "apikey": "Xcn6D05klxkrYHVAZk9lalp6Nvnvwlvf"
            }
            response = requests.request("GET", url, headers=headers, data = payload)
            result = json.loads(response.text)
            
            sql = "insert into Currencies(fecha,Country,valor) values(%s,%s,%s)"
            date = datetime.datetime.today()
            val = (date,currency,str(result["rates"][currency]))
            mycursor.execute(sql,val)
            conectar.commit()

          res = make_response(jsonify({"success":currency}),200)
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
      
          if mycursor.rowcount != 0:
             connectionUser = conectUserDatabase(miuser[0]["parent"])
             mycursor = connectionUser.cursor(dictionary=True)       
             mycursor.execute(sql)
             miuser = mycursor.fetchall()
             print(sql)
             salida["miuser"] = miuser
             
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

             sql = "select * from company"
             mycursor.execute(sql)
             country = mycursor.fetchone()
             pais = json.loads(country["pais"])["label"]
             salida["country"] = pais
             salida["company"] = country["nombre"]

             conectar = mysql.connection
             mycursor = conectar.cursor(dictionary=True)
             
             currency = CountryInfo(pais).currencies()[0]
             sql = "select * from Currencies where Country = "+"'"+currency+"'"
             mycursor.execute(sql)
             country = mycursor.fetchone()
             salida["currency"] = country["valor"]
             

             if country != None:
               end_date = country["fecha"] + datetime.timedelta(days=15)
               daysdif = diff_month(end_date,datetime.date.today())     
               
               if daysdif <= 0:
                  url = "https://api.apilayer.com/fixer/latest?symbols="+currency+"&base=USD"
                  payload = {}
                  headers= {"apikey": "Xcn6D05klxkrYHVAZk9lalp6Nvnvwlvf"}
                  response = requests.request("GET", url, headers=headers, data = payload)
                  result = json.loads(response.text)
                  date = datetime.datetime.today()

                  sql = "update users set date=%s,valor=%s where Country=%s"
                  val = (date,str(result["rates"][currency]),currency)
                  mycursor.execute(sql,val)
                  conectar.commit()


            
             
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