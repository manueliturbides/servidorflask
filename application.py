from countryinfo import CountryInfo
from flask import Flask
from flask_cors import CORS
from flask_mysql_connector import MySQL
from flask import jsonify
from flask import request
from flask import send_file
import smtplib
import random
from email.message import EmailMessage
from flask import send_file,url_for,redirect,flash
from flask import make_response
from flask import Blueprint,render_template
from datetime import datetime
from loginbackend import loginbackend_api
from restaurarcancelarprestamobackend import restaurarcancelarprestamobackend_api
from usersconfigbackend import usersconfigbackend_api
from solicitudprestamo import ingresosolicitudprestamo_api
from aprobacionprestamos import aprobacionprestamos_api
from pagosprestamos import pagosprestamos_api
from consultaprestamos import consultaprestamos_api
from consultarpagos import consultarpagos_api
from cancelarpagos import cancelarpagos_api
from cancelarrestaurarprestamo import cancelarrestaurarprestamo_api
from consultarsolicitud import consultasolicitud_api
from descuentoprestamos import descuentoprestamos_api
from interesescobradosperiodos import interesescobradosperiodos_api
from balanceprestamoclientes import balanceprestamoscliente_api
from balancecuotasantiguedad import balancecuotasantiguedad_api
from historialdepagos import hitorialdepagos_api
from historicodepagos import historicodepagos_api
from auditoriaderecibos import auditoriaderecibos_api
from cuadredecaja import cuadredecaja_api
from usersconfigbackend import usersconfigbackend_api
from billingbackend import billingbackend_api
from vendedoresbackend import vendedoresbackend_api
from supportbackend import supportbackend_api
from procconectar import conectUserDatabase
import googlemaps
from rutas import rutas_api
from dashboard import dashboard_api

import configuracionservidor 

application = Flask(__name__,static_url_path='',static_folder='build',template_folder='build')

application.config['MYSQL_USER'] = configuracionservidor.puser
application.config['MYSQL_DATABASE'] = configuracionservidor.pdatabase
application.config['MYSQL_HOST'] = configuracionservidor.phost
application.config['MYSQL_PASSWORD'] = configuracionservidor.ppassword

pruebabackend_api = Blueprint('pruebabackend_api',__name__)

mysql = MySQL(application)

CORS(application)

application.register_blueprint(loginbackend_api)
application.register_blueprint(ingresosolicitudprestamo_api)
application.register_blueprint(aprobacionprestamos_api)
application.register_blueprint(pagosprestamos_api)
application.register_blueprint(consultaprestamos_api)
application.register_blueprint(consultarpagos_api)
application.register_blueprint(cancelarpagos_api)
application.register_blueprint(cancelarrestaurarprestamo_api)
application.register_blueprint(consultasolicitud_api)
application.register_blueprint(descuentoprestamos_api)
application.register_blueprint(interesescobradosperiodos_api)
application.register_blueprint(balanceprestamoscliente_api)
application.register_blueprint(balancecuotasantiguedad_api)
application.register_blueprint(hitorialdepagos_api)
application.register_blueprint(historicodepagos_api)
application.register_blueprint(auditoriaderecibos_api)
application.register_blueprint(cuadredecaja_api)
application.register_blueprint(usersconfigbackend_api)
application.register_blueprint(billingbackend_api)
application.register_blueprint(vendedoresbackend_api)
application.register_blueprint(supportbackend_api)
application.register_blueprint(rutas_api)
application.register_blueprint(dashboard_api)

@application.route("/")
def servirpaginaestatica():
    return render_template("index.html")

@application.errorhandler(404)
def not_found(e):
    return render_template('index.html')

@application.route('/geocode',methods=['POST','GET'])
def geocode():
  gmaps_key = googlemaps.Client(key="AIzaSyAvgrqvE_JpqV_FzhrYsi6uhiOjgo8J95M")
  add_1 = "guayacanes, republica dominicana"
  g = gmaps_key.geocode(add_1)
  lat = g[0]["geometry"]["location"]["lat"]
  long = g[0]["geometry"]["location"]["lng"]
  print('Latitude: '+str(lat)+', Longitude: '+str(long))
  return "success"

