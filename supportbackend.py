from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
import requests
import base64
import uuid
import json
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
import calendar
from procconectar import conectUserDatabase
from procconectar import conectUserDatabaseVendedor
from procconectar import conectServerDatabase
import time


supportbackend_api = Blueprint('supportbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.user
app.config['MYSQL_DATABASE'] = configuracionservidor.database
app.config['MYSQL_HOST'] = configuracionservidor.host
app.config['MYSQL_PASSWORD'] = configuracionservidor.password

PAYPAL_CLIENT_ID = "Ac7Xe72157GerO-EfF2GpQuklSR2aQLIU66y3debvQZQMXXAMaHu69VFMwgn_a6db4zd1ud8-lSjnjc1"
PAYPAL_CLIENT_SECRET = "EFpvcnm5Z6-9CDXBNJ9d9AwGqiYStObWrmD2JVLMy9JDP86rROjqhtbtWXCE4POdCOIgKu4Kp9jHfd_C"
PLAN_ID = "P-8LJ579675P663525BMWZFF5Y"

base = "https://api-m.sandbox.paypal.com"

CORS(app,origins="http://localhost:3000")
mysql = MySQL(app)

@supportbackend_api.route("/api/supportbackend_login",methods=['POST','GET'])
def supportackend_login():
    
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
          sql = "select * from soporte where email = "+"'"+row['email']+"' and password = "+"'"+row['password']+"'"
          mycursor.execute(sql)
          miuser = mycursor.fetchall()
          salida["miuser"] = miuser

          if mycursor.rowcount != 0:
             salida = "success"
             
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


@supportbackend_api.route("/api/supportbackend_soportedata",methods=['POST','GET'])
def supportbackend_soportedata():
    
    aerror = False
    error = {}
    row = request.get_json()
    salida = {}
    
    if aerror == False:
       try:
          date = datetime.today()
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          sql = "select * from transacciones where realizada='false'"
          mycursor.execute(sql)
          transacciones = mycursor.fetchall()

          sql = "select * from soporte"
          mycursor.execute(sql)
          missoporte = mycursor.fetchall()
          
          sql = "SELECT SUM(total) FROM transacciones where realizada='true'"
          mycursor.execute(sql)
          transferido = mycursor.fetchone()

          sql = "SELECT SUM(total) FROM transacciones where MONTH(fecha) = '"+str(date.month)+"' and realizada='true'"
          mycursor.execute(sql)
          transferidoestemes = mycursor.fetchone()

          sql = "SELECT SUM(total) FROM transacciones where realizada='false' "
          mycursor.execute(sql)
          pendiente = mycursor.fetchone()


          salida["transacciones"] = transacciones
          salida["users"] = missoporte

          salida["transferido"] = 0
          if transferido["SUM(total)"] != None:
            salida["transferido"] =  transferido["SUM(total)"]
          
          salida["transferidomes"] = 0
          if transferidoestemes != None:
            salida["transferidomes"] = transferidoestemes["SUM(total)"]

          salida["pendiente"] = 0
          if pendiente != None:
            salida["pendiente"] = pendiente["SUM(total)"]

          print(salida)  
          res = make_response(jsonify(salida),200)
          return res 
       
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 



@supportbackend_api.route("/api/supportbackend_setdone",methods=['POST','GET'])
def supportbackend_setdone():
    
    aerror = False
    error = {}
    row = request.get_json()
    salida = {}
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          print(row["id"])
          sql = "update transacciones set realizada='true' where id = %s"
          val = (row["id"],)
          mycursor.execute(sql,val)
          conectar.commit()

          res = make_response(jsonify(salida),200)
          return res 
       
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 


@supportbackend_api.route("/api/supportbackend_updateuser",methods=['POST','GET'])
def supportbackend_updateuser():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if "@" not in row["email"]:
       aerror = True
       aerror = "Email invalido"
   

    if len(row["password"]) < 5:
       aerror = True
       error = "Contraseña debe tener mas de 5 letras"

    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor()
          sql = "update soporte set email=%s,password=%s where email=%s"
          val = (row["email"],row["password"],row["actualemail"])
          mycursor.execute(sql,val)
          conectar.commit()


          res = make_response(jsonify({"email":row["email"],"password":row["password"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@supportbackend_api.route("/api/supportbackend_adduser",methods=['POST','GET'])
def supportbackend_adduser():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor()
          sql = "select * from users where email = "+"'"+row['email']+"'"
          mycursor.execute(sql)
          miuser = mycursor.fetchall()
 
          if len(miuser) == 0:     
            sql = "insert into soporte(email,password,permisos) values(%s,%s,%s)"
            val = (row["email"],row["password"],row["permissions"])
            mycursor.execute(sql,val)
            conectar.commit()

            res = make_response(jsonify({"email":row["email"],"password":row["password"]}),200)
            return res 
          else:
             aerror = True
             error = {"userExist":True}
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@supportbackend_api.route("/api/supportbackend_deleteuser",methods=['POST','GET'])
def supportbackend_deleteuser():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if "@" not in row["email"]:
       aerror = True
       aerror = "Email invalido"
   
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor()
          sql = "delete from soporte where email = "+"'"+row["email"]+"'"
          mycursor.execute(sql)
          conectar.commit()


          res = make_response(jsonify({"email":row["email"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

