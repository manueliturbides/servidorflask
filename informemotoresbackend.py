from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 


informesmotoresbackend_api = Blueprint('informemotoresbackend_api',__name__)
modificasucursalbackend_api = Blueprint('modificasucursalbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

mysql = MySQL(app)

CORS(app)

mysql = MySQL(app)

@informesmotoresbackend_api.route("/api/informemotores",methods=['POST','GET'])
def informemotores():
    
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
          sql = "select concat(sucursal,'-',descripcion) as label  from sucursal "
          mycursor.execute(sql)
          misucursal = mycursor.fetchall()
          
          mycursor = conectar.cursor(dictionary=True)
          if len(row['status']) == 0:
             if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
                sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
             else:
                sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
          else:
              
              if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
                if row['status'][0].split("=")[0] == "I":
                   sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                   chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                   " and estado = 'I'"
                   
                if row['status'][0].split("=")[0] == "V":
                   sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                   chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                   " estado = 'V'"
                if row['status'][0].split("=")[0] == "N":
                   sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                   chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                   " and estado = ' '"
                if row['status'][0].split("=")[0] == "T":
                   sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                   chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
              
              else:
                 if row['status'][0].split("=")[0] == "I":
                    sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                    chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                    " and sucursal = "+"'"+str(row['sucursal'].split('-')[0])+"'"+" and estado = 'I'"

                 if row['status'][0].split("=")[0] == "V":
                    sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                    chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                    " and sucursal = "+"'"+str(row['sucursal'].split('-')[0])+"'"+" and estado = 'V'"  
              
                 if row['status'][0].split("=")[0] == "N":
                    sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                    chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                    " and sucursal = "+"'"+str(row['sucursal'].split('-')[0])+"'"+" and estado = ' '"  
              
                 if row['status'][0].split("=")[0] == "T":
                    sql = "select id,date_format(fecha,'%d-%m-%Y') as fecha,marca,modelo,colore,\
                    chasis,format(costo,2) as costo,format(precio,2) as precio,estado,condicion from producto where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                    " and sucursal = "+"'"+str(row['sucursal'].split('-')[0])+"'"  
             
          mycursor.execute(sql)
          mimotor = mycursor.fetchall()
          if mycursor.rowcount != 0:
             salida["motor"] = mimotor
             salida["sucursales"] = misucursal
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay motores registradas en las fechas seleccionadas o la sucursal elegida. Por favor revise"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@modificasucursalbackend_api.route("/api/modificasucursal",methods=['POST','GET'])
def modificasucursal():
    
    aerror = False
    salida = {}
    row = request.get_json()

    if aerror == False:
       if len(row['sucursalacambiar']) == 0:
          aerror = True
          error = "La sucursal a cambiar debe tener una sucursal valida asignada"
       else:
          try:
            conectar = mysql.connection
            mycursor = conectar.cursor(dictionary=True)
            sql = "select sucursal,descripcion from sucursal where sucursal = "+"'"+str(row['sucursalacambiar'])+"'"
            mycursor.execute(sql)
            missucursales = mycursor.fetchall()

            if mycursor.rowcount != 0:
               mycursor = conectar.cursor(dictionary=True)
               sql = "update producto set sucursal = "+"'"+str(row['sucursalacambiar'])+"'"+" where chasis = "+"'"+str(row['chasis'])+"'"      
               mycursor.execute(sql)
            
               conectar.commit()
               conectar.close()
          
               salida["ok"] = "Datos procesados correctamente"
               res = make_response(jsonify(salida),200)
               return res 
            else:
               aerror = True
               error = "La sucursal a cambiar no existe, por favor, revise"
                
            
          except Exception as e:
            aerror = True
            error = "Problemas para conectar la tabla "+str(e)        
          
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@modificasucursalbackend_api.route("/api/cobrosincautosfechas",methods=['POST','GET'])
def cobrosincautosfechas():
    
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
          sql = "select concat(sucursal,'-',descripcion) as label  from sucursal "
          mycursor.execute(sql)
          misucursal = mycursor.fetchall()
          
          mycursor = conectar.cursor(dictionary=True)
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             if len(row['estatus']) == 0:
                 sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,\
                 increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                 " where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
             else:
                 if row['estatus'] == "No Cobrado":
                    sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,"+\
                    "increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                    "where increg.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                    " and estado = ''"        
                 if row['estatus'] == "Cobrado":
                    sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,"+\
                    "increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                    "where increg.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                    " and estado = 'P'"        
                 if row['estatus'] == "Todos":
                    sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,"+\
                    "increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                    "where increg.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"        
                    
          else:
             if len(row['estatus']) == 0:
                sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,"+\
                " increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                " where increg.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                " and sucursal = "+"'"+str(row['sucursal'].split("-")[0])+"'"            
             else:
                if row['estatus'] == "No Cobrado":
                   sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,"+\
                   "increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                   " where increg.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                   " and increg.sucursal = "+"'"+str(row['sucursal'].split("-")[0])+"'"+" and estado = '' " 
                   
                if row['estatus'] == "Cobrado":
                   sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,"+\
                   "increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                   " where increg.fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                   " and sucursal = "+"'"+str(row['sucursal'].split("-")[0])+"'"+" and estado = 'P'"            
                
                if row['estatus'] == "Todos":
                   sql = "select increg.nuprest as id,date_format(increg.fecha,'%d-%m-%Y') as fecha,prestamo.nombres,prestamo.apellidos,"+\
                   "increg.cedula,increg.fechacobro,increg.incautador,increg.chasis from increg inner join prestamo on increg.nuprest = prestamo.noprest "+\
                   " where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
                   " and sucursal = "+"'"+str(row['sucursal'].split("-")[0])+"'"            
                
          mycursor.execute(sql)
          misincautos = mycursor.fetchall()
          if mycursor.rowcount != 0:
             salida["misincautos"] = misincautos
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay motores registradas en las fechas seleccionadas o la sucursal elegida. Por favor revise"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@modificasucursalbackend_api.route("/api/eliminarregistroincauto",methods=['POST','GET'])
def eliminarregistroincauto():
    
    aerror = False
    salida = {}
    row = request.get_json()

    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor()
          sql = "update producto set estado = 'V' where chasis = "+"'"+row['chasis']+"'"
          mycursor.execute(sql)
 
          mycursor1 = conectar.cursor()
          sql = "delete from increg where nuprest = "+"'"+str(row['noprest'])+"'"
          mycursor1.execute(sql)
 

          conectar.commit()
          conectar.close()
       
          salida["ok"] = "Datos modificados correctamente"
          res = make_response(jsonify(salida),200)
          return res 
   
      
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        

       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 


@modificasucursalbackend_api.route("/api/informecobrosmatriculas",methods=['POST','GET'])
def informecobrosmatriculas():
    
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
             sql = "select noprest as id,date_format(fecha,'%d-%m-%Y') as fecha1,nombres,apellidos,cedula,marca,modelo,colore,chasis,format(valor,2) as valor from pagomatri "+\
             " where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
                    
          else:
             sql = "select noprest as id,date_format(fecha,'%d-%m-%Y') as fecha1,nombres,apellidos,cedula,marca,modelo,colore,chasis,format(valor,2) from pagomatri "+\
             " where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
             " and sucursal = "+"'"+str(row['sucursal'].split("-")[0])+"'"            
                
          mycursor.execute(sql)
          mismatriculas = mycursor.fetchall()
          if mycursor.rowcount != 0:
             salida["matriculas"] = mismatriculas
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay pagos por matriculas registradas en las fechas seleccionadas o la sucursal elegida. Por favor revise"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@modificasucursalbackend_api.route("/api/eliminarcobrosmatriculas",methods=['POST','GET'])
def eliminarcobrosmatriculas():
    
    aerror = False
    salida = {}
    row = request.get_json()
   
    if aerror == False:
       try:
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          
          sql = "update  pagomatri set valor = 0 where noprest = "+"'"+str(row['noprest'])+"'"
                
          mycursor.execute(sql)
          salida["ok"] = "Pago de matricula eliminado correctamente"
          res = make_response(jsonify(salida),200)
          conectar.commit()
          conectar.close()
       
          return res 
          
          
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@modificasucursalbackend_api.route("/api/cobrosmatriculasporfechas",methods=['POST','GET'])
def cobrosmatriculasporfechas():
    
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
          
          mycursor = conectar.cursor(dictionary=True)
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select noprest as id,date_format(fecha,'%d-%m-%Y') as fecha1,nombres,apellidos,cedula,marca,modelo,colore,chasis,format(valor,2) as valor from pagomatri "+\
             " where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
                    
          else:
             sql = "select noprest as id,date_format(fecha,'%d-%m-%Y') as fecha1,nombres,apellidos,cedula,marca,modelo,colore,chasis,format(valor,2) from pagomatri "+\
             " where fecha between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
             " and sucursal = "+"'"+str(row['sucursal'].split("-")[0])+"'"            
                
          mycursor.execute(sql)
          mismatriculas = mycursor.fetchall()
          if mycursor.rowcount != 0:
             salida["matriculas"] = mismatriculas
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay pagos por matriculas registradas en las fechas seleccionadas o la sucursal elegida. Por favor revise"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 

@modificasucursalbackend_api.route("/api/informetraspaso",methods=['POST','GET'])
def informetraspaso():
    
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
          
          mycursor = conectar.cursor(dictionary=True)
          if len(row['sucursal']) == 0 or row['sucursal'] == None or row['sucursal'] == '':
             sql = "select noprest as id,date_format(fecha_crea,'%d-%m-%Y') as fecha1,concat(nombres,' ' ,apellidos) as nombres,cedula,chasis,marca,modelo,concat(tnombres,' ',tapellidos) as tnombres, tcedula from traspaso "+\
             " where fecha_crea between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"
                    
          else:
             sql = "select noprest as id,date_format(fecha_crea,'%d-%m-%Y') as fecha1,concat(nombres,' ' ,apellidos) as nombres,cedula,chasis,marca,modelo,concat(tnombres,' ',tapellidos) as tnombres, tcedula from traspaso "+\
             " where fecha_crea between "+"'"+row['fechadesde']+"' and "+"'"+row['fechahasta']+"'"+\
             " and sucursal = "+"'"+str(row['sucursal'].split("-")[0])+"'"            
                
          mycursor.execute(sql)
          mismatriculas = mycursor.fetchall()
          if mycursor.rowcount != 0:
             salida["matriculas"] = mismatriculas
             res = make_response(jsonify(salida),200)
             return res 
          else:
             aerror = True
             error = "No hay traspasos registradas en las fechas seleccionadas o la sucursal elegida. Por favor revise"
          conectar.close()
       
       except Exception as e:
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
