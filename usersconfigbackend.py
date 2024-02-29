from flask import Flask, send_file,url_for
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
import io
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
import calendar
from procconectar import conectUserDatabase


usersconfigbackend_api = Blueprint('usersconfigbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword


CORS(app)
mysql = MySQL(app)

@usersconfigbackend_api.route("/api/usersconfigbackend_updateuser",methods=['POST','GET'])
def usersconfigbackend_updateuser():    
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
          sql = "update users set email=%s,password=%s where id=%s"
          val = (row["email"],row["password"],row["id"])
          mycursor.execute(sql,val)
          conectar.commit()

          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update users set nombre=%s,apellido=%s,email=%s,password=%s,permissions=%s where id=%s"
          val = (row["nombre"],row["apellido"],row["email"],row["password"],row["permissions"],row["id"])
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
            sql = "insert into users(id,parent,email,password) values(%s,%s,%s,%s)"
            val = (row["id"],row["parent"],row["email"],row["password"])
            mycursor.execute(sql,val)
            conectar.commit()
          
            connectionUser = conectUserDatabase(row["parent"])
            mycursor = connectionUser.cursor()

            sql = "insert into users(id,parent,nombre,apellido,email,password,permissions) values(%s,%s,%s,%s,%s,%s,%s)"
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

@usersconfigbackend_api.route("/api/usersconfigbackend_deleteuser",methods=['POST','GET'])
def usersconfigbackend_deleteuser():    
    aerror = False
    error = {}
    row = request.get_json()
    
   
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor()
          sql = "delete from users where id = "+"'"+row["id"]+"'"
          mycursor.execute(sql)
          conectar.commit()

          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "delete from users where id = "+"'"+row["id"]+"'"
          mycursor.execute(sql)
          connectionUser.commit()



          res = make_response(jsonify({"id":row["id"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@usersconfigbackend_api.route("/api/usersconfigbackend_updatecompanylogo",methods=['POST','GET'])
def usersconfigbackend_updatecompanylogo():    
    aerror = False
    error = {}
    imagefile = request.files['image']
    bin_file = imagefile.read()
    
    if aerror == False:
       try:
          connectionUser = conectUserDatabase(request.form["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update company set logo=%s"
          val = (bin_file,)
          mycursor.execute(sql,val)
          connectionUser.commit()
          url = url_for("usersconfigbackend_api.logo", _id=request.form["parent"])
          print(url)

          res = make_response(jsonify({"succes":"sucess"}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@usersconfigbackend_api.route('/logo/<_id>')
def logo(_id):
   connectionUser = conectUserDatabase(_id)
   mycursor = connectionUser.cursor()
   
   sqlCompany = "select logo from company"
   mycursor.execute(sqlCompany)
   miComp = mycursor.fetchall()
   print(miComp[0][0])
 
   response =  send_file(io.BytesIO(miComp[0][0]),mimetype="image/*")

   return response


@usersconfigbackend_api.route("/api/usersconfigbackend_updatecompany",methods=['POST','GET'])
def usersconfigbackend_updatecompany():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if aerror == False:
       try:
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update company set nombre=%s,direccion=%s,telefono=%s,pais=%s"
          val = (row["nombre"],row["direccion"],row["telefono"],row["pais"])
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
         
          sqlCompany = "select nombre,direccion,telefono,pais from company"
          mycursor.execute(sqlCompany)
          miComp = mycursor.fetchall()

          sqlAllUsers = "select * from users"
          mycursor.execute(sqlAllUsers)
          misUsers = mycursor.fetchall()

          sql = "select sum(deudatotal) as totalvalorprestamo,count(id) as cantidaddeprestamo from solicit where aprobado = 'S' group by aprobado"
          mycursor.execute(sql)
          data = mycursor.fetchall()


          if len(miuser) != 0:
             
             salida["user"] = miuser
             salida["usersList"] = misUsers
             salida["company"] = miComp
             salida["generaldata"] = data

             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "Usuario no encontrado. Revise usuario y clave"
       
       
       except Exception as e:
          print(e)
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

    if "@" not in row["email"]:
       aerror = True
       aerror = "Email invalido"
   

    if len(row["password"]) < 5:
       aerror = True
       error = "Contraseña debe tener mas de 5 letras"


    
    if aerror == False:
       try:
          conectar = conectUserDatabase(row["parent"])
          mycursor = conectar.cursor()
          sql = "insert into users(id,parent,email,password) values(%s,%s,%s,%s)"
          val = (row["id"],row["parent"],row["email"],row["password"])
          mycursor.execute(sql,val)
          conectar.commit()
          
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor()
          sql = "CREATE TABLE IF NOT EXISTS users (id varchar(255) NOT NULL PRIMARY KEY,parent varchar(255),nombre varchar(255),apellido varchar(255),email varchar(255),password varchar(255),permissions varchar(255));"
          mycursor.execute(sql)

          sql = "insert into users(id,parent,nombre,apellido,email,password,permissions) values(%s,%s,%s,%s,%s,%s,%s)"
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

