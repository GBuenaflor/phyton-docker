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
                html.H4("Add New Entitlement", id = "ent_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Entitlements", id = "ent_results_head"),
                dbc.ModalBody([
                ], id = "ent_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_ent_head_close", color="primary", block=True),
                        ], id="ent_results_head_close", style={'display':'none'} ),
                        dbc.Col([
                            dbc.Button("Return", id="btn_ent_results_head_return", color="primary", block=True, href ='/settings/settings_entitlements'),
                        ], id="ent_results_head_return", style={'display':'none'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="ent_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Entitlements', href='/settings/settings_entitlements'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Entitlement Code", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="ent_code", placeholder="Enter Entitlement Code"
                            ),
                            #dbc.FormFeedback("Too short or already taken", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Entitlement Name", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="ent_name", placeholder="Enter Entitlement Name"
                            ),
                            dbc.FormFeedback("Too short or already taken", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Entitlement Description", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="ent_desc", placeholder="Enter Entitlement description"
                            ),
                            #dbc.FormFeedback("Too short or already taken", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),


                    html.Div([
                        dcc.Checklist(
                                options=[
                                    {'label': 'Mark for Deletion?', 'value': '1'},
                                ], id='ent_chkmarkfordeletion', value=[]
                            ),
                    ],id='diventdelete',  style={'text-align':'middle', 'display':'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Entitlement", id="ent_submit", color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="ent_cancel", color="secondary", className="ml-auto", href='/settings/settings_entitlements')
                    ]),
                ], style={'width':'100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='ent_submit_status', type='text', value="0")
                    ], style={'display':'none'}),
                    html.Div([
                        dcc.Input(id='ent_id', type='text', value="0")
                    ], style={'display':'none'}),
                    dcc.ConfirmDialog(
                        id='ent_message',
                    ),], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback(
    [
        Output('ent_code', 'value'),
        Output('ent_name', 'value'),
        Output('ent_desc', 'value'),
        Output("ent_process_editmodalhead", "children"),
        Output("ent_submit", "children"),
        Output("ent_id",'value'),
        Output("ent_chkmarkfordeletion", "value"),
        Output("diventdelete", "style"),
    ],
    [
        Input('ent_submit_status', 'value'),
        Input('btn_ent_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('ent_code', 'value'),
        State('ent_name', 'value'),
        State('ent_desc', 'value'),
        State('ent_process_editmodalhead',"children"),
        State("ent_submit", "children"),
        State("ent_id",'value'),
        State("ent_chkmarkfordeletion", "value"),
    ]

)
def cleardata(ent_submit_status,btn_ent_head_close,url,
    ent_code, ent_name, ent_desc, ent_process_editmodalhead,ent_submit,ent_id,ent_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            ent_id = parse_qs(parsed.query)['entitle_id'][0]
            sql = '''SELECT entitle_code, entitle_name, entitle_desc FROM entitlements WHERE entitle_id=%s'''
            values = (ent_id, )
            columns = ['entitle_code', 'entitle_name', 'entitle_desc']
            df = securequerydatafromdatabase(sql,values,columns)
            ent_code = df["entitle_code"][0]
            ent_name = df["entitle_name"][0]
            ent_desc = df["entitle_desc"][0]
            values = [ent_code, ent_name, ent_desc, "Edit Existing Entitlement","Save Changes", ent_id,[],{'text-align':'middle', 'display':'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["","","",ent_process_editmodalhead,ent_submit,ent_id,[],{'display':'none'}]
            return values
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("ent_code", "valid"),
        Output("ent_code", "invalid"),
        Output("ent_name", "valid"),
        Output("ent_name", "invalid"),
        Output("ent_desc", "valid"),
        Output("ent_desc", "invalid"),
        Output('ent_submit_status',"value"),
        Output('ent_results_modal',"is_open"),
        Output('ent_results_body',"children"),
        Output('ent_results_head_close',"style"),
        Output('ent_results_head_return',"style"),
    ],
    [
        Input('ent_submit', 'n_clicks'),
        Input('btn_ent_head_close', 'n_clicks'),
        Input('btn_ent_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('ent_code', 'value'),
        State('ent_name', 'value'),
        State('ent_desc', 'value'),
        State("ent_submit", "children"),
        State("ent_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('ent_id', 'value'),
    ]

)
def processdata(ent_submit,btn_ent_head_close,btn_ent_results_head_return,
    current_user_id, ent_code, ent_name, ent_desc, mode, ent_chkmarkfordeletion,url,ent_id):
    ctx = dash.callback_context
    stylehead_close = {'display':'none'}
    stylehead_return = {'display':'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,
            False, False,
            False, False
            ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'ent_submit':
            if ent_code:
                if len(ent_code) == 0:
                    is_valid_ent_code = False
                else:
                    is_valid_ent_code = True
            else:
                is_valid_ent_code = False

            if ent_name:
                if len(ent_name) == 0:
                    is_valid_ent_name = False
                else:
                    is_valid_ent_name = True
            else:
                is_valid_ent_name = False

            if ent_desc:
                is_valid_ent_desc= True
            else:
                is_valid_ent_desc= True

            # if ent_desc:
            #     if len(ent_desc) == 0:
            #         is_valid_ent_desc = False
            #     else:
            #         is_valid_ent_desc = True
            # else:
            #     is_valid_ent_desc = False

            validity = [
                is_valid_ent_code, not is_valid_ent_code,
                is_valid_ent_name, not is_valid_ent_name,
                is_valid_ent_desc, not is_valid_ent_desc,

            ]
            allvalid = [is_valid_ent_code, is_valid_ent_name, is_valid_ent_desc]
            if all(allvalid):
                if mode =="Save New Entitlement":
                    sql = """
                        INSERT INTO entitlements (entitle_code, entitle_name, entitle_desc, entitle_inserted_by, entitle_inserted_on, entitle_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING entitle_id
                    """
                    values = (ent_code, ent_name, ent_desc, current_user_id, datetime.now(), False)
                    entitle_id = modifydatabasereturnid(sql,values)
                    displayed = True
                    message = "Successfully added new entitlement"
                    status = "1"
                    stylehead_close = {'display':'inline'}
                    stylehead_return = {'display':'none'}
                else:
                    sql = """
                        UPDATE entitlements SET entitle_code = %s, entitle_name = %s, entitle_desc = %s,
                            entitle_delete_ind= %s, entitle_inserted_by= %s, entitle_inserted_on= %s WHERE
                            entitle_id = %s
                    """
                    if '1' in ent_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete= False
                    values = (ent_code, ent_name, ent_desc, fordelete, current_user_id, datetime.now(), ent_id)
                    modifydatabase(sql,values)
                    validity = [
                        False, False,
                        False, False,
                        False, False
                        ]
                    stylehead_close = {'display':'none'}
                    stylehead_return = {'display':'inline'}
                    displayed = True
                    message = "Successfully edited entitlement"
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
        elif eventid == 'btn_ent_head_close':
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