@application.route('/parents',methods=['POST','GET'])
def getparents():
    conectar = mysql.connection
    mycursor = conectar.cursor(dictionary=True)
    sql = "SELECT DISTINCT parent FROM users;"
    mycursor.execute(sql)
    misusers = mycursor.fetchall()

    for x in misusers:
      conectar = conectUserDatabase(x["parent"])
      mycursor = conectar.cursor(dictionary=True)
      sql = "select solicit.email as email, fecha as fechavenc, \
          format(amort.capital+amort.interes-amort.vpagcap-amort.vpagint,2) as balance from amort \
          inner join solicit on solicit.id = amort.nosolic \
          where datediff(fecha,now()) = 1"
      mycursor.execute(sql)
      data = mycursor.fetchall()


      sql = "select * from company"
      mycursor.execute(sql)
      dataComp = mycursor.fetchall()
      nameCompany = dataComp[0]["nombre"]
      
      if len(nameCompany)==0:
        nameCompany = "Recordatorio de Pago"         
      

      for y in data:
        email = y["email"]
        texto = "texto" #row["texto"]
  
        msg = EmailMessage()
        msg['Subject'] = nameCompany
        msg['From'] = "support@suitorbit.com"
        msg['To'] = email
        msg.set_content('''
                    <!DOCTYPE html>
                      <html>
                        <body style="background-color: #eee; display: flex; align-items: center; justify-content: center;">
                          <div style=" background-color: white; border-radius: 10px; border-width: 10px; width: 450px; height: 340px; margin:30px">
                            <div style="background-color:#f56016;margin-top: -20px; height: 110px; border-top-left-radius: 10px;border-top-right-radius: 10px; border-width: 10px; display:flex; align-items: center; justify-content: center;">
                              <h2 style="color: white; font-family:sans-serif">Recordatorio de pago</h2>
                            </div>
                            <div style="width:450px; background-color: white; ">
                              <div style="text-align: center; margin-left: 15px; margin-right:15px; font-family: Nunito; font-size: 18px;">
                                <p >Hola!</p>
                                <p>Te recordamos que debes hacer el pago de tu prestamo</p>
                                <strong>'''+y["balance"]+'''</strong> 
                                <p>Gracias</p>
                              </div>
                            </div>
                            <div style="background-color:black;margin-top: 55px; height: 20px; border-bottom-left-radius: 10px;border-bottom-right-radius: 10px; border-width: 10px;"></div>
                          </div>
                        </body>
                      </html>''', subtype='html')

        try:
          server = smtplib.SMTP_SSL('smtp.mail.us-east-1.awsapps.com', 465)
          server.ehlo()
          server.login('support@suitorbit.com', 'Mr00100267590')
          text = msg.as_string()
          server.sendmail("support@suitorbit.com", email, text)
          server.quit()
        except Exception as e:
          print("SMTP server connection error sksk")
      
      conectar.close() 


    return "matching_cities"
    

@application.route('/contactprosecom',methods=['POST','GET'])
def contactprosecom():
    codigo = random.randint(0,999999) 
    row = request.get_json()
        
    email = row["email"]
    texto = row["texto"]
   


    msg = EmailMessage()
    msg['Subject'] = 'SuitOrbit Contact'
    msg['From'] = "support@suitorbit.com"
    msg['To'] = email
    msg.set_content('''
                    <!DOCTYPE html>
                      <html>
                        <body style="background-color: #eee; display: flex; align-items: center; justify-content: center;">
                          <div style=" background-color: white; border-radius: 10px; border-width: 10px; width: 530px; height: 340px; margin:30px">
                            <div style="background-color:#f56016;margin-top: -20px; height: 110px; border-top-left-radius: 10px;border-top-right-radius: 10px; border-width: 10px; display:flex; align-items: center; justify-content: center;">
                              <h2 style="color: white; font-family:sans-serif">PrestaQuik</h2>
                            </div>

                            <div style="width:530px; background-color: white; ">
                              <div style="text-align: center; margin-left: 15px; margin-right:15px; font-family: Nunito; font-size: 18px;">
                                <p >Hola!</p>
                                <p>Estaremos respondiendo lo más rápido posible</p>
                                <p>Gracias,  equipo PrestaQuik</p>
                              </div>
                            </div>
                            <div style="background-color:black;margin-top: 55px; height: 20px; border-bottom-left-radius: 10px;border-bottom-right-radius: 10px; border-width: 10px;"></div>
                          </div>
                        </body>
                      </html>''', subtype='html')

    try:
      server = smtplib.SMTP_SSL('smtp.mail.us-east-1.awsapps.com', 465)
      server.ehlo()
      server.login('support@suitorbit.com', 'Mr00100267590')
      text = msg.as_string()
      server.sendmail("support@suitorbit.com", email, text)
      server.quit()
      print('Email sent to %s' "email_recipient")
    except Exception as e:
      print(e)
      print("SMTP server connection error sksk")

    
    msg = EmailMessage()
    msg['Subject'] = 'SuitOrbit Contact'
    msg['From'] = "support@suitorbit.com"
    msg['To'] = "support@suitorbit.com"
    msg.set_content('''
                    <!DOCTYPE html>
                      <html>
                        <body style="background-color: white; ">
                             '''+texto+'''
                             '''+email+'''

                       </body>
                      </html>''', subtype='html')

    try:
      server = smtplib.SMTP_SSL('smtp.mail.us-east-1.awsapps.com', 465)
      server.ehlo()
      server.login('support@suitorbit.com', 'Mr00100267590')
      text = msg.as_string()
      server.sendmail("support@suitorbit.com", "support@suitorbit.com", text)
      server.quit()
      print('Email sent to %s' "email_recipient")
    except Exception as e:
      print(e)
      print("SMTP server connection error")
    return str(codigo)

@application.route('/contrato',methods=['POST','GET'])
def contrato():
	  return send_file('Plantillas/contratofinal1.docx')
    
if __name__ == "__main__":
    application.debug = True
    application.run()
#application.run()