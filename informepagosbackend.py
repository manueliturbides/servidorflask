from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 


informespagosbackend_api = Blueprint('informepagosbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)

@informespagosbackend_api.route("/api/informespagoscancelados",methods=['POST','GET'])
def informespagoscancelados():
    
    aerror = False
    salida = {}
    row = request.get_json()
   
    if aerror == False:
       if len(row['fechadesde']) == 0 or row['fechadesde'] == None or row['fechadesde'] == '':
          aerror = True
          error = "La fecha desde donde quiere ver los pagos cancelados no puede estar en blanco"

    if aerror == False:
       if len(row['fechahasta']) == 0 or row['fechahasta'] == None or row['fechahasta'] == '':
          aerror = True
          error = "La fecha hasta donde quiere ver los pagos cancelados no puede estar en blanco"
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select pagoscanc.norecibo as id,date_format(pagoscanc.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,format(cuota,2) as cantsol,plazo,interes\
             mora from pagoscanc inner join prestamo on pagoscanc.noprest = prestamo.noprest "+\
             "where pagoscanc.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' group by pagoscanc.norecibo"            
          else:
             sql = "select pagoscanc.norecibo as id,date_format(pagoscanc.fecha,'%d-%m-%Y') as fecha,nombres,apellidos,format(sum(cuota),2) as cantsol, plazo,interes \
             mora from pagoscanc inner join prestamo on pagoscanc.noprest = prestamo.noprest "+\
             "where pagoscanc.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' and sucursal ="+"'"+str(row['sucursal'].split("-")[0])+"'"+" group by pagoscanc.norecibo"
                 
          mycursor.execute(sql)
          miprestamo = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             salida["prestamo"] = miprestamo
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay pagos cancelados registradas en las fechas seleccionadas"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    
@informespagosbackend_api.route("/api/informespagos",methods=['POST','GET'])
def informespagos():
    aerror = False
    salida = {}
    row = request.get_json()
   
    if aerror == False:
       if len(row['fechadesde']) == 0 or row['fechadesde'] == None or row['fechadesde'] == '':
          aerror = True
          error = "La fecha desde donde quiere ver los pagos no puede estar en blanco"

    if aerror == False:
       if len(row['fechahasta']) == 0 or row['fechahasta'] == None or row['fechahasta'] == '':
          aerror = True
          error = "La fecha hasta donde quiere ver los pagos no puede estar en blanco"
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
         
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select pagos.norecibo as id,date_format(pagos.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,format(cuota,2) as cantsol,\
             mora from pagos inner join prestamo on pagos.noprest = prestamo.noprest "+\
             "where pagos.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' group by pagos.norecibo"            
          else:
             sql = "select pagos.norecibo as id,date_format(pagos.fecha,'%d-%m-%Y') as fecha,nombres,apellidos,format(sum(cuota),2) as cantsol,\
             mora from pagos inner join prestamo on pagos.noprest = prestamo.noprest "+\
             "where pagos.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' and sucursal ="+"'"+str(row['sucursal'].split("-")[0])+"'"+" group by pagos.norecibo"
                 
          mycursor.execute(sql)
          miprestamo = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             salida["prestamo"] = miprestamo
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay pagos registradas en las fechas seleccionadas"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    
@informespagosbackend_api.route("/api/auditoriarecibos",methods=['POST','GET'])
def auditoriarecibos():
    aerror = False
    salida = {}
    row = request.get_json()
   
    if aerror == False:
       if len(row['recibodesde']) == 0 or row['recibodesde'] == None or row['recibodesde'] == '':
          aerror = True
          error = "Los recibos desde donde quiere ver los pagos no puede estar en blanco"

    if aerror == False:
       if len(row['recibohasta']) == 0 or row['recibohasta'] == None or row['recibohasta'] == '':
          aerror = True
          error = "Los recibos hasta donde quiere ver los pagos no puede estar en blanco"
    
    if aerror == False:
       if int(row['recibohasta']) < int(row['recibohasta']):
          aerror = True
          error = "El rango del recibo es incorrecto, por favor revise"   


    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
         
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select pagos.norecibo as id,date_format(pagos.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,format(cuota,2) as cantsol,\
             mora from pagos inner join prestamo on pagos.noprest = prestamo.noprest "+\
             "where pagos.norecibo between "+"'"+row['recibodesde']+"' and "+"'"+row['recibohasta']+"' group by pagos.norecibo"            
          else:
             sql = "select pagos.norecibo as id,date_format(pagos.fecha,'%d-%m-%Y') as fecha,nombres,apellidos,format(sum(cuota),2) as cantsol,\
             mora from pagos inner join prestamo on pagos.noprest = prestamo.noprest "+\
             "where pagos.norecibo between "+"'"+row['recibodesde']+"' and "+"'"+row['recibohasta']+"' and sucursal ="+"'"+str(row['sucursal'].split("-")[0])+"'"+" group by pagos.norecibo"
                 
          mycursor.execute(sql)
          mirecibos = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             salida["recibos"] = mirecibos
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay pagos registradas en las fechas seleccionadas"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 


@informespagosbackend_api.route("/api/recuperasucursales",methods=['POST','GET'])
def recuperasucursales():
    aerror = False
    salida = {}
    row = request.get_json()
   
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          sql = "select concat(sucursal,'-',descripcion) as label from sucursal"
                 
          mycursor.execute(sql)
          misucursal = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             salida["sucursales"] = misucursal
             res = make_response(jsonify(salida),200)
             return res 
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 



@informespagosbackend_api.route("/api/proyeccioncobros",methods=['POST','GET'])
def proyeccioncobros():
    aerror = False
    salida = {}
    row = request.get_json()
    
     

    if aerror == False:
       if len(row['fechadesde']) == 0 or row['fechadesde'] == None or row['fechadesde'] == '':
          aerror = True
          error = "La fecha desde donde quiere ver los pagos no puede estar en blanco"

    if aerror == False:
       if len(row['fechahasta']) == 0 or row['fechahasta'] == None or row['fechahasta'] == '':
          aerror = True
          error = "La fecha hasta donde quiere ver los pagos no puede estar en blanco"
    

    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select amort.noprest as id,format(sum(amort.capital+amort.interes-amort.vpagcuota),2) as proyectado,prestamo.nombres,prestamo.apellidos,count(amort.nocuota) as cantcuotas,prestamo.periodos as tipodepago from amort"+\
             " inner join prestamo on amort.noprest = prestamo.noprest where amort.status <> 'C' and "+\
             "amort.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' group by amort.noprest"
          else:
             sql = "select amort.noprest as id,format(sum(amort.capital+amort.interes-amort.vpagcuota),2) as proyectado,prestamo.nombres,prestamo.apellidos,count(amort.nocuota) as cantcuotas,prestamo.periodos as tipodepago from amort"+\
             " inner join prestamo on amort.noprest = prestamo.noprest where amort.status <> 'C' and "+\
             "amort.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' and sucursal ="+"'"+str(row['sucursal'].split("-")[0])+"'"+" group by amort.noprest"
                    
          mycursor.execute(sql)
          micobros = mycursor.fetchall()
          if mycursor.rowcount != 0:
             salida["cobros"] = micobros
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay datos para procesar en las fechas seleccionadas"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@informespagosbackend_api.route("/api/interescobradosperiodos",methods=['POST','GET'])
def interescobradosperiodos():
    aerror = False
    salida = {}
    row = request.get_json()
    
     

    if aerror == False:
       if len(row['fechadesde']) == 0 or row['fechadesde'] == None or row['fechadesde'] == '':
          aerror = True
          error = "La fecha desde donde quiere ver los pagos no puede estar en blanco"

    if aerror == False:
       if len(row['fechahasta']) == 0 or row['fechahasta'] == None or row['fechahasta'] == '':
          aerror = True
          error = "La fecha hasta donde quiere ver los pagos no puede estar en blanco"
    

    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select pagos.norecibo as id,format(sum(pagos.vpagint),2) as valor,prestamo.nombres,prestamo.apellidos from pagos"+\
             " inner join prestamo on pagos.noprest = prestamo.noprest where "+\
             "pagos.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' group by pagos.norecibo"
          else:
             sql = "select pagos.norecibo as id,format(sum(pagos.vpagint),2) as valor,prestamo.nombres,prestamo.apellidos from pagos"+\
             " inner join prestamo on pagos.noprest = prestamo.noprest where  "+\
             "pagos.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"' and sucursal ="+"'"+str(row['sucursal'].split("-")[0])+"'"+" group by pagos.noprest"
                    
          mycursor.execute(sql)
          micobros = mycursor.fetchall()
          if mycursor.rowcount != 0:
             salida["cobros"] = micobros
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay datos para procesar en las fechas seleccionadas"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 