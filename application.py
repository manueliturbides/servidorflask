from flask import Flask
from flask_cors import CORS
from flask_mysql_connector import MySQL
from flask import jsonify
from flask import request
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

import configuracionservidor 

application = Flask(__name__,static_url_path='',static_folder='build',template_folder='build')

application.config['MYSQL_USER'] = configuracionservidor.user
application.config['MYSQL_DATABASE'] = configuracionservidor.database
application.config['MYSQL_HOST'] = configuracionservidor.host
application.config['MYSQL_PASSWORD'] = configuracionservidor.password

pruebabackend_api = Blueprint('pruebabackend_api',__name__)

mysql = MySQL(application)

CORS(application)

application.register_blueprint(loginbackend_api)
application.register_blueprint(usersconfigbackend_api)
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

@application.route("/")
def servirpaginaestatica():
    return render_template("index.html")

@application.errorhandler(404)
def not_found(e):
    return "render_template('index.html')"

if __name__ == "__main__":
    application.debug = True
    application.run()
#application.run()