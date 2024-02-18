from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
import calendar
from procconectar import conectUserDatabase


loginbackend_api = Blueprint('loginbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.user
app.config['MYSQL_DATABASE'] = configuracionservidor.database
app.config['MYSQL_HOST'] = configuracionservidor.host
app.config['MYSQL_PASSWORD'] = configuracionservidor.password

mysql = MySQL(app)

CORS(app)

mysqluser = MySQL(app)


@loginbackend_api.route("/api/database",methods=['POST','GET'])
def database():
    connect = conectUserDatabase("manuel")

    return({"ok": "ok"})

@loginbackend_api.route("/api/configuredatabasegeneral",methods=['POST','GET'])
def registerbackend_configuredatabasegeneral():
    
    import mysql.connector

    aerror = False
    salida = {}
    
    if aerror == False:
       try:
          mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="00100267590")
          mycursor = mydb.cursor()
          mycursor.execute("create database if not exists generales")
      
          conectar = mysqluser.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "CREATE TABLE Users (id varchar(255),parent varchar(255),email varchar(255),password varchar(255));"
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

          sql = "insert into Company(nombre,direccion,telefono) values(%s,%s,%s)"
          val = ('','','')
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

@loginbackend_api.route("/api/loginbackend_login",methods=['POST','GET'])
def loginbackend_login():
    
    aerror = False
    salida = {}
    row = request.get_json()
    

    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from users where email = "+"'"+row['email']+"' and password = "+"'"+row['password']+"'"
          mycursor.execute(sql)
          miuser = mycursor.fetchall()

          if mycursor.rowcount != 0:
             salida["miuser"] = miuser
             
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "Usuario no encontrado. Revise usuario y clave"
       
       
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 