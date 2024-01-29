from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 

vendedor_api = Blueprint('vendedor_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.user
app.config['MYSQL_DATABASE'] = configuracionservidor.database
app.config['MYSQL_HOST'] = configuracionservidor.host
app.config['MYSQL_PASSWORD'] = configuracionservidor.password
mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)



@vendedor_api.route("/api/vendedor_lista")
def vendedor_lista():
    
    aerror = False
    
    try:
        conectar = mysql.connection
        mycursor = conectar.cursor()
        sql = "select id1,descrip from vendedor"
        mycursor.execute(sql)
        misclientes = mycursor.fetchall()

        conectar.close()
        res = make_response(jsonify(misclientes),200)
        return res 
    except Exception as e:
        error = True
        aerror = "Problemas para conectar la tabla "+str(e)        
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@vendedor_api.route("/api/vendedor_insertarvendedor",methods=['POST'])
def vendedor_insertarvendedor():

    conectar = mysql.connection
    row = request.get_json()
    aerror = False
    
    if aerror == False:
       if not 'nombrevendedor' in row or len(row['nombrevendedor']) == 0:
          aerror = True
          error  = "El nombre del Cliente no puede estar en blanco"
    
    if aerror == False:
      x = 0
      if x == 0:
      #try: 
         mycursor = conectar.cursor()
         sql = "INSERT into vendedor(descrip,creado,modificado,fechamod) values (%s,%s,%s,%s)"
         val = (row['nombrevendedor'],"","",datetime.now().date())
         mycursor.execute(sql,val) 
         

         if mycursor.rowcount == 0:
            aerror = True
            error = "Datos no fueron registrados"
         else:
            aerror = False
            error  = "Datos Grabados Correctamente"

         conectar.commit()
         conectar.close()

      #except Exception as e:
      #   aerror = True
      #   error = "Problemas para instertar en tabla de vendedores "+str(e)
    

    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

    if aerror == False:
       res = make_response(jsonify({"Error": error}),200)
       return res; 
      

@vendedor_api.route("/api/vendedor_eliminarvendedor",methods=['POST'])
def vendedor_eliminarvendedor():

    row = request.get_json()
    aerror = False

    try:
      conectar = mysql.connection
      mycursor = conectar.cursor()
      sql = "delete from vendedor where id1 = "+str(row['id']) 
      mycursor.execute(sql)

      conectar.commit()
      conectar.close()  
    except Exception as e:
      aerror = True
      error = "Problemas para eliminar el vendedor "+str(e) 


    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

    if aerror == False:
       res = make_response(jsonify({"Error": "Vendedor Eliminado Correctamente"}),200)
       return res; 
