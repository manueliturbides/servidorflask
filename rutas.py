from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
from procconectar import conectUserDatabase


rutas_api = Blueprint('rutas_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@rutas_api.route("/api/rutas",methods=['POST','GET'])
def rutas():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       ###validar campos de entrada

       aerror = False

       #row['user'] = ""

       if len(row['fecha']) == 0 and len(row['ciudad']) == 0:
          error 
          aerror = True


       if aerror == False:
          conectar = conectUserDatabase(row["parent"])
          mycursor = conectar.cursor(dictionary=True)
          
          if len(row['fecha']) != 0 and len(row['ciudad']) == 0:
       
             sql = "select concat(solicit.nombres,' ',solicit.apellidos) as nombres,solicit.direccion as direccion,\
             solicit.celular as celular,solicit.longitud as longitud, solicit.latitud as latitud, \
             sum(amort.cuota) as porcobrar,sum(vpagint+vpagcap) as cobrado,solicit.id as id \
             from amort \
             inner join solicit on amort.nosolic = solicit.id  \
             where amort.fecha = "+"'"+row['fecha']+"' group by noprest"
             
          if len(row['fecha']) == 0 and len(row['ciudad']) != 0:
             sql = "select concat(solicit.nombres,' ',solicit.apellidos) as nombres,solicit.direccion as direccion,\
             solicit.celular as celular,solicit.longitud as longitud,solicit.latitud as latitud, sum(amort.cuota) as porcobrar, \
             sum(vpagint+vpagcap) as cobrado solicit.id as id from amort \
             inner join solicit on amort.nosolic = solicit.id  \
             where solicit.provincia = "+"'"+row['ciudad']+"' group by noprest"
             
          if len(row['fecha']) != 0 and len(row['ciudad']) != 0:
             sql = "select concat(solicit.nombres,' ',solicit.apellidos) as nombres,solicit.direccion as direccion,\
             solicit.celular as celular,solicit.longitud as longitud, solicit.latitud as latitud \
             sum(amort.cuota) as porcobrar, sum(vpagint+vpagcap) as cobrado,solicit.id as id \
             from amort \
             inner join solicit on amort.nosolic = solicit.id  \
             where solicit.fecha = "+"'"+row['ciudad']+"' and solicit.provincia =  "+"'"+row['ciudad']+"' group by amort.noprest"
             
  
          mycursor.execute(sql)
          data = mycursor.fetchall()


          totalporcobrar = 0
          totalcobrado = 0
          c = 0
          for x in data:
              totalporcobrar = totalporcobrar + x['porcobrar']
              totalcobrado = totalcobrado + x['cobrado']

              if x['cobrado'] != 0:
                 c = c + 1
  
          conectar.commit()
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
       res = make_response(jsonify({'data': data,'porcobrar': '{:,.2f}'.format(totalporcobrar),'cobrado':'{:,.2f}'.format(totalcobrado),'cantidaddecobrados':'{:,.2f}'.format(c)}),200)
       return res; 
      
 