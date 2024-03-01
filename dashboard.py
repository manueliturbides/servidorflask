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


dashboard_api = Blueprint('dashboard_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@dashboard_api.route("/api/dashboardmain",methods=['POST','GET'])
def dashboardmain():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       ###validar campos de entrada
        
       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select format(sum(deudatotal),2) as solicitudnueva  from solicit where month(fecha_crea) = month(now())"
          mycursor.execute(sql)
          solicitudnueva = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             valorsolicitudnueva = solicitudnueva[0]['solicitudnueva']
          else:
             valorsolicitudnueva = 0.0     

          sql = "select format(sum(cuota),2) as pagosdelmes from pagos where month(fecha) = month(now())"
          mycursor.execute(sql)
          pagosdelmes = mycursor.fetchall()
          if mycursor.rowcount != 0:
             valorpagosdelmes = pagosdelmes[0]['pagosdelmes']
          else:
             valorpagosdelmes = 0.0 
          
          sql = "select format(sum(deudatotal),2) as prestamodelmes from solicit where aprobado = 'S' and month(fecha_crea) = month(now())"
          mycursor.execute(sql)
          prestamodelmes = mycursor.fetchall()
          if mycursor.rowcount != 0:
             valorprestamodelmes = prestamodelmes[0]['prestamodelmes']
          else:
             valorprestamodelmes = 0.0 
          

          sql = "select format(sum(deudatotal),2) as aprobadosdelmes from solicit where aprobado = 'S' and month(fecha_crea) = month(now())  "
          mycursor.execute(sql)
          aprobadosdelmes = mycursor.fetchall()
          if mycursor.rowcount != 0:
             valoraprobadosdelmes = aprobadosdelmes[0]['aprobadosdelmes']
          else:
             valoraprobadosdelmes = 0.0 
          
          sql = "select sum(solicit.financiamiento) as monto,monthname(solicit.fecha_crea) as mes from solicit group by month(fecha_crea)"
          mycursor.execute(sql)
          grafico = mycursor.fetchall()
        
          datasol = []
          listasol = []
          for x in grafico:
              datasol.append(x['monto'])
              listasol.append(x['mes']) 
          
          sql = "select sum(solicit.deudatotal) as monto,monthname(solicit.fecha_crea) as mes from solicit where aprobado = 'S' group by month(fecha_crea) "
          mycursor.execute(sql)
          grafico = mycursor.fetchall()

          datapre = []
          listapre = []
          for x in grafico:
              datapre.append(x['monto'])
              listapre.append(x['mes']) 
          
          sql = "select sum(pagos.cuota) as monto,monthname(pagos.fecha) as mes from pagos group by month(fecha)"
          mycursor.execute(sql)
          grafico = mycursor.fetchall()

          datapag = []
          listapag = []
          for x in grafico:
              datapag.append(x['monto'])
              listapag.append(x['mes']) 
            

          data = {"solicituddelmes": valorsolicitudnueva,"pagosdelmes": valorpagosdelmes,"prestamodelmes": valorprestamodelmes,"aprobadosdelmes": valoraprobadosdelmes}          
          datasolicitud = {"datasol": datasol, "listasol": listasol}
          dataprestamos = {"datapre": datapre, "listapre": listapre}
          datapagos = {"datapag": datapag, "listapag": listapag}
          print(datasolicitud)
          
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data,"datasolicitud": datasolicitud, "dataprestamos":dataprestamos,"datapagos":datapagos}),200)
       #res = make_response(jsonify({"data":data,"datasolicitud": datasolicitud}),200)
       
       return res; 
