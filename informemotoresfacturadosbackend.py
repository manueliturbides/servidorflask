from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime,timedelta
from flask_mysql_connector import MySQL
import configuracionservidor 


informesmotoresfacturadosbackend_api = Blueprint('informemotoresfacturadosbackend_api',__name__)
modificachasisincautados_api = Blueprint('modificachasisincautados_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)


@informesmotoresfacturadosbackend_api.route("/api/informemotoresfacturados",methods=['POST','GET'])
def informemotoresfacturados():
    
    aerror = False
    salida = {}
    row = request.get_json()
   
    if aerror == False:
       if len(row['fechadesde']) == 0 or row['fechadesde'] == None or row['fechadesde'] == '':
          aerror = True
          error = "La fecha desde donde quiere ver la facturacion no puede estar en blanco"

    if aerror == False:
       if len(row['fechahasta']) == 0 or row['fechahasta'] == None or row['fechahasta'] == '':
          aerror = True
          error = "La fecha hasta donde quiere ver los eventos no puede estar en blanco"
    
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select secuencia as id,date_format(fecha,'%d-%m-%Y') as fecha,nombres,apellidos,chasis,\
             financia from factmot where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
          else:
             sql = "select secuencia as id,date_format(fecha,'%d-%m-%Y') as fecha,nombres,apellidos,chasis,\
             financia from factmot where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
                 
          mycursor.execute(sql)
          mifacturacion = mycursor.fetchall()
          
          if mycursor.rowcount != 0:
             salida["facturacion"] = mifacturacion
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay facturas registradas en las fechas seleccionadas"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 



@modificachasisincautados_api.route("/api/modificachasisincautados",methods=['POST','GET'])
def modificachasisincautados():
    
    aerror = False
    salida = {}
    row = request.get_json()
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary = True)
          sql="select secuencia,if(chasis is null,'',chasis) as chasis,noprest from factmot where chasis = "+"'"+row['chasis']+"'"
          mycursor.execute(sql)
          mifactura= mycursor.fetchall()

          if mycursor.rowcount != 0:
              mycursor = conectar.cursor(dictionary = True)
              sql="select if(chasis is null,'',chasis) as chasis,marca,modelo,colore, if(estado is null,'',estado) as estado from producto "+\
              "where chasis = "+"'"+row['chasisacambiar']+"'"
              mycursor.execute(sql)
              michasis = mycursor.fetchall()

              if mycursor.rowcount != 0:
                 if len(michasis[0]['estado']) == 0:
                    ####Grabar data
                    mycursor = conectar.cursor()
                    sql = "update factmot set "+\
                    " chasis = "+"'"+michasis[0]['chasis']+"',"+\
                    " marca = "+"'"+michasis[0]['marca']+"',"+\
                    " modelo = "+"'"+michasis[0]['modelo']+"',"+\
                    " colore = "+"'"+michasis[0]['colore']+"' where secuencia = "+str(mifactura[0]['secuencia'])
                    mycursor.execute(sql)

                    mycursor = conectar.cursor()
                    sql = "update prestamo set "+\
                    " chasis = "+"'"+michasis[0]['chasis']+"'"+\
                    " where noprest = "+"'"+str(mifactura[0]['noprest'])+"'"
                    mycursor.execute(sql)

                    mycursor = conectar.cursor()
                    sql = "update producto set "+\
                    " estado = 'V', noprest = "+"'"+str(mifactura[0]['noprest'])+"'"+\
                    " where chasis = "+"'"+michasis[0]['chasis']+"'"
                    mycursor.execute(sql)

                    mycursor = conectar.cursor()
                    sql = "update producto set "+\
                    " estado = ' ', noprest = 0 "+\
                    " where chasis = "+"'"+mifactura[0]['chasis']+"'"
                    mycursor.execute(sql)

                    mycursor = conectar.cursor()
                    sql = "update producto set "+\
                    " estado = '' "+\
                    " where chasis = "+"'"+str(mifactura[0]['chasis'])+"'"
                    mycursor.execute(sql)

                    res = make_response(jsonify({"OK": "Datos guardados correctamente"}),200)
        
          
                 else:
                    if michasis[0]['estado'] != "I":

                       if michasis[0]['estado'] == "A":
                          res = make_response(jsonify({"Error": "El chasis tiene un prestamo asignado, debe cancelar el prestamo #"+str(michasis[0]['noprest'])}),400)
                          return res
                       else:
                          if michasis[0]['estado'] == "V":
                             res = make_response(jsonify({"Error": "Este chasis pertenece a un motor previamente vendido"}),400)
                             return res

              else:
                res = make_response(jsonify({"Error": "El chasis no existe o no ha sido registrado"}),400)
                return res
          conectar.commit()
          conectar.close()
          
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 


