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
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid
import hashlib
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
import urllib.parse as urlparse
from urllib.parse import parse_qs
import logging

app.config.suppress_callback_exceptions = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()
layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Role", id = "role_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dcc.ConfirmDialog(
                id='role_usermessage',
            ),
            dbc.Modal([
                dbc.ModalHeader("Process roles", id = "role_results_head"),
                dbc.ModalBody([
                ], id = "role_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_role_head_close", color="primary", block=True),
                        ], id="roles_results_head_close", style={'display':'none'} ),
                        dbc.Col([
                            dbc.Button("Return", id="btn_role_results_head_return", color="primary", block=True, href ='/settings/settings_roles'),
                        ], id="roles_results_head_return", style={'display':'none'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="roles_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Roles', href='/settings/settings_roles'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Role Name", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="role_name", placeholder="Enter role name"
                            ),
                            dbc.FormFeedback("Too short, already taken, or has spaces", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),


                    html.Div([
                        dcc.Checklist(
                                options=[
                                    {'label': 'Mark for Deletion?', 'value': '1'},
                                ], id='role_chkmarkfordeletion', value=[]
                            ),
                    ],id='divroledelete',  style={'text-align':'middle', 'display':'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Role", id="role_submit", color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="role_cancel", color="secondary", className="ml-auto", href ='/settings/settings_roles')
                    ]),
                ], style={'width':'100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='role_submit_status', type='text', value="0")
                    ], style={'display':'none'}),
                    html.Div([
                        dcc.Input(id='role_id', type='text', value="0")
                    ], style={'display':'none'}),
                    dcc.ConfirmDialog(
                        id='role_message',
                    ),], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback(
    [
        Output('role_name', 'value'),
        Output("role_process_editmodalhead", "children"),
        Output("role_submit", "children"),
        Output("role_id",'value'),
        Output("role_chkmarkfordeletion", "value"),
        Output("divroledelete", "style"),
    ],
    [
        Input('role_submit_status', 'value'),
        Input('btn_role_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('role_name', 'value'),
        State('role_process_editmodalhead',"children"),
        State("role_submit", "children"),
        State("role_id",'value'),
        State("role_chkmarkfordeletion", "value"),
    ]

)
def clear_roles_data(role_submit_status,btn_role_head_close,url,
    role_name, role_process_editmodalhead,role_submit,role_id,role_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            role_id = parse_qs(parsed.query)['role_id'][0]
            sql = '''SELECT role_name FROM roles WHERE role_id=%s'''
            values = (role_id, )
            columns = ['role_name']
            df = securequerydatafromdatabase(sql,values,columns)
            role_name = df["role_name"][0]
            values = [role_name,"Edit Existing Role","Save Changes",role_id,[],{'text-align':'middle', 'display':'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["",role_process_editmodalhead,role_submit,role_id,[],{'display':'none'}]
            return values
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("role_name", "valid"),
        Output("role_name", "invalid"),
        Output('role_submit_status',"value"),
        Output('roles_results_modal',"is_open"),
        Output('role_results_body',"children"),
        Output('roles_results_head_close',"style"),
        Output('roles_results_head_return',"style"),
    ],
    [
        Input('role_submit', 'n_clicks'),
        Input('btn_role_head_close', 'n_clicks'),
        Input('btn_role_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('role_name', 'value'),
        State("role_submit", "children"),
        State("role_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('role_id', 'value'),
    ]

)
def process_roles_data(role_submit,btn_role_head_close,btn_role_results_head_return,
    current_user_id, role_name, mode, role_chkmarkfordeletion,url,role_id):
    ctx = dash.callback_context
    stylehead_close = {'display':'none'}
    stylehead_return = {'display':'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False
            ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'role_submit':
            if role_name:
                is_valid_role_name= True
            else:
                is_valid_role_name= False

            validity = [
                is_valid_role_name, not is_valid_role_name,

            ]
            allvalid = [is_valid_role_name]
            if all(allvalid):
                if mode =="Save New Role":
                    sql = """
                        INSERT INTO roles (role_name, role_delete_ind,
                        role_modified_by, role_modified_on)
                        VALUES (%s, %s, %s, %s)
                        RETURNING role_id
                    """
                    values = (role_name, False, current_user_id, datetime.now())
                    role_id = modifydatabasereturnid(sql,values)
                    displayed = True
                    message = "Successfully added new role"
                    status = "1"
                    stylehead_close = {'display':'inline'}
                    stylehead_return = {'display':'none'}
                else:
                    sql = """
                        UPDATE roles SET role_name = %s,
                            role_delete_ind= %s, role_modified_by= %s, role_modified_on= %s WHERE
                            role_id = %s
                    """
                    if '1' in role_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete= False
                    values = (role_name, fordelete, current_user_id, datetime.now(), role_id)
                    modifydatabase(sql,values)
                    validity = [
                        False, False
                        ]
                    stylehead_close = {'display':'none'}
                    stylehead_return = {'display':'inline'}
                    displayed = True
                    message = "Successfully edited role"
                    status = "1"
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display':'inline'}
                stylehead_return = {'display':'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out

            return out
        elif eventid == 'btn_role_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display':'inline'}
            stylehead_return = {'display':'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
