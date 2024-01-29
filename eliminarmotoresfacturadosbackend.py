from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 


eliminarmotoresfacturadosbackend_api = Blueprint('eliminarmotoresfacturadosbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)

@eliminarmotoresfacturadosbackend_api.route("/api/eliminarmotoresfacturados",methods=['POST','GET'])
def eliminarmotoresfacturados():
    
    aerror = False
    salida = {}
    row = request.get_json()
        
    conectar = mysql.connection
    mycursor = conectar.cursor(dictionary=True)
    sql = "select factmot.noprest,prestamo.status from factmot " +\
    "left join prestamo on factmot.noprest = prestamo.noprest  where factmot.secuencia = "+"'"+str(row['id'])+"'"
    mycursor.execute(sql)
    misfacturas = mycursor.fetchall()
    if mycursor.rowcount != 0:
      if misfacturas[0]['status'] == "A":
         error = "No puede eliminar factura con prestamo activo "+str(misfacturas[0]['noprest'])
         aerror = True
      else:
         mycursor = conectar.cursor()
         sql = "delete from factmot where secuencia = "+"'"+str(row['id'])+"'"
         mycursor.execute(sql)
    else:
         aerror = True
         error = "No hay datos para eliminar "
    conectar.commit()
    conectar.close()
    mensajeok = "Datos Eliminados Correctamente"
         
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"dataok": mensajeok}),200)
       return res     

