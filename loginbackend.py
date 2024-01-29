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


loginbackend_api = Blueprint('loginbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.user
app.config['MYSQL_DATABASE'] = configuracionservidor.database
app.config['MYSQL_HOST'] = configuracionservidor.host
app.config['MYSQL_PASSWORD'] = configuracionservidor.password

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)

@loginbackend_api.route("/api/loginbackend_buscardatosiniciales",methods=['POST','GET'])
def loginbackend_buscardatosiniciales():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    if aerror == False:
       if len(row['usuario']) == 0 or row['usuario'] == None or row['usuario'] == '':
          aerror = True
          error = "El campo del usuario no puede estar en blanco"

    if aerror == False:
       if len(row['password']) == 0 or row['password'] == None or row['password'] == '':
          aerror = True
          error = "El campo clave no puede estar en blanco"
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from usuarios where usuario = "+"'"+row['usuario']+"' and clave = "+"'"+row['password']+"'"
          mycursor.execute(sql)
          misusers = mycursor.fetchall()

          if mycursor.rowcount != 0:
             mycursor = conectar.cursor(dictionary=True)
             sql = "select ncomp from varinicial"
             mycursor.execute(sql)
             micomp = mycursor.fetchall()
             
                
             salida['nombrenegocio'] = micomp
             salida["usuarios"] = misusers
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


