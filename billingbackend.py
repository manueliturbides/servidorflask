import pandas as pd
from flask import Flask
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
import requests
import base64
import uuid
import json
from flask import make_response
from datetime import datetime
from flask_mysql_connector import MySQL
import configuracionservidor 
import calendar
from procconectar import conectUserDatabase
from procconectar import conectUserDatabaseVendedor
from procconectar import conectServerDatabase
import time


billingbackend_api = Blueprint('billinggbackend_api',__name__)

app = Flask(__name__)

app.config['MYSQL_USER'] = configuracionservidor.puser
app.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
app.config['MYSQL_HOST'] = configuracionservidor.phost
app.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

PAYPAL_CLIENT_ID = "Ac7Xe72157GerO-EfF2GpQuklSR2aQLIU66y3debvQZQMXXAMaHu69VFMwgn_a6db4zd1ud8-lSjnjc1"
PAYPAL_CLIENT_SECRET = "EFpvcnm5Z6-9CDXBNJ9d9AwGqiYStObWrmD2JVLMy9JDP86rROjqhtbtWXCE4POdCOIgKu4Kp9jHfd_C"
PLAN_ID = "P-8LJ579675P663525BMWZFF5Y"

base = "https://api-m.sandbox.paypal.com"

CORS(app,origins="http://localhost:3000")
mysql = MySQL(app)



@billingbackend_api.route("/api/billingbackend_promcodecheck",methods=['POST','GET'])
def billingbackend_promcodecheck():
    aerror = False
    error = {}
    salida = {}
    row = request.get_json()
    
    if aerror == False:
       try:
 
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from Vendedores where promcode = "+"'"+row['promcode']+"'"
          mycursor.execute(sql)
          vendedor = mycursor.fetchall()

          if len(vendedor) == 0 :
             aerror = True 
             error = "not exist"  

       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"sucess":"sucess"}),200)
       return res

@billingbackend_api.route("/api/billingbackend_unsuscribe",methods=['POST','GET'])
def billingbackend_unsuscribe():
    aerror = False
    error = {}
    salida = {}
    row = request.get_json()
    suscriptionid = row["suscriptionid"]
    promcode = row["promCode"]


    if aerror == False:
       try:
         if promcode != "":  
            conectar = mysql.connection
            mycursor = conectar.cursor(dictionary=True)
            sql = "select id from Vendedores where promcode = "+"'"+promcode+"'"
            mycursor.execute(sql)
            vendedor = mycursor.fetchone()

            connectionVendedor = conectUserDatabaseVendedor(vendedor["id"])
            mycursor = connectionVendedor.cursor(dictionary=True)
            sql = "delete from clientes where id = "+"'"+row["parent"]+"'"
            mycursor.execute(sql)

            date = datetime.today()         
            sql = "select * from facturas WHERE MONTH(fecha) = '"+str(date.month)+"' AND YEAR(fecha) = '"+str(date.year)+"'"
            mycursor.execute(sql)
            factura = mycursor.fetchone()

            if factura != None:
               sql = "update facturas set numSuscrip=%s where id=%s"
               val = (factura["numSuscrip"]-1,factura["id"])
               mycursor.execute(sql,val)
               connectionVendedor.commit()

         conectar = mysql.connection
         mycursor = conectar.cursor(dictionary=True)
         sql = "delete from users where parent = "+"'"+row["parent"]+"'"
         mycursor.execute(sql)
         conectar.commit()

         
         connectionUser = conectServerDatabase() 
         mycursor = connectionUser.cursor()
         sql = "drop database if exists "+row["parent"]
         mycursor.execute(sql)

         
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 
    if aerror == False:
       res = make_response(jsonify({"sucess":"sucess"}),200)
       return res



@billingbackend_api.route("/api/billingbackend_getdatabilling",methods=['POST','GET'])
def billingbackend_getdatabilling():
    aerror = False
    error = {}
    salida = {}
    row = request.get_json()
    
    if aerror == False:
       try:
 
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "select * from facturas order by id desc limit 1"
          mycursor.execute(sql)
          ultFactura = mycursor.fetchall()
          salida["factura"] = ultFactura

          if len(ultFactura) == 0:
            aerror=True
            error="error"
          else:   
            res = make_response(jsonify(salida),200)
            return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 

