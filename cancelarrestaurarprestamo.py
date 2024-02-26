from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
from datetime import datetime,timedelta
from procconectar import conectUserDatabase


cancelarrestaurarprestamo_api = Blueprint('cancelarrestaurarprestamo_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@cancelarrestaurarprestamo_api.route("/api/consultarprestamos",methods=['POST','GET'])
def consultarprestamos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    print(row)
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select prestamo.noprest as Noprest,date_format(prestamo.fecha,'%d-%m-%Y') as Fecha,concat(prestamo.nombres,' ',prestamo.apellidos) as Nombres,\
          (solicit.deudatotal - (prestamo.vpagcap+prestamo.vpagint)) as Valor,prestamo.status as Status from prestamo \
          inner join solicit on prestamo.nosolic = solicit.id \
          where prestamo.noprest = "+"'"+str(row['noprest'])+"'"+" and prestamo.fecha between "+"'"+str(row['fechadesde'])+"' and "+" '"+str(row['fechahasta'])+"'"
          
          print(sql)
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          
          conectar.close() 
          print(data) 
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data}),200)
       return res; 


@cancelarrestaurarprestamo_api.route("/api/cancelarrestaurarprestamo",methods=['POST','GET'])
def consultarrestaurarprestamos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    print(row)
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          if row['status'] == "A":
             sql = "update prestamo set status = 'C' where noprest = "+"'"+str(row['noprest'])+"'"

          if row['status'] == "C":
             sql = "update prestamo set status = 'A' where noprest = "+"'"+str(row['noprest'])+"'"
          
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          conectar.commit()
          conectar.close() 
         
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data}),200)
       return res; 


@cancelarrestaurarprestamo_api.route("/api/recuperartodosprestamos",methods=['POST','GET'])
def recuperartodosprestamos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select concat(prestamo.noprest,'/',prestamo.nombres,' ',prestamo.apellidos,'/',solicit.cedula,'/',solicit.id) as label \
          from prestamo \
          inner join solicit on prestamo.nosolic = solicit.id"


          mycursor.execute(sql)
          data = mycursor.fetchall()
          conectar.close() 

    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data}),200)
       return res; 
