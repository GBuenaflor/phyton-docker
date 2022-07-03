# Python Flask build_spec.yaml 
# POC Develop By GB Buenaflor and isRAEL Casisdsid
# OKE , MySQL ,Terraform ,DevOPS

#from flask import Flask
#app = Flask(__name__)

#count = 0

#@app.route('/')
#def index():
#    global count
#    count += 1
#    return 'Python with Flask Website - OKE,MySQL,Terraform,DevOPS. GBuenaflor/iSRAel :     ' + str(count) 

#if __name__ == '__main__':
#    app.run(host='0.0.0.0')

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import logging
from flask import Flask
from flask_talisman import Talisman
from flask_sslify import SSLify
import os

# font_path = os.getcwd() +'/.fonts/'

app = dash.Dash(__name__, external_stylesheets=[
                "assets/bootstrap.css"], external_scripts=['https://kit.fontawesome.com/0656940dab.js'],)

#server = app.server
server = '0.0.0.0'

 # Talisman(server) not working
 # sslify = SSLify(server)

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.title = 'HRDO PUSO System'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

