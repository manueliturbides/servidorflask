from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 

listadochasisincautados_api = Blueprint('listadochasisincautados_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)

@listadochasisincautados_api.route("/api/listadochasisincautados",methods=['POST','GET'])
def listadochasisincautados():
    
    aerror = False
    salida = {}
    row = request.get_json()
   
    if aerror == False:
       if len(row['fechadesde']) == 0 or row['fechadesde'] == None or row['fechadesde'] == '':
          aerror = True
          error = "La fecha desde donde quiere ver la facturacion no puede estar en blanco"

    if aerror == False:
       if len(row['fechahasta']) == 0 or row['fechahasta'] == None or row['fechahasta'] == '':
          aerror = True
          error = "La fecha hasta donde quiere ver los eventos no puede estar en blanco"
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select noprest as id,date_format(prestamo.fecha,'%d-%m-%Y') as fecha,concat(prestamo.nombres,' ',prestamo.apellidos) as nombrecompleto,prestamo.chasis,\
             format(increg.valor,2) as financia,incautador from prestamo inner join increg on prestamo.noprest = increg.nuprest where prestamo.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' "
          else:
             sql = "select noprest as id,date_format(prestamo.fecha,'%d-%m-%Y') as fecha,concat(prestamo.nombres,' ',prestamo.apellidos) as nombrecompleto,prestamo.chasis,\
             format(increg.valor,2) as financia,incautador from prestamo inner join increg on prestamo.noprest = increg.nuprest where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
                 
          mycursor.execute(sql)
          mifacturacion = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             salida["facturacion"] = mifacturacion
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay incautos registrados en las fechas seleccionadas"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 


