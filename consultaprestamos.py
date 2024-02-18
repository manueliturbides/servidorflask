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


consultaprestamos_api = Blueprint('consultaprestamos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@consultaprestamos_api.route("/api/consultarprestamo",methods=['POST','GET'])
def consultarprestamo():
    
    aerror = False
    salida = {}
    row = request.get_json()
    print(row)
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select prestamo.noprest as Noprest,date_format(prestamo.fecha,'%d-%m-%Y') as Fecha,concat(prestamo.nombres,' ',prestamo.apellidos) as Nombres,\
          format(solicit.deudatotal,2) as Valor,\
          prestamo.status as Status,prestamo.noprest as id from prestamo \
          inner join solicit on prestamo.nosolic = solicit.id \
          where prestamo.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
          mycursor.execute(sql)
          data = mycursor.fetchall()
          
          
          sql = "select sum(prestamo.solicitado) as monto,monthname(prestamo.fecha) as mes from prestamo group by month(fecha) "
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
      