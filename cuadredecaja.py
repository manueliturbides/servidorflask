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

cuadredecaja_api = Blueprint('cuadredecaja_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@cuadredecaja_api.route("/api/cuadredecaja",methods=['POST','GET'])
def cuadredecaja():
    
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
          sql = "select pagos.norecibo as Nrecibo, pagos.noprest as Noprest,date_format(pagos.fecha,'%d-%m-%Y') as Fecha,format((pagos.vpagint+pagos.vpagcap),2) as Valor, format(pagos.vpagmora,2) as Mora, \
          format(pagos.descinte,2) as Descuento,format(pagos.mora,2) as Mora, format((pagos.vpagcap+pagos.vpagint+pagos.vpagmora),2) as Total,\
          pagos.norecibo as id, concat(prestamo.nombres,' ',prestamo.apellidos) as Nombres from pagos \
          inner join prestamo on prestamo.noprest = pagos.noprest \
          where pagos.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"

          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          if mycursor.rowcount == 0:
             error = True
             error = "No hay datos que recuperar"
              
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
      