from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 

popup_api = Blueprint('popup_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.user
app.config['MYSQL_DATABASE'] = configuracionservidor.database
app.config['MYSQL_HOST'] = configuracionservidor.host
app.config['MYSQL_PASSWORD'] = configuracionservidor.password
mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)



@popup_api.route("/api/popupvendedorarea")
def areageografica_consulta():

    row = request.get_json()

    aerror = False
    
  
    try:
      conectar = mysql.connection
      mycursor = conectar.cursor()
      sql = "select id,id1,descrip from vendedor"
      mycursor.execute(sql)
      misvendedores = mycursor.fetchall()
      
      salida = {}
      salida["datavendedor"] = misvendedores
     
      mycursor = conectar.cursor()
      sql = "select id,ciudad from area"
      mycursor.execute(sql)
      misareas = mycursor.fetchall()
     
      salida["area"] =  misareas
     
      res = make_response(jsonify(salida),200)
      return res; 
      conectar.close()

    except Exception as e:
      aerror = True
      error  = "Problemas de conexion con la tabla vendedores "+str(e)
      

    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