@billingbackend_api.route("/api/billingbackend_nuevafactura",methods=['POST','GET'])
def billingbackend_nuevafactura():
    aerror = False
    error = {}
    row = request.get_json()
    
    if aerror == False:
       try:
          print(row)
          connectionUser = conectUserDatabase(row["parent"])
          mycursor = connectionUser.cursor(dictionary=True)
          sql = "insert into facturas(plan,total,promocode,suscriptionid,fecha) values(%s,%s,%s,%s,%s)"
          date = datetime.today()
          val = (str(row["plan"]),row["total"],row["promcode"],row["suscriptionid"],date)
          mycursor.execute(sql,val)
          connectionUser.commit()

          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)
          sql = "select * from Vendedores where promcode = "+"'"+row['promcode']+"'"
          mycursor.execute(sql)
          vendedor = mycursor.fetchone()
          print(vendedor)

          if vendedor != None:
            connectionVendedor = conectUserDatabaseVendedor(vendedor["id"])
            mycursor = connectionVendedor.cursor(dictionary=True)     
            sql = "SELECT * FROM clientes WHERE id = "+"'"+row['id']+"'"
            mycursor.execute(sql)
            cliente = mycursor.fetchone()

            if cliente == None:
               print("cliente "+str(cliente))
               sql = "insert into clientes(id,email,producto,fecha) values(%s,%s,%s,%s)"
               date = datetime.today()
               val = (row["id"],row["email"],"PrestaQuiK",date)
               mycursor.execute(sql,val)
               connectionVendedor.commit()
             
               sql = "select * from facturas order by id desc limit 1"
               mycursor.execute(sql)
               factura = mycursor.fetchone()

               if factura["fecha"].year == date.year and factura["fecha"].month == date.month:               
                 sql = "update facturas set numSuscrip=%s where id=%s"
                 val = (factura["numSuscrip"]+1,factura["id"])
                 mycursor.execute(sql,val)
                 connectionVendedor.commit()
               else:
                  sql = "SELECT COUNT(*) FROM clientes"
                  mycursor.execute(sql)
                  numclient = mycursor.fetchall()[-1][-1]

                  sql = "insert into facturas(fecha,numSuscrip,retired) values(%s,%s,%s)"
                  date = datetime.today()
                  val = (date,numclient+1,"false")          
                  mycursor.execute(sql,val)
                  connectionUser.commit()


             

          res = make_response(jsonify(row),200)
          return res
       
       except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 


def handle_response(response):
    try:
        jsonResponse = response.json()
        return {
            "jsonResponse": jsonResponse,
            "httpStatusCode": response.status_code,
        }
    except Exception as err:
        errorMessage = response.text
        raise Exception(errorMessage)

def generate_access_token():
    try:
        if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
            raise Exception("MISSING_API_CREDENTIALS")
        
        auth = base64.b64encode(f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}".encode()).decode("utf-8")
        response = requests.post(f"{base}/v1/oauth2/token", data="grant_type=client_credentials", headers={"Authorization": f"Basic {auth}"})
        
        data = response.json()
        return data["access_token"]
    except Exception as error:
        print("Failed to generate Access Token:", error)


