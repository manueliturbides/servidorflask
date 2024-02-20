from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
import json
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
import calendar
from procconectar import conectUserDatabaseVendedor


vendedoresbackend_api = Blueprint('vendedoresbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword


CORS(app,origins="http://localhost:3001")
mysql = MySQL(app)

@vendedoresbackend_api.route("/api/vendedoresbackend_paypaldata",methods=['POST','GET'])
def vendedoresbackend_paypaldata():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if "@" not in row["emailPayPal"]:
       aerror = True
       aerror = "Email invalido"
   

    if aerror == False:
       try:


          connectionUser = conectUserDatabaseVendedor(row["id"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update user set paypal=%s where id=%s"
          val = (row["emailPayPal"],row["id"])
          mycursor.execute(sql,val)
          connectionUser.commit()

          res = make_response(jsonify({"email":row["emailPayPal"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@vendedoresbackend_api.route("/api/vendedoresbackend_retirar",methods=['POST','GET'])
def vendedoresbackend_retirar():    
    aerror = False
    error = {}
    row = request.get_json()
    
    if "@" not in row["emailPayPal"]:
       aerror = True
       aerror = "Email invalido"
   

    if aerror == False:
       try:


          connection = mysql.connection
          mycursor = connection.cursor(dictionary=True)
          sql = "insert into transacciones(fecha,paypal,id,total,realizada) values(%s,%s,%s,%s,%s)"
          date = datetime.today()
          val = (date,row["emailPayPal"],row["id"],row["total"],"false")          
          mycursor.execute(sql,val)
          connection.commit()

          connectionUser = conectUserDatabaseVendedor(row["id"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update facturas set retired=%s where MONTH(fecha) != '"+str(date.month)+"'"
          val = ("true",)
          mycursor.execute(sql,val)
          connectionUser.commit()


          res = make_response(jsonify({"email":row["emailPayPal"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@vendedoresbackend_api.route("/api/vendedoresbackend_updateuser",methods=['POST','GET'])
def vendedoresbackend_updateuser():    
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
          sql = "update vendedores set email=%s,password=%s where id=%s"
          val = (row["email"],row["password"],row["id"])
          mycursor.execute(sql,val)
          conectar.commit()

          connectionUser = conectUserDatabaseVendedor(row["id"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "update user set nombre=%s,email=%s,password=%s where id=%s"
          val = (row["nombre"],row["email"],row["password"],row["id"])
          mycursor.execute(sql,val)
          connectionUser.commit()

          res = make_response(jsonify({"nombre":row["nombre"],"email":row["email"],"password":row["password"]}),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@vendedoresbackend_api.route("/api/vendedoresbackend_vendedordata",methods=['POST','GET'])
def vendedoresbackend_vendedordata():
    
    aerror = False
    error = {}
    row = request.get_json()
    salida = {}
    
    if aerror == False:
       try:
          date = datetime.today()
          conectar = conectUserDatabaseVendedor(row["id"])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from clientes"
          mycursor.execute(sql)
          misclientes = mycursor.fetchall()

          sql = "select * from user"
          mycursor.execute(sql)
          miuser = mycursor.fetchall()
 
          sql = "SELECT SUM(numSuscrip) FROM facturas where MONTH(fecha) != '"+str(date.month)+"'  and retired='false'"
          mycursor.execute(sql)
          payment = mycursor.fetchall()
          
          sql = "SELECT numSuscrip FROM facturas WHERE MONTH(fecha) = '"+str(date.month)+"' AND YEAR(fecha) = '"+str(date.year)+"'"
          mycursor.execute(sql)
          monthpayment = mycursor.fetchone()
          
          connection = mysql.connection
          mycursor = connection.cursor(dictionary=True)
          sql = "select total from transacciones where id = '"+row["id"]+"'"
          mycursor.execute(sql)
          pendientetransac = mycursor.fetchone()


          salida["clientes"] = misclientes 
          salida["user"] = miuser
          salida["payment"] = 0
          if payment[0]["SUM(numSuscrip)"] != None:
            salida["payment"] =  int(payment[0]["SUM(numSuscrip)"]) * 5
          salida["monthpayment"] = 0
          if monthpayment == None:
            sql = "SELECT COUNT(*) FROM clientes"
            mycursor.execute(sql)
            numclient = mycursor.fetchall()[0]["COUNT(*)"]
            print(numclient)


            sql = "insert into facturas(fecha,numSuscrip,retired) values(%s,%s,%s)"
            date = datetime.today()
            val = (date,numclient,"false")          
            mycursor.execute(sql,val)
            conectar.commit()
          else:  
            salida["monthpayment"] = int(monthpayment["numSuscrip"]) * 5
          salida["transaccionpend"] = 0
          if pendientetransac != None:
            salida["transaccionpend"] = pendientetransac["total"]

          res = make_response(jsonify(salida),200)
          return res 
       
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 


@vendedoresbackend_api.route("/api/vendedoresbackend_validateemail",methods=['POST','GET'])
def vendedoresbackend_validateemail():
    
    aerror = False
    error = {}
    row = request.get_json()
    print(row)
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
          sql = "select * from vendedores where email = "+"'"+row['email']+"'"
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
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

 
@vendedoresbackend_api.route("/api/vendedoresbackend_registrar",methods=['POST','GET'])
def vendedoresbackend_registrar():
    
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
          connectionUser = conectUserDatabaseVendedor(row["id"])
          mycursor = connectionUser.cursor()
          sql = "insert into User(id,nombre,email,password,promcode) values(%s,%s,%s,%s,%s)"
          val = (row["id"],row["email"].split("@")[0],row["email"],row["password"],row["promcode"])
          print(val)
          mycursor.execute(sql,val)
          connectionUser.commit()

          sql = "insert into facturas(fecha,numSuscrip,retired) values(%s,%s,%s)"
          date = datetime.today()
          val = (date,0,"false")          
          mycursor.execute(sql,val)
          connectionUser.commit()

          conectar = mysql.connection
          mycursor = conectar.cursor()
          sql = "insert into Vendedores(id,email,password,promcode,fecha) values(%s,%s,%s,%s,%s)"
          val = (row["id"],row["email"],row["password"],row["promcode"],datetime.today())
          mycursor.execute(sql,val)
          conectar.commit()



          res = make_response(jsonify({"success":"success"}),200)
          return res 
              
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@vendedoresbackend_api.route("/api/vendedoresbackend_login",methods=['POST','GET'])
def vendedoresbackend_login():
    
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
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from vendedores where email = "+"'"+row['email']+"' and password = "+"'"+row['password']+"'"
          mycursor.execute(sql)
          miuser = mycursor.fetchall()

          if mycursor.rowcount != 0:
             
             res = make_response(jsonify(miuser),200)
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
