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

server = app.server
# Talisman(server) not working
#sslify = SSLify(server)

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.title = 'HRDO PUSO System'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# import logging
# from flask import Flask
# from flask_talisman import Talisman
# from flask_sslify import SSLify
#
# app = dash.Dash(__name__, external_stylesheets=[
#                 "assets/bootstrap.css"], external_scripts=['https://kit.fontawesome.com/0656940dab.js'])
#
# app.config.suppress_callback_exceptions = True
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
#
# SELF = "'self'"
#
# csp = {
#     'default-src': ['\'self\'',
#                     'https://www.googleapis.com/auth/userinfo.email',
#                     'https://www.googleapis.com/auth/userinfo.profile',
#                     'https://accounts.google.com/o/oauth2/v2/auth',
#                     'https://www.googleapis.com/oauth2/v4/token',
#                     'https://www.googleapis.com/auth/userinfo.email',
#                     'https://www.googleapis.com/auth/userinfo.profile',
#                     'https://www.googleapis.com/oauth2/v1/userinfo',
#                     'https://upd.edu.ph/privacy/',
#                     'https://kit.fontawesome.com/0656940dab.js',
#                     'https://forms.gle/yC2qMFUTiaQ58YRe8',
#                     'https://kit.fontawesome.com/0656940dab.js', ],
#     'prefetch-src': '\'self\'',
#     'script-src': '\'self\'',  # [SELF, '\'unsafe-eval\''],   # [1]
#     'style-src': ['\'self\'', '*',   '\'unsafe-inline\''],  # [2]
#     'navigate-to': '\'self\'',
#     'base-uri': '\'self\'',
#     'form-action': '\'self\'',
#     'frame-ancestors': '*',  # '\'none\'',
#     'object-src': '*',  # '\'none\'',
#     'media-src': '*',
#     'img-src': '*',
# }
#
# server = app.server
# Talisman(server,
#          content_security_policy=csp,
#          force_https=False,
#          content_security_policy_nonce_in=['script-src'],
#          content_security_policy_report_only=True,
#          content_security_policy_report_uri='/report-csp-violations.txt'
#          )  # not working
# # sslify = SSLify(server)
#
#
# app.title = 'HRDO PUSO System'
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
