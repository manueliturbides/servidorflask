import json
from flask import Flask,send_file,url_for
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
from procconectar import conectUserDatabase
import pandas as pd
import googlemaps
import io

ingresosolicitudprestamo_api = Blueprint('ingresosolicitudprestamo_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)
CORS(app)
mysql = MySQL(app)


@ingresosolicitudprestamo_api.route("/api/getcities",methods=['POST','GET'])
def getcities():
    row = request.get_json()
    country = row["country"]
    df = pd.read_csv("Herramientas/worldcities.csv")
    
    matching_cities = df[df['country'].str.lower() == country.lower()]['city_ascii'].tolist()
   
    return jsonify({'data':matching_cities})

@ingresosolicitudprestamo_api.route('/ftuser/<_id>/<num>')
def ftuser(_id,num):
   connectionUser = conectUserDatabase(_id)
   mycursor = connectionUser.cursor(dictionary=True)
   
   sqlCompany = "select * from solicit where id = "+num
   mycursor.execute(sqlCompany)
   solicit = mycursor.fetchall()
 
   response =  send_file(io.BytesIO(solicit[0]["foto"]),mimetype="image/*")

   return response


@ingresosolicitudprestamo_api.route('/api/modificarfoto',methods=['POST','GET'])
def modificarfoto():
    
    try:
      aerror = False
      salida = {}

      try:
        imagefile = request.files['image']
        bin_file = imagefile.read()
      except Exception as e:
        bin_file = "" 
   
      jsonData = request.form["json"]
      row = json.loads(jsonData)

      connectionUser = conectUserDatabase(row['parent'])
      mycursor = connectionUser.cursor(dictionary=True)
   
      sqlCompany = "update solicit set foto = %s where id = "+str(row['id'])
      val = (bin_file,)
      mycursor.execute(sqlCompany,val)
      connectionUser.commit()

    except Exception as e:
      print(e)
      aerror = True
      error = "No pudo modificar la foto "+str(e) 

    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
         res = make_response(jsonify({"ok": "ok"}),200)
         return res; 
    
     

@ingresosolicitudprestamo_api.route("/api/ingresarsolicitudprestamo",methods=['POST','GET'])
def ingresarsolicitudprestamo():
    
    aerror = False
    salida = {}

    try:
      imagefile = request.files['image']
      bin_file = imagefile.read()
    except Exception as e:
      bin_file = "" 
    
    
    jsonData = request.form["json"]

    row = json.loads(jsonData)
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
       
       gmaps_key = googlemaps.Client(key="AIzaSyAvgrqvE_JpqV_FzhrYsi6uhiOjgo8J95M")
       add_1 = row["direccion"]+","+row["provincia"]+" ,"+row["pais"]
       g = gmaps_key.geocode(add_1)
       latitud = g[0]["geometry"]["location"]["lat"]
       longitud = g[0]["geometry"]["location"]["lng"]
       

       if aerror == False:
          conectar = conectUserDatabase(row["parent"])
          mycursor = conectar.cursor(dictionary=True)
          sql = "insert into solicit(cedula,nombres,apellidos,provincia,direccion,\
          telefono,sector,nacionalidad,nombrepila,email,\
          comentario,financiamiento,plazo,formapago,interes,\
          mora,cedulafiador,nombrefiador,telefonofiador,direccionfiador,\
          tipofinanciamiento,valorcuotas,deudatotal,edad,celular,\
          sexo,ecivil,dependientes,user,fecha_crea,fecha_mod,aprobado,longitud,latitud,foto) values(%s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,\
          %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

          val = (row['cedula'],row['nombres'],row['apellidos'],row['provincia'],row['direccion'],\
                 row['telefono'],row['sector'],row['nacionalidad'],row['nombrepila'],row['email'],\
                 row['comentario'],float(row['financiamiento']),int(row['plazo']),row['formapago'],row['interes'],\
                 row['mora'],row['cedulafiador'],row['nombrefiador'],row['telefonofiador'],row['direccionfiador'],\
                 row['tiposolicitud'],float(row['valorcuotas']),float(row['deudatotal']),row['edad'],row['celular'],\
                 row['sexo'],row['ecivil'],row['dependientes'],row['user'],datetime.now().date(),datetime.now().date(),"N",latitud,longitud,bin_file)
          mycursor.execute(sql,val)

  
          conectar.commit()

          sql = "SELECT id FROM solicit order by id desc limit 1"
          mycursor.execute(sql)
          ultSolicit = mycursor.fetchone()
          url = url_for("ingresosolicitudprestamo_api.ftuser", _id=row["parent"],num=ultSolicit["id"])
          print(url)


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
      
 