from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor
from procconectar import conectUserDatabase 


pagosprestamos_api = Blueprint('pagosprestamos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@pagosprestamos_api.route("/api/recuperartablaamortizacion",methods=['POST','GET'])
def recuperartablaamortizacion():
    
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
          sql = "select amort.nocuota as Cuota,date_format(amort.fecha,'%d-%m-%Y') as Fecha,concat(prestamo.nombres,' ',prestamo.apellidos) as Nombres,\
              format(amort.capital+amort.interes-amort.vpagcap-amort.vpagint,2) as Valor, \
              if(datediff("+"'"+str(datetime.now().date())+"'"+",amort.fecha) > 3,\
              ((solicit.valorcuotas*(solicit.mora/100))/30)*(datediff("+"'"+str(datetime.now().date())+"'"+",amort.fecha)),'0.00') as Mora,\
              '0.00' as Pagado,'0.00' as PagMora, 0.0 as Balance, \
              (amort.interes-amort.vpagint) as sinteres,(amort.capital-amort.vpagcap) as scapital,amort.noprest as Snoprest,\
              solicit.id as id,pagadodescuento,format(descuento,2) as descuento \
              from amort \
              inner join prestamo on amort.noprest = prestamo.noprest \
              inner join solicit on amort.nosolic = solicit.id \
              where amort.noprest = "+"'"+row['noprest']+"' and amort.status <> 'P'"          
           
          mycursor.execute(sql)
          data = mycursor.fetchall()

          
          #extracion de datos de prestamos generales
          sql = "select count(cedula) as cedula  from prestamo \
          where prestamo.cedula = "+"'"+str(row['noprest'].split("/")[2])+"' and prestamo.status = 'A'"
          mycursor.execute(sql)
          datacuentaactiva = mycursor.fetchall()
          
          #extraccion data prestamo activo
          sql = "select date_format(prestamo.fultpago,'%d-%m-%Y') as fultpago, \
          format((solicit.deudatotal-prestamo.vpagint-prestamo.vpagcap),2) as pendiente,\
          format(prestamo.montoult,2) as montoult,format(prestamo.vpagmora,2) as vpagmora,format(prestamo.vpagcap,2) as vpagcap,\
          format((prestamo.vpagcap+prestamo.vpagint+prestamo.vpagmora),2) as recibido, solicit.formapago  from prestamo \
          inner join solicit on solicit.id = prestamo.nosolic \
          where noprest = "+"'"+str(row['noprest'].split("/")[0])+"'"

          mycursor.execute(sql) 
          dataprestamo = mycursor.fetchall()
          
          print(data)
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"data":data,"datacuentaactiva":datacuentaactiva,"dataprestamo": dataprestamo}),200)
       return res; 

@pagosprestamos_api.route("/api/recuperarprestamosactivos",methods=['POST','GET'])
def recuperarprestamosactivos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select concat(prestamo.noprest,'/',prestamo.nombres,' ',prestamo.apellidos,'/',solicit.cedula,'/',solicit.id) as label \
          from prestamo \
          inner join solicit on prestamo.nosolic = solicit.id \
          where status = 'A'"


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