@informesmotoresfacturadosbackend_api.route("/api/facturacionultimomes",methods=['POST','GET'])
def facturacionultimomes():
    
    aerror = False
    row = request.get_json()
    salida = {}
   
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select ifnull(sum(precio),0) as precio,ifnull(0,count(precio)) as cantidad, fecha from factmot where month(fecha)  = "+"'"+str(datetime.now().month)+"' and year(fecha) = "+"'"+str(datetime.now().year)+"'"
          mycursor.execute(sql)
          mifacturacion = mycursor.fetchall()
          
          mycursor = conectar.cursor(dictionary=True)
          sql = "select ifnull(sum(cantsol),0) as valor from prestamo where month(fecha)  = "+"'"+str(datetime.now().month)+"' and year(fecha) = "+"'"+str(datetime.now().year)+"'"
          mycursor.execute(sql)
          miprestamo = mycursor.fetchall()
          
          mycursor = conectar.cursor(dictionary=True)
          sql = "select ifnull(sum(vpagcap),0) as valor from pagosres where month(fecha_crea)  = "+"'"+str(datetime.now().month)+"' and year(fecha_crea) = "+"'"+str(datetime.now().year)+"'"
          mycursor.execute(sql)
          mipagos = mycursor.fetchall()
         
          #determinar los dias de semana a partir del dia de hoy
          mycursor = conectar.cursor(dictionary=True)
         
          sql = "select fecha,sum(vpagint+vpagmora+vpagcap) as cobros from pagos where fecha between "+"'"+str(datetime.today().date()-timedelta(days=7))+"'"+\
          " and "+"'"+str(datetime.now().date())+"'"+" group by fecha"
          mycursor.execute(sql)
          mispagosporfecha = mycursor.fetchall()           
          
          diasdesemana = []
          valores = []

          for x in mispagosporfecha:
              if x['fecha'].weekday() == 1:
                 diasdesemana.append("D")
                 valores.append(x['cobros'])
            
              if x['fecha'].weekday() == 2:
                 diasdesemana.append("Lu")
                 valores.append(x['cobros'])
             
              if x['fecha'].weekday() == 3:
                 diasdesemana.append("Ma")
                 valores.append(x['cobros'])
             
              if x['fecha'].weekday() == 4:
                 diasdesemana.append("Mi")
                 valores.append(x['cobros'])
              
              if x['fecha'].weekday() == 5:
                 diasdesemana.append("Ju")
                 valores.append(x['cobros'])
              else:
                 if x['fecha'].weekday() == 6:
                    diasdesemana.append("Vi")
                    valores.append(x['cobros'])
              
              if x['fecha'].weekday() == 7:
                 diasdesemana.append("S")
                 valores.append(x['cobros'])
                    
          json = {
             "label": diasdesemana,
             "etiqueta": "label",
             "valor": valores
          }
          
          #ventasultimos seis meses motores
          mycursor = conectar.cursor(dictionary=True)
          sql = "select month(fecha) as fecha,sum(precio) as valor from factmot where fecha between "+"'"+str(datetime.today().date()-timedelta(days=183))+"'"+\
          " and "+"'"+str(datetime.now().date())+"'"+" group by MONTH(fecha)"
          mycursor.execute(sql)
          mifacturapormes = mycursor.fetchall()           
          

          nmes = []
          mesvalor = []
          for x in mifacturapormes:
              if x['fecha'] == 1:
                 nmes.append("Ene")
                 mesvalor.append(x['valor'])
                 
              if x['fecha'] == 2:
                 nmes.append("Feb")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 3:
                 nmes.append("Mar")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 4:
                 nmes.append("Abr")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 5:
                 nmes.append("May")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 6:
                 nmes.append("Jun")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 7:
                 nmes.append("Jul")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 8:
                 nmes.append("Ago")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 9:
                 nmes.append("Sep")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 10:
                 nmes.append("Oct")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 11:
                 nmes.append("Nov")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 12:
                 nmes.append("Dic")
                 mesvalor.append(x['valor'])
              
          jsonmesvalor = {
             "label": nmes,
             "etiqueta": "Mes",
             "valor": mesvalor
          }
           
          #cobrosultimos seis meses motores
          mycursor = conectar.cursor(dictionary=True)
          sql = "select month(fecha) as fecha,sum(vpagint+vpagcap+vpagmora) as valor from pagos where fecha between "+"'"+str(datetime.today().date()-timedelta(days=183))+"'"+\
          " and "+"'"+str(datetime.now().date())+"'"+" group by MONTH(fecha)"
          mycursor.execute(sql)
          mispagospormes = mycursor.fetchall()           
          

          nmes = []
          mesvalor = []
          for x in mispagospormes:
              if x['fecha'] == 1:
                 nmes.append("Ene")
                 mesvalor.append(x['valor'])
                 
              if x['fecha'] == 2:
                 nmes.append("Feb")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 3:
                 nmes.append("Mar")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 4:
                 nmes.append("Abr")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 5:
                 nmes.append("May")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 6:
                 nmes.append("Jun")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 7:
                 nmes.append("Jul")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 8:
                 nmes.append("Ago")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 9:
                 nmes.append("Sep")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 10:
                 nmes.append("Oct")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 11:
                 nmes.append("Nov")
                 mesvalor.append(x['valor'])
              
              if x['fecha'] == 12:
                 nmes.append("Dic")
                 mesvalor.append(x['valor'])
              
          jsonpagosvalor = {
             "label": nmes,
             "etiqueta": "Mes",
             "valor": mesvalor
          }
          
          salida["facturacion"] = mifacturacion
          salida["prestamo"] = miprestamo
          salida["pagos"] = mipagos
          salida["datachart"] = json
          salida['mesvalor'] = jsonmesvalor
          salida['pagosvalor'] = jsonpagosvalor
          res = make_response(jsonify(salida),200)
          
          
          return res
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
