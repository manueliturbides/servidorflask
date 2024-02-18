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

hitorialdepagos_api = Blueprint('historialdepagos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@hitorialdepagos_api.route("/api/historialdepagos",methods=['POST','GET'])
def historialdepagos():
    
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
          sql = "select distinct format(solicit.deudatotal,2) as Deudatotal, concat(solicit.nombres,' ',solicit.apellidos) as Nombres,prestamo.noprest as Nprest, \
          format(prestamo.vpagcap,2) as Capitalpagado, format(prestamo.vpagint,2) as Interespagado, format((solicit.deudatotal - (prestamo.vpagint+prestamo.vpagcap)),2) as Balance, \
          prestamo.status as Status,prestamo.noprest as id \
          from prestamo \
          inner join solicit on solicit.cedula = prestamo.cedula and solicit.id = prestamo.nosolic where prestamo.cedula = "+"'"+row['cedula']+"'"
          
          #sql = "select prestamo.noprest as Nprest, \
          #prestamo.vpagcap as Capitalpagado, prestamo.vpagint as Interespagado, ((prestamo.vpagint+prestamo.vpagcap)) as Balance, \
          #prestamo.status as Status,prestamo.noprest as id \
          #from prestamo \
          #where prestamo.cedula = "+"'"+row['cedula']+"'"
        
        
          print(sql)
        
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
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
      