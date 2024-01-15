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


usersconfigbackend_api = Blueprint('usersconfigbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.user
app.config['MYSQL_DATABASE'] = configuracionservidor.database
app.config['MYSQL_HOST'] = configuracionservidor.host
app.config['MYSQL_PASSWORD'] = configuracionservidor.password


CORS(app)
mysql = MySQL(app)

@usersconfigbackend_api.route("/api/usersconfigbackend_updateuser",methods=['POST','GET'])
def usersconfigbackend_updateuser():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if aerror == False:
       try:
          print(row["id"]+" skksk")
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update users set nombre=%s,apellido=%s,email=%s,password=%s where id=%s"
          val = (row["nombre"],row["apellido"],row["email"],row["password"],row["id"])
          mycursor.execute(sql,val)
          connectionUser.commit()

          res = make_response(jsonify({"nombre":row["nombre"],"apellido":row["apellido"],"email":row["email"],"password":row["password"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@usersconfigbackend_api.route("/api/usersconfigbackend_adduser",methods=['POST','GET'])
def usersconfigbackend_adduser():    
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
            sql = "insert into Users(id,parent,email,password) values(%s,%s,%s,%s)"
            val = (row["id"],row["parent"],row["email"],row["password"])
            mycursor.execute(sql,val)
            conectar.commit()
          
            connectionUser = conectUserDatabase(row["parent"])
            mycursor = connectionUser.cursor()

            sql = "insert into Users(id,parent,nombre,apellido,email,password,permissions) values(%s,%s,%s,%s,%s,%s,%s)"
            val = (row["id"],row["parent"],row["nombre"],row["apellido"],row["email"],row["password"],row["permissions"])
            mycursor.execute(sql,val)
            connectionUser.commit()

            res = make_response(jsonify({"nombre":row["nombre"],"apellido":row["apellido"],"email":row["email"],"password":row["password"]}),200)
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

@usersconfigbackend_api.route("/api/usersconfigbackend_updatecompany",methods=['POST','GET'])
def usersconfigbackend_updatecompany():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if aerror == False:
       try:
          print(row["id"]+" skksk")
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update company set nombre=%s,direccion=%s,telefono=%s"
          val = (row["nombre"],row["direccion"],row["telefono"])
          mycursor.execute(sql,val)
          connectionUser.commit()

          res = make_response(jsonify({"nombre":row["nombre"],"telefono":row["telefono"],"direccion":row["direccion"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 


@usersconfigbackend_api.route("/api/usersconfigbackend_userdata",methods=['POST','GET'])
def usersconfigbackend_userdata():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    
    if aerror == False:
       try:

          conectar = conectUserDatabase(row["parent"])
          mycursor = conectar.cursor(dictionary=True)
          sqlUser = "select * from users where id = "+"'"+row["id"]+"'"
          mycursor.execute(sqlUser)
          miuser = mycursor.fetchall()
         
          sqlCompany = "select * from company"
          mycursor.execute(sqlCompany)
          miComp = mycursor.fetchall()

          
          if len(miuser) != 0:
             
             salida["user"] = miuser
             salida["company"] = miComp

             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "Usuario no encontrado. Revise usuario y clave"
       
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 


@usersconfigbackend_api.route("/api/usersconfigbackend_newuser",methods=['POST','GET'])
def usersconfigbackend_newuser():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    
    if aerror == False:
       try:
          conectar = conectUserDatabase(row["parent"])
          mycursor = conectar.cursor()
          sql = "insert into Users(id,parent,email,password) values(%s,%s,%s,%s)"
          val = (row["id"],row["parent"],row["email"],row["password"])
          mycursor.execute(sql,val)
          conectar.commit()
          
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor()
          sql = "CREATE TABLE IF NOT EXISTS Users (id varchar(255) NOT NULL PRIMARY KEY,parent varchar(255),nombre varchar(255),apellido varchar(255),email varchar(255),password varchar(255),permissions varchar(255));"
          mycursor.execute(sql)

          sql = "insert into Users(id,parent,nombre,apellido,email,password,permissions) values(%s,%s,%s,%s,%s,%s,%s)"
          val = (row["id"],row["parent"],"","",row["email"],row["password"],"administrator")
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