@billingbackend_api.route("/api/paypal/create-plans",methods=['POST','GET'])
def createplans():
    aerror = False
    error = {}
    access_token = generate_access_token()
    if aerror == False:
        try:
          emprendedor = {"name":"emprendedor","price":"20"}
          emprendedordescuento = {"name":"emprendedordescuento","price":"18.99"}
          mypimes = {"name":"mipymes","price":"35"}
          mypimesdescuento = {"name":"mipymesdescuento","price":"33.25"}
          pro = {"name":"pro","price":"70"}
          prodescuento = {"name":"prodescuento","price":"66.5"}
          plus = {"name":"plus","price":"105"}
          plusdescuento = {"name":"plusdescuento","price":"100"}

          planes = [emprendedor,emprendedordescuento,mypimes,mypimesdescuento,pro,prodescuento,plus,plusdescuento]
          conectar = mysql.connection
          mycursor = conectar.cursor(dictionary=True)

          url = "https://api-m.sandbox.paypal.com/v1/catalogs/products"
          paypal_request_id = str(uuid.uuid4())
          headers = {
               "Content-Type": "application/json",
               "Authorization": f"Bearer {access_token}",
               "PayPal-Request-Id": paypal_request_id,}
            
          data = {
               "name":"PrestaQuiK",
               "description": "Suscripcion de PrestaQuiK",
               "type": "SERVICE",
               "category": "SOFTWARE"
               }

          response = requests.post(url, json=data, headers=headers)
          jsonfinal = json.loads(json.dumps(response.json()))
          
          print(jsonfinal)
          idproduct = jsonfinal["id"]

          for x in planes:  
            jsonplan = json.loads(json.dumps(x))
            
            
            
            url = "https://api-m.sandbox.paypal.com/v1/billing/plans"
            access_token = generate_access_token()
            headers = {
               "Accept": "application/json",
               "Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json",
               "PayPal-Request-Id": str(uuid.uuid4()),}

            data = {
               "product_id": idproduct,
               "name": jsonplan["name"],
               "description": jsonplan["name"],
               "billing_cycles": [
                 {
                  "frequency": {
                  "interval_unit": "MONTH",
                  "interval_count": 1
                  },
                 "tenure_type": "REGULAR",
                 "sequence": 1,
                "total_cycles": 12,
                 "pricing_scheme": {
                 "fixed_price": {
                    "value": jsonplan["price"],
                    "currency_code": "USD"
                    }
                  }
                 }
               ],
               "payment_preferences": {
               "auto_bill_outstanding": True,
               "setup_fee": {
                  "value": "0",
                  "currency_code": "USD"
               },
               "setup_fee_failure_action": "CONTINUE",
               "payment_failure_threshold": 3
               },
              "taxes": {
                  "percentage": "0",
                  "inclusive": False
               }
            }

            response = requests.post(url, json=data, headers=headers, verify=False) 
            jsonfinal = json.loads(json.dumps(response.json()))


            sql = "insert into Planes (name,id,product_id) values(%s,%s,%s)"
            val = (jsonfinal["name"],jsonfinal["id"],jsonfinal["product_id"])
            mycursor.execute(sql,val)
            conectar.commit()            


          return "success"
        except Exception as error:
            print(error)
            return jsonify({"error": "Failed to create order."}, 500)
       
    if aerror == True:
       res = make_response(jsonify( error),400)
       return res; 


@billingbackend_api.route("/api/paypal/updatesuscription",methods=['POST','GET'])
def updatesuscription():
   row = request.get_json()
   plan = row["plan"]
   suscriptionid = row["suscriptionid"]

   url = f"{base}/v1/billing/subscriptions/{suscriptionid}/revise"
   access_token = generate_access_token()
   headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
   }

   conectar = mysql.connection
   mycursor = conectar.cursor(dictionary=True)
   sql = "select * from planes where name = "+"'"+plan+"'"
   mycursor.execute(sql)
   misplanes = mycursor.fetchall()
   data = {
    "plan_id": misplanes[0]["id"]
   }

   response = requests.post(url, headers=headers, json=data)

   print("Response Code:", response.status_code)
   print("Response Body:", response.text)
   result = handle_response(response=response)
   return jsonify(result["jsonResponse"])

@billingbackend_api.route("/api/paypal/create-subscription",methods=['POST','GET'])
def createsubscription():
    url = f"{base}/v1/billing/subscriptions"
    access_token = generate_access_token()
    user_action="SUBSCRIBE_NOW"
    row = request.get_json()
    
    print(row["name"])
    conectar = mysql.connection
    mycursor = conectar.cursor(dictionary=True)
    sql = "select * from planes where name = "+"'"+row['name']+"'"
    mycursor.execute(sql)
    misplanes = mycursor.fetchall()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Prefer": "return=representation",
    }

    payload = {
        "plan_id": misplanes[0]["id"],
        "application_context": {
            "user_action": user_action,
        },
    }

    response = requests.post(url, json=payload, headers=headers)
    result = handle_response(response=response)
    return jsonify(result["jsonResponse"]), result["httpStatusCode"]


 
@billingbackend_api.route("/api/limitedeclientes",methods=['POST','GET'])
def limitedeclientes():
    
    aerror = False
    salida = {}
    row = request.get_json()
    try:
       aerror = False
       
       if aerror == False:
          conectar = conectUserDatabase(row["parent"])
          mycursor = conectar.cursor(dictionary=True)
          sql = "select sum(deudatotal) as totalvalorprestamo,count(id) as cantidaddeprestamo from solicit where aprobado = 'S' group by aprobado"
          mycursor.execute(sql)
          data = mycursor.fetchall()
          conectar.close()
          print(sql)
          print(data) 
    except Exception as e:
          print(e)
          aerror = True
          error = "Problemas para conectar la tabla "+str(e)        
       
    if aerror == True:
       res = make_response(jsonify({"Error": error}),400)
       return res; 
    if aerror == False:
       return jsonify({'data':data})
       #res = make_response(jsonify({"data":data}),200)
       #return res; 
      