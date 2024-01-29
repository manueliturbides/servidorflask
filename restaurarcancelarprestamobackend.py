from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 


restaurarcancelarprestamobackend_api = Blueprint('restaurarcancelarprestamobackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)

@restaurarcancelarprestamobackend_api.route("/api/cancelarprestamo",methods=['POST','GET'])
def cancelarprestamo():
    
    aerror = False
    salida = {}
    row = request.get_json()
   
    try:
       conectar = mysql.connection
       mycursor = conectar.cursor()
       sql = "update prestamo set status = 'C',fcancel = "+"'"+str(datetime.now().date())+"'"+" where noprest = "+str(row['id'])
       mycursor.execute(sql)

       mycursor = conectar.cursor(dictionary=True)
       sql = "select estado from previnc where estado <> 'C' and nuprest = "+"'"+str(row['id'])+"'"            
       mycursor.execute(sql)
       miprevinc = mycursor.fetchall()

       if len(miprevinc) != 0:
           mycursor = conectar.cursor()
           sql = "update previnc set estado = 'C' where nuprest = "+"'"+str(row['id'])+"'"
           mycursor.execute(sql)

           mycursor = conectar.cursor()
           sql = "update solicit set status = '' where noprest = "+"'"+str(row['id'])+"'"
           mycursor.execute(sql)

           mycursor = conectar.cursor(dictionary=True)
           sql = "select inicial from factmot where noprest = "+"'"+str(row['id'])+"'"
           mycursor.execute(sql)
           miinicial = mycursor.fetchall()

           if mycursor.rowcount != 0:    
              pass
              #mycursor = conectar.cursor()
              #costoadescontar = float(self.tableWidget.item(fila,3).text())-miinicial[0]['inicial']
              #sql = "update producto set "+\
              #"estado = ' ', costo = costo - "+str(costoadescontar)+",condicion = 'U'"+\
              #" where noprest = "+"'"+str(self.lenoprest.text().split("-")[0])+"'" 
              #mycursor.execute(sql)
                
                
              mycursor = conectar.cursor()
              sql = "update producto set costo = if(costo<=0,1000,costo) where noprest = "+"'"+str(row['id'])+"'"
              mycursor.execute(sql)
      
       conectar.commit()
       conectar.close() 
       
    except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"mensajeok": "Prestamos cancelado correctamente"}),200)
       return res; 
      
 
@restaurarcancelarprestamobackend_api.route("/api/restaurarprestamo",methods=['POST','GET'])
def restaurarprestamo():
    
    aerror = False
    salida = {}
    row = request.get_json()

    try:
       conectar = mysql.connection
       mycursor = conectar.cursor(dictionary=True)
       sql = "select prestamo.noprest,prestamo.chasis as prestchasis, producto.chasis as prodchasis from prestamo "+\
       " inner join producto on prestamo.noprest = producto.noprest "
       mycursor.execute(sql)
       miproducto = mycursor.fetchall()
       if mycursor.rowcount != 0:
          if miproducto[0]['prestchasis'] != miproducto[0]['prodchasis']:
             aerror = True
             error = "Este prestamo no se puede restaurar debido al que el chasis ya fue asignado a otro prestamo"
       else:
          mycursor = conectar.cursor(dictionary=True)
          sql = "select status from prestamo where noprest = "+"'"+str(row['id'])+"'"
          mycursor.execute(sql)
          miprestamo = mycursor.fetchall() 
     
       if mycursor.rowcount != 0:
          if miprestamo[0]['status'] == 'C':
             mycursor1 = conectar.cursor()
             sql = "update prestamo set status = 'A',fcancel = Null where noprest ="+"'"+str(row['id'])+"'"
             mycursor1.execute(sql)

       conectar.commit()
       conectar.close()          
    except Exception as e: 
       aerror = True
       error = "No se puede conectar con la tabla de amortizacion "+str(e)

    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"mensajeok": "Prestamo restaurado correctamente"}),200)
       return res;  