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


ingresosolicitudprestamo_api = Blueprint('ingresosolicitudprestamo_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)

@ingresosolicitudprestamo_api.route("/api/ingresarsolicitudprestamo",methods=['POST','GET'])
def ingresarsolicitudprestamo():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       ###validar campos de entrada

       aerror = False

       #row['user'] = ""

       if aerror == False:
          if len(row['cedula']) == 0 or len(row['cedula']) != 11:
             aerror = True
             error = "La cedula no puede estar en blanco o la longitud es incorrecta"
              
       if aerror == False:
          if (len(row['nombres']) == 0):
             aerror = True
             error = "Los nombres no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['apellidos']) == 0):
             aerror = True
             error = "Los apellidos no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['provincia']) == 0):
             aerror = True
             error = "Los provincia no puede estar en blanco "
       
       if aerror == False:
          if (len(row['direccion']) == 0):
             aerror = True
             error = "La direccion no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['telefono']) == 0):
             aerror = True
             error = "Los telefonos no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['edad']) == 0):
             aerror = True
             error = "La edad no puede estar en blanco "
       
       if aerror == False:
          if (len(row['celular']) == 0):
             aerror = True
             error = "El celular no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['sexo']) == 0):
             aerror = True
             error = "El genero no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['telefono']) == 0):
             aerror = True
             error = "Los telefonos no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['ecivil']) == 0):
             aerror = True
             error = "El estado civil no puede estar en blanco "
       
       if aerror == False:
          if (len(row['dependientes']) == 0):
             aerror = True
             error = "Los dependientes no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['telefono']) == 0):
             aerror = True
             error = "Los telefonos no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['sector']) == 0):
             aerror = True
             error = "El sector donde reside pueden estar en blanco "
       
       if aerror == False:
          if (len(row['nacionalidad']) == 0):
             aerror = True
             error = "La nacionalidad no puede estar en blanco "
       
       if aerror == False:
          if (len(row['nombrepila']) == 0):
             aerror = True
             error = "El nombre de pila no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['email']) == 0):
             aerror = True
             error = "El email no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['financiamiento']) == 0):
             aerror = True
             error = "El financiamiento no puede estar en blanco "
       
       if aerror == False:
          if (len(row['plazo']) == 0):
             aerror = True
             error = "El plazo no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['formapago']) == 0):
             aerror = True
             error = "La forma de pago no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['interes']) == 0):
             aerror = True
             error = "El interes no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['telefono']) == 0):
             aerror = True
             error = "Los telefonos no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['mora']) == 0):
             aerror = True
             error = "La mora no puede estar en blanco "
       
       if aerror == False:
          if (len(row['cedulafiador']) == 0):
             aerror = True
             error = "La cedula del fiador no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['nombrefiador']) == 0):
             aerror = True
             error = "El nombre del fiador no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['telefonofiador']) == 0):
             aerror = True
             error = "El telefono del fiador no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['direccionfiador']) == 0):
             aerror = True
             error = "La direccion del fiador no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['tiposolicitud']) == 0):
             aerror = True
             error = "El tipo de financiamiento no pueden estar en blanco "
       
       if aerror == False:
          if (len(row['cedulafiador']) == 0):
             aerror = True
             error = "La cedula del fiador no pueden estar en blanco "
       
       

       if aerror == False:
          conectar = conectUserDatabase(row["parent"])
          mycursor = conectar.cursor()
          sql = "insert into solicit(cedula,nombres,apellidos,provincia,direccion,\
          telefono,sector,nacionalidad,nombrepila,email,\
          comentario,financiamiento,plazo,formapago,interes,\
          mora,cedulafiador,nombrefiador,telefonofiador,direccionfiador,\
          tipofinanciamiento,valorcuotas,deudatotal,edad,celular,\
          sexo,ecivil,dependientes,user,fecha_crea,fecha_mod,aprobado) values(%s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,%s,%s)"

          val = (row['cedula'],row['nombres'],row['apellidos'],row['provincia'],row['direccion'],\
                 row['telefono'],row['sector'],row['nacionalidad'],row['nombrepila'],row['email'],\
                 row['comentario'],float(row['financiamiento']),int(row['plazo']),row['formapago'],row['interes'],\
                 row['mora'],row['cedulafiador'],row['nombrefiador'],row['telefonofiador'],row['direccionfiador'],\
                 row['tiposolicitud'],float(row['valorcuotas']),float(row['deudatotal']),row['edad'],row['celular'],\
                 row['sexo'],row['ecivil'],row['dependientes'],row['user'],datetime.now().date(),datetime.now().date(),"N")
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
       res = make_response(jsonify({"mensajeok": "Prestamos cancelado correctamente"}),200)
       return res; 
      
 