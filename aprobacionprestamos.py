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

aprobacionprestamos_api = Blueprint('aprobacionprestamos_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@aprobacionprestamos_api.route("/api/buscaraprobacionprestamos",methods=['POST','GET'])
def buscasaprobacionprestamos():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select id as Num,'2023-10-31' as Fecha,concat(nombres,' ',apellidos) as Nombres,format(financiamiento,2) as Solicitado,format(valorcuotas,2) as Cuotas,\
          format(deudatotal,2) as DeudaTotal,tipofinanciamiento,fecha_crea,plazo,\
          nombres,apellidos,financiamiento,interes,mora from solicit where aprobado <> 'S' or aprobado <> 's' "
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
      
@aprobacionprestamos_api.route("/api/aprobacionprestamos",methods=['POST','GET'])
def aprobacionprestamos():
    
    aerror = False
    salida = {}
    row = request.get_json()

    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "update solicit set aprobado = 'S', user = "+"'"+row['user']+"'"+", fecha_mod = "+"'"+str(datetime.now().date())+"'"+\
          " where id = "+"'"+str(row['id'])+"'"
          mycursor.execute(sql)
                   
          mycursor1 = conectar.cursor(dictionary=True)
          sql = "select id as Num,fecha_crea as Fecha,concat(nombres,' ',apellidos) as Nombres,format(financiamiento,2) as Solicitado,format(valorcuotas,2) as Cuotas,\
          format(deudatotal,2) as DeudaTotal,tipofinanciamiento,fecha_crea,plazo,\
          nombres,apellidos,financiamiento,interes,mora,cedula,valorcuotas,formapago from solicit where id = "+"'"+str(row['id'])+"'"
          mycursor1.execute(sql) 
          data = mycursor1.fetchall()
          
          #crear tabla de amortizacion

          if data[0]['tipofinanciamiento'] == "Soluto":
             
             #grabar prestamos
             sql = "insert into prestamo(nosolic,fecha,periodos,nombres,apellidos,solicitado,plazo,\
             interes,mora,status,vpagcap,vpagint,vpagmora,norecibo,montoult,user,fecha_crea,fecha_mod,cedula) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
             
             val= (data[0]['Num'],data[0]['fecha_crea'],data[0]['plazo'],data[0]['nombres'],data[0]['apellidos'],\
                   data[0]['financiamiento'],data[0]['plazo'],data[0]['interes'],data[0]['mora'],"A",0.0,0.0,0.0,0,0.0,\
                   row['user'],datetime.now().date(),datetime.now().date(),data[0]['cedula'])
             mycursor.execute(sql,val)

             noprest = "select last_insert_id() as noprest"
             mycursor.execute(noprest)
             nopres1 = mycursor.fetchall()    
            

             #determinacion de fecha
             fechacuota = datetime.now().date()
             diainciocuota = fechacuota.day     
             diferenciadia = 0

             if data[0]['formapago'] == "Diario": 
                fechacuota = fechacuota + timedelta(days = 1)
             if data[0]['formapago'] == "Mensual": 
                fechacuota = fechacuota + timedelta(days = 28)
                           
                diacuota = fechacuota.day
                
                diferenciadia = diainciocuota - diacuota

                if diferenciadia > 0:
                   fechacuota = fechacuota + timedelta(days = diferenciadia)
                else:
                   fechacuota = fechacuota - timedelta(days = diferenciadia)
                           
             if data[0]['formapago'] == "Quincenal": 
                fechacuota = fechacuota + timedelta(days = 14)
             
             if data[0]['formapago'] == "Anual": 
                fechacuota = fechacuota + timedelta(days = 365)
                             
                diacuota = fechacuota.day
                diferenciadia = diainciocuota - diacuota

                if diferenciadia > 0:
                   fechacuota = fechacuota + timedelta(days = diferenciadia)
                else:
                   fechacuota = fechacuota - timedelta(days = diferenciadia)
                                                
             if data[0]['formapago'] == "Semanal": 
                fechacuota = fechacuota + timedelta(days = 7)
                         
      
             c = 1
             interes = data[0]['financiamiento']*(data[0]['interes']/100)
             bcependiente = data[0]['financiamiento']
             for x in range(data[0]['plazo']):
         
                 sql = "insert into amort(nosolic,noprest,cedula,nocuota,cuota,capital,interes,balance,\
                 vpagcap,vpagint,vpagmora,status,pcuotas,user,fecha_crea,fecha_mod,fecha) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                 capital = data[0]['valorcuotas']
                 bcependiente = bcependiente  - (data[0]['valorcuotas'])

                 val = (data[0]['Num'],nopres1[0]['noprest'],data[0]['cedula'],c,data[0]['valorcuotas'],capital-interes,
                       interes,bcependiente,0.0,0.0,0.0," ",0,row['user'],datetime.now().date(),datetime.now().date(),fechacuota)
                 

                 if data[0]['formapago'] == "Diario": 
                    fechacuota = fechacuota + timedelta(days = 1)
                    
                 if data[0]['formapago'] == "Mensual": 
                    fechacuota = fechacuota + timedelta(days = 28)

                    diacuota = fechacuota.day
                    diferenciadia = diainciocuota - diacuota

                    if diferenciadia > 0:
                       fechacuota = fechacuota + timedelta(days = diferenciadia)
                    else:
                       fechacuota = fechacuota - timedelta(days = diferenciadia)
                           
                 if data[0]['formapago'] == "Quincenal": 
                    fechacuota = fechacuota + timedelta(days = 14)
                 
                 if data[0]['formapago'] == "Anual": 
                    fechacuota = fechacuota + timedelta(days = 365)
                    diacuota = fechacuota.day
                    diferenciadia = diainciocuota - diacuota

                    if diferenciadia > 0:
                       fechacuota = fechacuota + timedelta(days = diferenciadia)
                    else:
                       fechacuota = fechacuota - timedelta(days = diferenciadia) 
                               
                 if data[0]['formapago'] == "Semanal": 
                    fechacuota = fechacuota + timedelta(days = 7)
                         
                 c = c + 1
                 mycursor.execute(sql,val)
          
          if data[0]['tipofinanciamiento'] == "Insoluto":
             
             #grabar prestamos
             sql = "insert into prestamo(nosolic,fecha,periodos,nombres,apellidos,solicitado,plazo,\
             interes,mora,status,vpagcap,vpagint,vpagmora,norecibo,montoult,user,fecha_crea,fecha_mod,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
             
             val= (data[0]['Num'],data[0]['fecha_crea'],data[0]['plazo'],data[0]['nombres'],data[0]['apellidos'],\
                   data[0]['financiamiento'],data[0]['plazo'],data[0]['interes'],data[0]['mora']," ",0.0,0.0,0.0,0,0.0,\
                   row['user'],datetime.now().date(),datetime.now().date(),"A")
             mycursor.execute(sql,val)

             noprest = "select last_insert_id() as noprest"
             mycursor.execute(noprest)
             nopres1 = mycursor.fetchall()    
            

             porinteres = float(data[0]['interes'])/100
             vcuotas = float(data[0]['valorcuotas'])
             capitalflotante = 0.0
             interesflotante = 0.0
             
             vinteres = float(data[0]['financiamiento'])*porinteres
             
             capitalflotante = float(data[0]['financiamiento'])
             interesflotante = vinteres

             totalcapital = 0.0
             totalinteres = 0.0
             totaldeuda = 0.0

             #determinacion de fecha
             fechacuota = datetime.now().date()
             diainciocuota = fechacuota.day     
             
             if data[0]['formapago'] == "Diario": 
                fechacuota = fechacuota + timedelta(days = 1)
             
             if data[0]['formapago'] == "Mensual": 
                fechacuota = fechacuota + timedelta(days = 28)
                           
                diacuota = fechacuota.day
                diferenciadia = diainciocuota - diacuota

                if diferenciadia > 0:
                   fechacuota = fechacuota + timedelta(days = diferenciadia)
                else:
                   fechacuota = fechacuota - timedelta(days = diferenciadia)
                            
             if data[0]['formapago'] == "Quincenal": 
                fechacuota = fechacuota + timedelta(days = 14)
             
             if data[0]['formapago'] == "Anual": 
                fechacuota = fechacuota + timedelta(days = 365)
                             
                diacuota = fechacuota.day
                diferenciadia = diainciocuota - diacuota

                if diferenciadia > 0:
                   fechacuota = fechacuota + timedelta(days = diferenciadia)
                else:
                   fechacuota = fechacuota - timedelta(days = diferenciadia)
                                                
             if data[0]['formapago'] == "Semanal": 
                fechacuota = fechacuota + timedelta(days = 7)
             
             c = 1 
             for x in range(int(data[0]['plazo'])+1):
                 interesflotante = capitalflotante * porinteres
                 
                 totalcapital = totalcapital + (vcuotas-interesflotante)
                 totalinteres = totalinteres + interesflotante

                 sql = "insert into amort(nosolic,noprest,cedula,nocuota,cuota,capital,interes,balance,\
                 vpagcap,vpagint,vpagmora,status,pcuotas,user,fecha_crea,fecha_mod,fecha) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                 
                 val = (data[0]['Num'],nopres1[0]['noprest'],data[0]['cedula'],c,vcuotas,vcuotas-interesflotante,
                       interesflotante,capitalflotante-(vcuotas-interesflotante),0.0,0.0,0.0," ",0,row['user'],datetime.now().date(),datetime.now().date(),fechacuota)
                 
                 interesflotante = capitalflotante * porinteres
                 capitalflotante = capitalflotante - (vcuotas-interesflotante)
          
                 if data[0]['formapago'] == "Diario": 
                    fechacuota = fechacuota + timedelta(days = 1)
                    
                 if data[0]['formapago'] == "Mensual": 
                    fechacuota = fechacuota + timedelta(days = 28)

                    diacuota = fechacuota.day
                    diferenciadia = diainciocuota - diacuota

                    if diferenciadia > 0:
                       fechacuota = fechacuota + timedelta(days = diferenciadia)
                    else:
                       fechacuota = fechacuota - timedelta(days = diferenciadia)
                           
                 if data[0]['formapago'] == "Quincenal": 
                    fechacuota = fechacuota + timedelta(days = 14)
                 
                 if data[0]['formapago'] == "Anual": 
                    fechacuota = fechacuota + timedelta(days = 365)
                    diacuota = fechacuota.day
                    diferenciadia = diainciocuota - diacuota

                    if diferenciadia > 0:
                       fechacuota = fechacuota + timedelta(days = diferenciadia)
                    else:
                       fechacuota = fechacuota - timedelta(days = diferenciadia) 
                               
                 if data[0]['formapago'] == "Semanal": 
                    fechacuota = fechacuota + timedelta(days = 7)
                 
                 
                 mycursor.execute(sql,val)
                 c = c + 1 

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
       res = make_response(jsonify({"data":data}),200)
       return res; 
      
@aprobacionprestamos_api.route("/api/buscarsolicitud",methods=['POST','GET'])
def buscarsolicitud():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select id,nombres,apellidos,cedula,direccion,provincia,telefono,edad,celular,sexo,\
          ecivil,dependientes,sector,nacionalidad,nombrepila,email,comentario,format(financiamiento,2) as financiamiento,plazo,\
          formapago,interes,mora,cedulafiador,nombrefiador,telefonofiador,direccionfiador,tipofinanciamiento,\
          format(valorcuotas,2) as valorcuotas,format(deudatotal,2) as deudatotal from solicit where id = "+"'"+str(row['id'])+"'"
          mycursor.execute(sql)
          data = mycursor.fetchall()         
       
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
       res = make_response(jsonify({"data":data}),200)
       return res; 
      
 
@aprobacionprestamos_api.route("/api/modificardatossolicitud",methods=['POST','GET'])
def modificardatossolicitud():
    
    aerror = False
    salida = {}
    row = request.get_json()
    
    try:
       ###validar campos de entrada

       aerror = False

       if aerror == False: 
          if len(row['nombrespersonal']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True         
       if aerror == False: 
          if len(row['apellidos']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True

       if aerror == False: 
          if len(row['direccion']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True
       if aerror == False: 
          if len(row['provincia']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True
       if aerror == False: 
          if len(row['telefono']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True
       if aerror == False: 
          if len(row['celular']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True 
       if aerror == False: 
          if len(row['sector']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True
       if aerror == False: 
          if len(row['cedulafiador']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True
       if aerror == False: 
          if len(row['nombrefiador']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True
       if aerror == False: 
          if len(row['telefonofiador']) == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True
       if aerror == False: 
          if row['mora'] == 0:
            error = "Datos incompletos, por favor revisar" 
            aerror = True 
   
       if aerror == False:
          
          conectar = conectUserDatabase(row['parent'])
          mycursor = conectar.cursor(dictionary=True)
          sql = "update solicit set nombres = %s,apellidos = %s,direccion=%s,provincia=%s,telefono=%s,celular=%s,sector=%s,\
          cedulafiador=%s,nombrefiador=%s,telefonofiador=%s,mora=%s where id = "+"'"+str(row['id'])+"'"

          val = (row['nombrespersonal'],row['apellidos'],row['direccion'],row['provincia'],\
                 row['telefono'],row['celular'],row['sector'],row['cedulafiador'],\
                 row['nombrefiador'],row['telefonofiador'],row['mora']) 

          mycursor.execute(sql,val)
          data = mycursor.fetchall()         
       
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
       res = make_response(jsonify({"data":data}),200)
       return res; 
      
 