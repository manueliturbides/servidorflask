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

balanceprestamoscliente_api = Blueprint('balanceprestamoscliente_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@balanceprestamoscliente_api.route("/api/balanceprestamoscliente",methods=['POST','GET'])
def balanceprestamoscliente():
    
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
          sql = "select prestamo.noprest as Nprest, concat(prestamo.nombres,' ',prestamo.apellidos) as Nombres,\
          format(solicit.financiamiento,2) as Solicitado,format((solicit.deudatotal-solicit.financiamiento),2) as InteresxCob, format(sum(prestamo.vpagint),2) as VpagInteres, \
          format(prestamo.vpagcap,2) as PagadoCap,format((solicit.financiamiento - prestamo.vpagcap),2) as BalanceCap,format((solicit.deudatotal-solicit.financiamiento-vpagint),2) as BalanceInt, \
          format((solicit.deudatotal - prestamo.vpagint - prestamo.vpagcap),2) as Balance,@numero:=@numero+1 as id from prestamo \
          inner join solicit on prestamo.nosolic = solicit.id \
          where prestamo.status = 'A' "
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          if mycursor.rowcount != 0 and data[0]['id'] != None:
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
          else:
              aerror = True
              error = "No hay datos para recuperar" 
          
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

@balanceprestamoscliente_api.route("/api/balanceprestamosclientegeneral",methods=['POST','GET'])
def balanceprestamosclientegeneral():
    
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
          sql = "select prestamo.noprest as Nprest, concat(prestamo.nombres,' ',prestamo.apellidos) as Nombres,\
          format(solicit.financiamiento,2) as Solicitado,format((solicit.deudatotal-solicit.financiamiento),2) as InteresxCob, format(sum(prestamo.vpagint),2) as VpagInteres, \
          format(prestamo.vpagcap,2) as PagadoCap,format((solicit.financiamiento - prestamo.vpagcap),2) as BalanceCap,format((solicit.deudatotal-solicit.financiamiento-vpagint),2) as BalanceInt, \
          format((solicit.deudatotal - prestamo.vpagint - prestamo.vpagcap),2) as Balance,prestamo.noprest as id from prestamo \
          inner join solicit on prestamo.nosolic = solicit.id \
          where prestamo.status = 'A' limit 30 "
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
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
          else:
              aerror = True
              error = "No hay datos para recuperar" 
          
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
            