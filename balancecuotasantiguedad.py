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

balancecuotasantiguedad_api = Blueprint('balancecuotasantiguedad_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@balancecuotasantiguedad_api.route("/api/balancecuotasantiguedad",methods=['POST','GET'])
def balancecuotasantiguedad():
    
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
          sql = "select amort.noprest as Nprest, concat(solicit.nombres,' ',solicit.apellidos) as Nombres,format(sum((capital-vpagcap)),2) as Capital, \
          format(sum((amort.interes - amort.vpagint)),2) as Interes, count(amort.noprest) as Cuotas, amort.noprest as id from amort  \
          inner join solicit on amort.nosolic = solicit.id \
          where amort.fecha <"+" '"+str(row['fecha'])+"' and amort.status <> 'P'"+"group by amort.noprest"
          
        
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             datafinal = []
             for x in data:
                 if row['tipodeoperacion'] == '>':
                    if x['Cuotas'] > int(row['cuotas']):
                       datafinal.append(x)

                 if row['tipodeoperacion'] == '=':
                    if x['Cuotas'] == int(row['cuotas']):
                       datafinal.append(x)

             sql = ""
          else:
             aerror = True
             error = "No hay datos para recuperar"   


    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":datafinal}),200)
       return res; 
