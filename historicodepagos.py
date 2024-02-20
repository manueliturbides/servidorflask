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

historicodepagos_api = Blueprint('historicodepagos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@historicodepagos_api.route("/api/historicodepagos",methods=['POST','GET'])
def historicodepagos():
    
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
          sql = "select norecibo as Nrecibo, noprest as Nprest,date_format(fecha,'%d-%m-%Y') as Fecha,format(sum((vpagint+vpagcap)),2) as Cuota, format(sum(vpagmora),2) as Mora, \
          format(sum(descinte),2) as Descuento,norecibo as id from pagos where cedula = "+"'"+row['cedula']+"' and noprest = "+"'"+row['noprest']+"'"+\
          " group by norecibo"

          print(sql)
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
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
      