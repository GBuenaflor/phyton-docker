import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
from dash.dependencies import Input, Output, State
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps import home
from apps.dbconnect import querydatafromdatabase, securequerydatafromdatabase, modifydatabase, modifydatabasereturnid
import hashlib
from datetime import datetime
#import dash_table
import pandas as pd
import numpy as np
import base64
from requests_oauthlib import OAuth2Session
import json
import os
import flask
from flask import request
import requests
from dash_extensions import Keyboard
from flask import request
import urllib.parse as urlparse
from urllib.parse import parse_qs
#
# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# import googleapiclient.discovery


def returnupgooglelogincreds():
    #client_id = os.environ['client_id']
    client_id = '381724806277-c9f8covbca6viba1b3j29tafigrlmt72.apps.googleusercontent.com'
    client_secret = 'kV7aHIPO-QFyGpGDwZ3umJ1e'
    #redirect_uri = 'http://127.0.0.1:8050/'
    redirect_uri = 'http://127.0.0.1:8050/'
    authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url = "https://www.googleapis.com/oauth2/v4/token"
    scope = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ]
    return client_id, client_secret, redirect_uri, authorization_base_url, token_url, scope


image_filename = 'static/HRDO.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


login_CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "display": "flex"
}

layout = html.Div([
    commonmodules.get_common_variables(),
    html.Div([
        html.Div([
            Keyboard(id="keyboard"),
            dcc.ConfirmDialog(
                id='loginerror',
                message='Error, please provide correct credentials',
            ),
            html.Div([
                dcc.Input(id='loginstate', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                dcc.Input(id='loginupstate', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height="85px", width="600px"),
                ], style={'width': '100%', 'display': 'inline-block', 'fontSize': '30px', 'vertical-align': 'middle', 'height': '60px',  "text-align": "center"}),
                html.P(" ", style={"fontSize": "24px"}),
                html.Br(),
                dbc.FormGroup(dbc.FormText("version 1.0"), style={
                              "textAlign": "center", "vertical-align": "bottom"})
            ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle', 'height': '60px'})
        ], id="loginpageheader", style={"position": 'absolute', "left": "50%", "transform": "translate(-50%,0%)", "width": "38rem", }
        ),
        html.Div([

            dbc.Card([
                dbc.CardBody(
                    html.H4("Login", style={"textAlign": "center",
                                            "fontWeight": "bold", "color": "white"}, id="loginname"),
                    style={"background-color": "rgb(123,20,24)"}
                ),
                dbc.Spinner([
                    html.Div([
                        dbc.CardBody([
                            dbc.Form([
                                dbc.Card([
                                    dbc.CardBody([
                                        html.H5("Log-in Credentials",
                                                className='card-subtitle'),
                                        html.Hr(),
                                        html.Br(),
                                        html.Div([
                                            dbc.FormGroup(
                                                [dbc.Label("Username", width=4, style={"text-align": "right"}),
                                                 dbc.Col([
                                                     dbc.Input(
                                                         type="text", id="txtusername", placeholder="Enter username", autoFocus=True
                                                     ),

                                                 ],
                                                    width=8
                                                )],
                                                row=True
                                            ),
                                            dbc.FormGroup(
                                                [dbc.Label("Password", width=4, style={"text-align": "right"}),
                                                 dbc.Col([
                                                     dbc.Input(
                                                         type="password", id="txtuserpassword", placeholder="Enter password"
                                                     ),
                                                 ], width=8
                                                )],
                                                row=True
                                            )
                                        ], style={'display': 'inline'}),
                                        html.Div([
                                            dbc.Button("Login Via UP Mail", id="btnloginup", color="primary",
                                                       block=True, n_clicks=0)  # , n_clicks=0),
                                        ], style={"display": "none", "width": "100%"}),  # "inline-block"
                                    ]),
                                    html.Br(),
                                    html.Div([
                                        dcc.Input(id='loginloading', type='text', value="0")
                                    ], style={'display': 'none'}),
                                    html.Div([
                                        dbc.Button("Login", id="btnlogin", color="primary",
                                                   block=True, n_clicks=0),
                                    ], style={"display": "inline", "width": "100%"}
                                    ),

                                    html.Br(),


                                ], style={"display": "block"}),  # "block"
                            ])
                        ], style={"background-color": "#f8f9fa"}),
                    ], id="logindiv"),
                    html.Div([
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ], id="logindivmlogin"),
                ], color="danger"),
                dbc.CardFooter([
                    html.P(["                      "
                    # html.P(["You can review UPD HRDO PUSO's Privacy Policy ", html.A("here", href='/privacy', style={"textDecoration": "underline", "cursor": "pointer"}), "."
                     # You may also find more info about the site ",
                    # html.A("here", href='/siteinfo', style={"textDecoration": "underline", "cursor": "pointer"}), '.'
                    ],


                    style={"textAlign": "center"}),
                    html.Br(),
                    ], style={"background-color": "#CDCDCD"})
            ],
                style={"position": 'absolute', "top": "20%", "left": "50%",
                       "transform": "translate(-50%,0%)", "width": "38rem", "border": "2px solid", },
                color='light',
                className='border-dark',
            )
        ],
            style=login_CONTENT_STYLE
        )
    ]),
])


@app.callback([Output('current_user_id', 'data'),
               Output('loginerror', 'displayed'),
               Output('loginerror', 'message'),
               Output('txtusername', 'value'),
               Output('txtuserpassword', 'value'),
               Output('loginstate', 'value'),
               Output('sessionmenudict', 'data'),
               Output('sessionddroledropdown', 'data'),
               Output('sessiondefaultrole', 'data'),
               Output('sessionroleaccessunits', 'data'), #access level
               Output('sessionroleunits', 'data'), #home
               Output('sessionlistofunits', 'data'), #access level
               Output('sessionlistofunits_home', 'data'), #home
               # Output('sessioncurrentunit', 'data'),  # added feb 5
               Output('loginloading', 'value'),
               ],
              [Input('btnlogin', 'n_clicks'),
               Input('url', 'search'),
               Input("sessionlogout", 'modified_timestamp'),
               #   Input("btnloginup", "n_clicks")
               ],
              [State('txtusername', 'value'),
               State('txtuserpassword', 'value'), State('url', 'pathname'), State('googlestate', 'data'), State('current_user_id','data')])
def loginfunction(n_clicks, url, sessionlogout, txtusername, txtuserpassword, path, state,current_user_id):

    if sessionlogout == False:
        raise PreventUpdate
    loginerrordisplayed = False
    loginerrormessage = ""
    user_key = -1
    ctx = dash.callback_context
    loginstate = 0
    dfdict = {}
    dfoptions = {}
    dfunitroles = {}
    defaultrole = ""
    listofunits = {}
    defaultunit = ""
    dfoptionroles_home = {}
    listofunits_home = {}
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        # print("login event", eventid)
        # print("login state", state)
        # print("login url", url)
        if eventid == "btnlogin" or eventid == "keyboard":

            if txtusername and txtuserpassword and (n_clicks > 0 or eventid == "keyboard"):

                txtuserpassword = hash_string(txtuserpassword)
                sql = """SELECT user_id, user_name FROM users WHERE user_name = %(username)s AND user_password = %(txtuserpassword)s
                    AND user_delete_ind= %(user_delete_ind)s;"""
                values = {'username': txtusername,
                          'txtuserpassword': txtuserpassword, 'user_delete_ind': False}
                columns = ['user_id', 'user_name']
                users = securequerydatafromdatabase(sql, values, columns)
                user_key = []
                if users.shape[0] == 1:
                    user_key = users['user_id'][0].item()
                    saveuserlogin(user_key, request.remote_addr)
                    loginstate = 1
                    dfdict, dfoptions, defaultrole, dfunitroles, listofunits, dfoptionroles_home, listofunits_home = returnmenulist(  # defaultunit

                        user_key)

                else:
                    loginerrordisplayed = True
                    loginerrormessage = "Please provide correct credentials"
            elif n_clicks == 0 and state and path != "/logout" and url:
                parsed = urlparse.urlparse(url)

                if "state" in parse_qs(parsed.query):

                    state = str(parse_qs(parsed.query)['state'][0])
                    client_id, client_secret, redirect_uri, authorization_base_url, token_url, scope = returnupgooglelogincreds()
                    redirect_response = path+url

                    google = OAuth2Session(client_id, state=state, redirect_uri=redirect_uri)
                    google.fetch_token(token_url, client_secret=client_secret,
                                       authorization_response=redirect_response)
                    r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
                    res = json.loads(r.content.decode('UTF-8'))
                    email = res['email']
                # elif "search" in parse_qs(parsed.query):
                #     # headers = request.headers
                #     # auth = headers.get("apikey")
                #     # if auth == 'pusotbulsa2022':
                #     #     emailjson = request.get_json()
                #     #     print(emailjson)
                #     search = str(parse_qs(parsed.query)['search'][0])
                #     email=search
                else:
                    email=None


                sql = """SELECT user_id, user_name FROM users WHERE user_up_email = %(user_up_email)s
                    AND user_delete_ind= %(user_delete_ind)s;"""
                values = {'user_up_email':email ,
                          'user_delete_ind': False}
                columns = ['user_id', 'user_name']
                users = securequerydatafromdatabase(sql, values, columns)
                user_key = []
                if users.shape[0] == 1:
                    user_key = users['user_id'][0].item()
                    saveuserlogin(user_key, request.remote_addr)
                    loginstate = 1
                    dfdict, dfoptions, defaultrole, dfunitroles, listofunits, dfoptionroles_home, listofunits_home = returnmenulist(  # defaultunit
                        user_key)
                else:

                    loginerrordisplayed = True
                    loginerrormessage = "Your UP Email is not registered. Please contact HRDO for you to use this website."

            elif n_clicks == 0:
                # print("executed here",current_user_id)
                pass
                #raise PreventUpdate
            else:
                loginerrordisplayed = True
                loginerrormessage = "Please provide username and password"

        #    print( dfdict, dfoptions, defaultrole, dfunitroles, listofunits)
        elif eventid == "sessionlogout":
            # print("logout!")
            user_key = -1

    else:
        raise PreventUpdate
    # print(user_key)
#    print(dfdict)
#    print(dfunitroles)
    # print('printing from returnmenulist ', listofunits)
    return [user_key, loginerrordisplayed, loginerrormessage, "", "", loginstate, dfdict, dfoptions, defaultrole, dfunitroles, dfoptionroles_home, listofunits, listofunits_home, 2]  # defaultunit


def saveuserlogin(user_key, ipaddress):
    bp_statuses = [user_key, ipaddress, datetime.now()]
    sqlbpstatuses = """
        INSERT INTO account_logins(user_id, ip_address, login_date_time)
        VALUES (%s, %s, %s)

    """
    modifydatabase(sqlbpstatuses, bp_statuses)


def returnmenulist(userid):

    sqlcommand = '''SELECT user_id, r.role_id, role_name, module_name, module_header, module_link, ur.user_role_default, u.unit_name, u.unit_id,
                    m.module_is_report, m.module_icon, m.module_is_open, un.unit_name, un.unit_id
    FROM user_roles ur INNER JOIN roles r on r.role_id = ur.role_id
    INNER JOIN module_roles mr ON r.role_id = mr.role_id
    INNER JOIN modules m on m.module_id= mr.module_id
    INNER JOIN units u on u.unit_id = ur.user_role_access_level_unit_id
    INNER JOIN units un on un.unit_id = ur.user_role_unit_id
    WHERE module_delete_ind = %s
    AND user_id=%s
    AND user_role_delete_ind = %s
    AND user_role_active_ind = %s
    ORDER BY role_name, m.module_header, m.module_name

    '''
    values = (False, str(userid), False, True)
    columns = ["user_id", "role_id", "role_name", "module_name", "module_header",
               "module_link", "user_role_default", "unit_name", "unit_id", 'module_is_report',
               'module_icon', 'module_is_open', 'home_unit_name', 'home_unit_id']
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    dfdict = df.copy()
    dfdict = dfdict.to_dict('list')
    defaultrole = df[["role_id", "role_name", "user_role_default"]].copy()
    defaultrole = defaultrole.drop_duplicates(keep='last')
    defaultrole = defaultrole[defaultrole["user_role_default"] == True]["role_id"].item()
    dfoptions = df[["role_id", "role_name"]].copy()
    dfoptions = dfoptions.drop_duplicates(keep='last')
    dfoptions.columns = ["value", 'label']
    dfoptions = dfoptions.to_dict('records')

    dfoptionroles = df[["role_id", "unit_id", "unit_name"]].copy()
    dfoptionroles = dfoptionroles.drop_duplicates(keep='last')

    dfoptionroles.columns = ["role_id", 'unit_id', 'unit_name']
    # print('printing dfoptionroles, ', dfoptionroles)
    listofunits = queryallsubunits(dfoptionroles)
    #print('printing from login ', listofunits)
    dfoptionroles = dfoptionroles.to_dict('records')


    #session unit roles based on home level

    dfoptionroles_home = df[["role_id", "home_unit_id", "home_unit_name"]].copy()
    dfoptionroles_home = dfoptionroles_home.drop_duplicates(keep='last')
    dfoptionroles_home.columns = ["role_id", 'unit_id', 'unit_name']
    listofunits_home = queryallsubunits(dfoptionroles_home)
    dfoptionroles_home = dfoptionroles_home.to_dict('records')

    # default unit added feb 5
    # defaultunit = df[["role_id", "role_name", "user_role_default", "unit_name", "unit_id"]].copy()
    # defaultunit = defaultunit.drop_duplicates(keep='last')
    # defaultunit = defaultunit[defaultunit["user_role_default"] == True]["unit_id"].item()

    #print("return: ", dfdict, dfoptions, defaultrole, dfoptionroles, listofunits)
    return dfdict, dfoptions, defaultrole, dfoptionroles, listofunits, dfoptionroles_home, listofunits_home # , defaultunit


def saveuserlogin(user_key, ipaddress):
    bp_statuses = [user_key, ipaddress, datetime.now()]
    sqlbpstatuses = """
        INSERT INTO account_logins(user_id, ip_address, login_date_time)
        VALUES (%s, %s, %s)
    """
    modifydatabase(sqlbpstatuses, bp_statuses)


def queryallsubunits(df):
    listofunits = {}
    for index, row in df.iterrows():
        sql = '''
        WITH RECURSIVE subordinates AS (
        	SELECT unit_id,	unit_parent_id,	unit_name
        	FROM units
        	WHERE unit_id = %s
        	UNION
        		SELECT e.unit_id,e.unit_parent_id,e.unit_name
        		FROM units e
        		INNER JOIN subordinates s ON s.unit_id = e.unit_parent_id
        ) SELECT * FROM subordinates
        '''
        # IF OVC Offices, Set Parent as Diliman
        # if row["unit_id"] in [28, 27, 30]:
        #     values = (2,)
        # else:
        values = (row["unit_id"],)
        columns = ["unit_id", "unit_parent_id", "unit_name"]
        dfquery = securequerydatafromdatabase(sql, values, columns)
        listofunits[row["unit_id"]] = dfquery['unit_id'].to_list()
    return listofunits


@app.callback([
    Output('logindiv', 'style'),
    Output('logindivmlogin', 'style'),
    Output('loginname', 'children'),
    #
],
    [
    Input('url', 'search'),

],
    [
    State('url', 'pathname'),
],)
def logindiv(search,  pathname):

    if (pathname == "/" or pathname == "/logout") and search:
        return [{'display': 'none'}, {'display': 'inline'}, ["Processing Login"]]
    else:
        return [{'display': 'inline'}, {'display': 'none'}, ["Login"]]


@app.callback([
    Output('url', 'pathname'),
    #
],
    [
    Input('loginstate', 'value'),
    Input('loginupstate', 'value'),
],
    [
    State('url', 'pathname'),
    State('current_user_id', 'data'),
],)
def loginprocesses(loginstate, loginupstate, pathname, current_user_id):
    # menudiv = [] #commented Feb 16, 2021
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == "loginstate" and loginstate == 1:  # and pathname=="/home":

            if current_user_id != -1:
                pathname = "/main"
                return [pathname]
            else:
                raise PreventUpdate
        elif eventid == "loginupstate" and loginupstate == 1:  # and pathname=="/home":

            if current_user_id != -1:

                pathname = "/main"
                return [pathname]
            else:
                raise PreventUpdate
        elif eventid == "loginstate" and loginstate == 0 and pathname != "/":  # and pathname=="/home":

            pathname = "/logout"
            return [pathname]
        else:

            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('btnloginup', 'href'),
    Output('loginupstate', 'value'),
    Output('googlestate', 'data'),
    # Output('url','search')
],
    [
    Input('url', 'pathname'),

],
    [

    State('googlestate', 'data'),
    State('url', 'search'),
],)
def creategooglehref(url, state, search):

    if not search:
        if url == "/" or url == "/logout":
            client_id, client_secret, redirect_uri, authorization_base_url, token_url, scope = returnupgooglelogincreds()
            google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
            authorization_url, state = google.authorization_url(
                authorization_base_url, access_type="offline", prompt="select_account")

            return [authorization_url, 0, state]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

    #print("google", url)
    # ctx = dash.callback_context
    # # print(ctx.triggered)
    # if ctx.triggered:
    #     eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    #
    #     if eventid == "url":
    #         if (url == "/" or url == "/logout"):
    #
    #             client_id, client_secret, redirect_uri, authorization_base_url, token_url, scope = returnupgooglelogincreds()
    #             google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    #             authorization_url, state = google.authorization_url(
    #                 authorization_base_url, access_type="offline", prompt="select_account")
    #
    #             return [authorization_url, 0, state]
    #         else:
    #             raise PreventUpdate
    #     else:
    #         raise PreventUpdate
    # else:
    #
    #     raise PreventUpdate
