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


consultarpagos_api = Blueprint('consultarpagos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@consultarpagos_api.route("/api/consultarpagos",methods=['POST','GET'])
def consultarpagos():
    
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
          sql = "select pagosres.noprest as Noprest, pagosres.norecibo as Norecibo,date_format(pagosres.fecha,'%d-%m-%Y') as Fecha,\
          concat(solicit.nombres,' ',solicit.apellidos) as Nombres,format((pagosres.vpagint+pagosres.vpagcap+vpagmora),2) as Cuota, format(pagosres.vpagmora,2) as Mora,\
          pagosres.norecibo as id from pagosres \
          inner join solicit on pagosres.nosolic = solicit.id \
          where pagosres.fecha between "+"'"+str(row['fechadesde'])+"' and"+"'"+str(row['fechahasta'])+"' and pagosres.cuota <> 0 order by fecha desc"
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          if mycursor.rowcount == 0:
             aerror = True
             error = "No hay datos para recuperar"

          if aerror == False:
            sql = "select sum(pagosres.cuota) as monto,monthname(pagosres.fecha) as mes,sum(pagosres.mora) as mora from pagosres where pagosres.fecha between "+"'"+str(row['fechadesde'])+"' and "+"'"+str(row['fechahasta'])+"'"+"  group by month(fecha) "
            mycursor.execute(sql)
            grafico = mycursor.fetchall()

            listavalor = []
            listames = []
            listamora = []
            for x in grafico:
                listavalor.append(x['monto'])
                listames.append(x['mes']) 
                listamora.append(x['mora'])

          conectar.close() 
           
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data,"listavalor": listavalor, "listames":listames,"listamora":listamora}),200)
       return res; 

@consultarpagos_api.route("/api/consultarpagosgeneral",methods=['POST','GET'])
def consultarpagosgeneral():
    
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
          sql = "select pagosres.noprest as Noprest, pagosres.norecibo as Norecibo,date_format(pagosres.fecha,'%d-%m-%Y') as Fecha,\
          concat(solicit.nombres,' ',solicit.apellidos) as Nombres,format((pagosres.vpagint+pagosres.vpagcap+vpagmora),2) as Cuota, format(pagosres.vpagmora,2) as Mora,\
          pagosres.norecibo as id from pagosres \
          inner join solicit on pagosres.nosolic = solicit.id  where pagosres.cuota <> 0 order by pagosres.fecha desc limit 30 "
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          if mycursor.rowcount == 0:
             aerror = True
             error = "No hay datos para recuperar" 

          else:
              sql = "select sum(pagosres.cuota) as monto,monthname(pagosres.fecha) as mes,sum(pagosres.mora) as mora from pagosres group by month(fecha) "
              mycursor.execute(sql)
              grafico = mycursor.fetchall()

              listavalor = []
              listames = []
              listamora = []
              for x in grafico:
                 listamora.append(x['mora'])
                 listavalor.append(x['monto'])
                 listames.append(x['mes']) 
                 
          
          conectar.close() 
           
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data,"listavalor": listavalor, "listames":listames,"listamora":listamora}),200)
       return res; 
            