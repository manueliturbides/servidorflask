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

@application.route("/")
def servirpaginaestatica():
    return render_template("index.html")

@application.errorhandler(404)
def not_found(e):
    return render_template('index.html')

if __name__ == "__main__":
    application.debug = True
    application.run()
#application.run()