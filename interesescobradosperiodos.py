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


interesescobradosperiodos_api = Blueprint('interesescobradosperiodos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@interesescobradosperiodos_api.route("/api/interesescobradosperiodos",methods=['POST','GET'])
def interesescobradosperiodos():
    
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
          sql = "select pagosres.norecibo as Nrecibo,pagosres.noprest as Noprest,date_format(pagosres.fecha,'%d-%m-%Y') as Fecha,\
          format(pagosres.vpagint,2) as Valor, concat(nombres,' ',apellidos) as Nombres,pagosres.norecibo as id from pagosres \
          inner join prestamo on pagosres.noprest = prestamo.noprest \
          where pagosres.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
          mycursor.execute(sql)
          data = mycursor.fetchall()
          

          if mycursor.rowcount == 0:
             aerror = True
             error = "No hay datos para recuperar" 
          else:          
             sql = "select sum(pagosres.vpagint) as monto,monthname(pagosres.fecha) as mes,month(pagosres.fecha) as mesnumero from pagosres group by month(pagosres.fecha) "
             mycursor.execute(sql)
             grafico = mycursor.fetchall()

             listavalor = []
             listames = []
             listamesnumero = []
             for x in grafico:
                 listavalor.append(str(x['monto']))
                 listames.append(x['mes'])
                 listamesnumero.append(x['mesnumero']) 
          conectar.close() 
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data,"listavalor":listavalor,"listames":listames,"listamesnumero":listamesnumero}),200)
       return res; 

@interesescobradosperiodos_api.route("/api/interesescobradosperiodosgeneral",methods=['POST','GET'])
def interesescobradosperiodosgeneral():
    
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
          sql = "select pagosres.norecibo as Nrecibo,pagosres.noprest as Noprest,date_format(pagosres.fecha,'%d-%m-%Y') as Fecha,\
          format(pagosres.vpagint,2) as Valor, concat(nombres,' ',apellidos) as Nombres,pagosres.norecibo as id from pagosres \
          inner join prestamo on pagosres.noprest = prestamo.noprest limit 30"
          mycursor.execute(sql)
          data = mycursor.fetchall()
          

          if mycursor.rowcount == 0:
             aerror = True
             error = "No hay datos para recuperar" 
          else:          
             sql = "select sum(pagosres.vpagint) as monto,monthname(pagosres.fecha) as mes,month(pagosres.fecha) as mesnumero from pagosres group by month(pagosres.fecha) limit 30"
             mycursor.execute(sql)
             grafico = mycursor.fetchall()

             listavalor = []
             listames = []
             listamesnumero = []
             for x in grafico:
                 listavalor.append(str(x['monto']))
                 listames.append(x['mes'])
                 listamesnumero.append(x['mesnumero']) 
          conectar.close() 
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data,"listavalor":listavalor,"listames":listames,"listamesnumero":listamesnumero}),200)
       return res; 
            