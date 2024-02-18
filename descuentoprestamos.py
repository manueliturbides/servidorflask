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


descuentoprestamos_api = Blueprint('descuentoprestamos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@descuentoprestamos_api.route("/api/consultadescuentoprestamos",methods=['POST','GET'])
def consultadescuentoprestamos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    print(row)
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select nocuota as Nocuota,date_format(fecha,'%d-%m-%Y') as Fecha,format(cuota,2) as Valor,format((interes-(vpagint+ifnull(descuento,0))),2) as Interespend,ifnull(descuento,0) as Descuento,Pagadodescuento,id from amort \
          where status <> 'P' and noprest = "+"'"+str(row['noprest'])+"'"
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          print(data)
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

@descuentoprestamos_api.route("/api/procesardescuento",methods=['POST','GET'])
def procesardescuento():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select nocuota as Nocuota,format((interes-vpagint),2) as descuento from amort \
          where status <> 'P' and noprest = "+"'"+str(row['noprest'])+"' and nocuota \
          between "+"'"+str(row['cuotadesde'])+"'"+" and "+"'"+str(row['cuotahasta'])+"'"
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


@descuentoprestamos_api.route("/api/guardardescuento",methods=['POST','GET'])
def guardardescuento():
    
    aerror = False
    salida = {}
    row = request.get_json()
    for x in row['dataresultados']:
        print(x)
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          for x in row['dataresultados']:
             sql = "update amort set descuento = "+"'"+str(float(x['Descuento']))+"'"+\
             " where noprest = "+"'"+str(row['noprest'])+"'"+" and nocuota = "+"'"+str(x['Nocuota'])+"'"    
             mycursor.execute(sql)
          
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
       res = make_response(jsonify({"data":"Datos correctamente procesados"}),200)
       return res; 

@descuentoprestamos_api.route("/api/limpiardescuento",methods=['POST','GET'])
def limpiardescuento():
    
    aerror = False
    salida = {}
    row = request.get_json()
    for x in row['dataresultados']:
        print(x)
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          for x in row['dataresultados']:
             sql = "update amort set descuento = "+"'"+str(float(x['Descuento']))+"'"+\
             " where noprest = "+"'"+str(row['noprest'])+"'"+" and nocuota = "+"'"+str(x['Nocuota'])+"'"    
             mycursor.execute(sql)
          
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
       res = make_response(jsonify({"data":"Datos correctamente procesados"}),200)
       return res; 
                        