@pagosprestamos_api.route("/api/guardardatospagos",methods=['POST','GET'])
def guardardatospagos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    
    try:
       ###validar campos de entrada
      
       aerror = False
       vinterespagado = 0
       vcapitalpagado = 0
       tvinterespagado = 0
       tvcapitalpagado = 0
       tmorapagado = 0
       noprest = 0  
       
       conectar = conectUserDatabase(row['parent'])
          
       for x in row['datospago']:
          
          noprest = x['Snoprest']
          mycursor = conectar.cursor()
      
          if (float(x['Pagado']) <= float(x['Sinteres'])):
             vinterespagado = float(x['Pagado'])
             tvinterespagado = tvinterespagado + vinterespagado
             vcapitalpagado = 0
          else:
             vinterespagado = float(x['Sinteres'])
             tvinterespagado = tvinterespagado + vinterespagado
             vcapitalpagado = float(x['Pagado']) - float(x['Sinteres'])     
             tvcapitalpagado = tvcapitalpagado + vcapitalpagado
   
          tmorapagado = tmorapagado + float(x['Mora'])

          sql = "update amort set vpagcap = vpagcap + "+"'"+str(vcapitalpagado)+"',"+\
          "vpagint = vpagint + "+"'"+str(vinterespagado)+"',"+\
          "vpagmora = vpagmora + "+"'"+str(x['Mora'])+"',"+\
          " status = if(amort.capital+amort.interes-amort.vpagcap-amort.vpagint = 0,'P',''), "+\
          " pagadodescuento = if(amort.descuento <> 0,'S','N') "+\
          " where noprest = "+"'"+str(x['Snoprest'])+"'"+\
          " and nocuota = "+"'"+str(x['Cuota'])+"'"
          mycursor.execute(sql)

          print(vinterespagado)
          sql = "update prestamo set vpagcap = vpagcap + "+"'"+str(vcapitalpagado)+"',"+\
          "vpagint = vpagint + "+"'"+str(vinterespagado)+"',"+\
          "vpagmora = vpagmora + "+"'"+str(x['Mora'])+"',"+\
          " status = if(prestamo.solicitado-prestamo.vpagcap = 0,'P','A'), "+\
          " fultpago = "+"'"+str(datetime.now().date())+"',"+\
          " montoult = "+"'"+str(x['Totalpago'])+"'"+\
          " where noprest = "+"'"+str(x['Snoprest'])+"'"
          mycursor.execute(sql)
       
          vinterespagado = 0
          vcapitalpagado = 0
       
       sql = "insert into pagosres(noprest,nosolic,cedula,cuota,mora,fecha,vpagint,vpagmora,vpagcap,descinte,\
       user,fecha_crea,fecha_mod,tipodepago,aprobacion,numerotarjeta) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

       val = (noprest,row['nosolic'],row['cedula'],tvcapitalpagado+tvinterespagado+tmorapagado,tmorapagado,\
              datetime.now().date(),tvinterespagado,tmorapagado,tvcapitalpagado,row['descuento'],row['user'],\
               datetime.now().date(),datetime.now().date(),row['tipodepago'],row['aprobacion'],row['numerotarjeta']) 
       mycursor.execute(sql,val)
       
       sql = "select last_insert_id() as list"
       mycursor.execute(sql)
       lastid = mycursor.fetchall()
       
       for x in row['datospago']:
          
          if (float(x['Pagado']) <= float(x['Sinteres'])):
             vinterespagado = float(x['Pagado'])
             vcapitalpagado = 0
          else:
             vinterespagado = float(x['Sinteres'])
             vcapitalpagado = float(x['Pagado']) - float(x['Sinteres'])     
             
          
          if float(x['Pagado']) != 0:
             #actualizar archivos de pagos
             
             sql = "insert into pagos(norecibo,noprest,nosolic,cedula,nocuota,mora,fecha,vpagint,vpagmora,vpagcap,descinte,\
               user,fecha_crea,fecha_mod,cuota,balance) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
         
             val = (lastid[0][0],x['Snoprest'],row['nosolic'],row['cedula'],x['Cuota'],x['Mora'],datetime.now().date(),vinterespagado,\
                x['PagMora'],vcapitalpagado,row['descuento'],row['user'],datetime.now().date(),datetime.now().date(),vcapitalpagado+vinterespagado+float(x['Mora']),x['Balance'])
          
             mycursor.execute(sql,val)
       
  

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
       res = make_response(jsonify({"data":"data"}),200)
       return res; 


@pagosprestamos_api.route("/api/reimprimirrecibodepago",methods=['POST','GET'])
def reimprimirrecibodepago():
    
    aerror = False
    salida = {}
    row = request.get_json()
   
    try:
       ###validar campos de entrada
      
       aerror = False
      
       
       conectar = conectUserDatabase(row['parent'])
       mycursor = conectar.cursor(dictionary=True)
       sql = "select cast(pagos.noprest as char) as Noprest,date_format(pagos.fecha,'%d-%m-%Y') as Fecha,pagos.norecibo,concat(prestamo.nombres,' ',prestamo.apellidos) as Nombres,prestamo.cedula,\
       pagos.cuota as Cuota,(pagos.vpagint+pagos.vpagcap) as Pagado, pagos.vpagmora as Mora, balance as Balance,prestamo.cedula as Cedula from pagos \
       inner join prestamo on pagos.noprest = prestamo.noprest where pagos.norecibo = "+"'"+str(row['norecibo'])+"'"     
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
