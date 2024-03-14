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

cancelarpagos_api = Blueprint('cancelarpagos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@cancelarpagos_api.route("/api/cancelarpagos",methods=['POST','GET'])
def consultarpagos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select pagosres.noprest as Noprest, pagosres.norecibo as Norecibo,date_format(pagosres.fecha,'%d-%m-%Y') as Fecha,\
          prestamo.nombres as Nombres,format((pagosres.vpagint+pagosres.vpagcap+vpagmora),2) as Cuota, format(pagosres.vpagmora,2) as Mora,\
          pagosres.norecibo as id from pagosres \
          inner join prestamo on pagosres.noprest = prestamo.noprest \
          where pagosres.fecha between "+"'"+str(row['fechadesde'])+"' and"+"'"+str(row['fechahasta'])+"'"
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          
          conectar.close() 
           
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

@cancelarpagos_api.route("/api/consultarpagosacancelar",methods=['POST','GET'])
def consultarpagosacancelar():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select pagosres.noprest as Noprest, pagosres.norecibo as Norecibo,date_format(pagosres.fecha,'%d-%m-%Y') as Fecha,\
          prestamo.nombres as Nombres,format((pagosres.vpagint+pagosres.vpagcap+pagosres.vpagmora),2) as Cuota, format(pagosres.vpagmora,2) as Mora,\
          pagosres.norecibo as id from pagosres \
          inner join prestamo on pagosres.noprest = prestamo.noprest \
          where prestamo.noprest = "+"'"+row['noprest']+"'"+" and pagosres.fecha between "+"'"+str(row['fechadesde'])+"' and"+"'"+str(row['fechahasta'])+"' order by pagosres.norecibo desc"
          
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          
          conectar.close() 
           
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


@cancelarpagos_api.route("/api/cancelarpagopornumeroderecibo",methods=['POST','GET'])
def cancelarpagopornumeroderecibo():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select vpagint,vpagmora,vpagcap from pagosres where norecibo = "+"'"+str(row['norecibo'])+"'"
          mycursor.execute(sql)
          misdatos = mycursor.fetchall()
          
          mycursor = conectar.cursor()
          sql = " update prestamo set vpagint = vpagint - "+"'"+str(misdatos[0]['vpagint'])+"', vpagmora = vpagmora - "+"'"+str(misdatos[0]['vpagmora'])+"'\
          ,vpagcap = vpagcap - "+"'"+str(misdatos[0]['vpagcap'])+"', status = if(solicitado > vpagint+vpagcap, 'A','C') where noprest = "+"'"+str(row['noprest'])+"'"
          mycursor.execute(sql)

          mycursor = conectar.cursor(dictionary=True)
          sql = "select vpagint,vpagmora,vpagcap,nocuota,norecibo from pagos where norecibo = "+"'"+str(row['norecibo'])+"'"
          mycursor.execute(sql)
          misdatosamort = mycursor.fetchall()
           
          for x in misdatosamort:
              print(x)
              mycursor = conectar.cursor()
              sql = " update amort set vpagint = vpagint - "+"'"+str(x['vpagint'])+"', vpagmora = vpagmora - "+"'"+str(x['vpagmora'])+"'\
             ,vpagcap = vpagcap - "+"'"+str(x['vpagcap'])+"', status = if(cuota > vpagint+vpagcap, 'A','P') where noprest = "+"'"+str(row['noprest'])+"'\
               and nocuota = "+"'"+str(x['nocuota'])+"'" 
              mycursor.execute(sql)
          
          
          sql = "update pagosres set cuota = 0, mora = 0, vpagint = 0, vpagmora = 0, vpagcap = 0, descinte = 0 where norecibo = "+"'"+str(row['norecibo'])+"'"
          mycursor.execute(sql)
          
          sql = "update pagos set cuota = 0, mora  = 0, vpagint = 0, vpagmora = 0, vpagcap = 0, descinte = 0  where norecibo = "+"'"+str(row['norecibo'])+"'"
          mycursor.execute(sql)
          
                    
          conectar.commit()
          conectar.close() 
          
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":"Pago Eliminado Correctamente"}),200)
       return res; 
            