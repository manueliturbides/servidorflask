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

consultasolicitud_api = Blueprint('consultasolicitud_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@consultasolicitud_api.route("/api/consultarsolicitud",methods=['POST','GET'])
def consultarsolicitud():
    
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
          sql = "select solicit.id as Nosolic,date_format(solicit.fecha_crea,'%d-%m-%Y') as Fecha,concat(solicit.nombres,' ',solicit.apellidos) as Nombres,\
          format(solicit.deudatotal,2) as Valor,\
          solicit.aprobado as Aprobado,solicit.id as id from solicit \
          where solicit.fecha_crea between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          if mycursor.rowcount == 0:
             aerror = True
             error = "No hay datos que recuperar" 
          else:   
             sql = "select sum(solicit.deudatotal) as monto,monthname(solicit.fecha_crea) as mes from solicit group by month(fecha_crea) "
             mycursor.execute(sql)
             grafico = mycursor.fetchall()

             listavalor = []
             listames = []
             for x in grafico:
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
       res = make_response(jsonify({"data":data,"listavalor":listavalor,"listames":listames}),200)
       return res; 
      