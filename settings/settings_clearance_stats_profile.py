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
                html.H4("Add New Role", id = "cstatus_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dcc.ConfirmDialog(
                id='cstatus_usermessage',
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Status", id = "cstatus_results_head"),
                dbc.ModalBody([
                ], id = "cstatus_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_cstatus_head_close", color="primary", block=True),
                        ], id="status_results_head_close", style={'display':'none'} ),
                        dbc.Col([
                            dbc.Button("Return", id="btn_cstatus_results_head_return", color="primary", block=True, href ='/settings/settings_clearance_stats'),
                        ], id="cstatus_results_head_close", style={'display':'none'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="cstatus_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Clearances', href='/settings/settings_clearance_stats'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Clearance Name", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="cstatus_name", placeholder="Enter role Name"
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
                                ], id='cstatus_chkmarkfordeletion', value=[]
                            ),
                    ],id='divcstatusdelete',  style={'text-align':'middle', 'display':'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Status", id="cstatus_submit", color="info", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="cstatus_cancel", color="warning", className="ml-auto")
                    ]),
                ], style={'width':'100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='cstatus_submit_status', type='text', value="0")
                    ], style={'display':'none'}),
                    html.Div([
                        dcc.Input(id='cstatus_id', type='text', value="0")
                    ], style={'display':'none'}),
                    dcc.ConfirmDialog(
                        id='cstatus_message',
                    ),], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback(
    [
        Output('cstatus_name', 'value'),
        Output("cstatus_process_editmodalhead", "children"),
        Output("cstatus_submit", "children"),
        Output("cstatus_id",'value'),
        Output("cstatus_chkmarkfordeletion", "value"),
        Output("divcstatusdelete", "style"),
    ],
    [
        Input('cstatus_submit_status', 'value'),
        Input('btn_cstatus_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('cstatus_name', 'value'),
        State('cstatus_process_editmodalhead',"children"),
        State("cstatus_submit", "children"),
        State("cstatus_id",'value'),
        State("cstatus_chkmarkfordeletion", "value"),
    ]

)
def cleardata(cstatus_submit_status,btn_cstatus_head_close,url,
    cstatus_name, cstatus_process_editmodalhead,cstatus_submit,cstatus_id,cstatus_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            cstatus_id = parse_qs(parsed.query)['status_id'][0]
            sql = '''SELECT clearance_office_status_name FROM clearance_office_statuses WHERE clearance_office_status_id=%s'''
            values = (cstatus_id, )
            columns = ['clearance_office_status_name']
            df = securequerydatafromdatabase(sql,values,columns)
            clearance_office_status_name = df["clearance_office_status_name"][0]
            values = [clearance_office_status_name,"Edit Existing Status:","Save Changes",cstatus_id,[],{'text-align':'middle', 'display':'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["",cstatus_process_editmodalhead,cstatus_submit,cstatus_id,[],{'display':'none'}]
            return values
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("cstatus_name", "valid"),
        Output("cstatus_name", "invalid"),
        Output('cstatus_submit_status',"value"),
        Output('cstatus_results_modal',"is_open"),
        Output('cstatus_results_body',"children"),
        Output('status_results_head_close',"style"),
        Output('cstatus_results_head_close',"style"),
    ],
    [
        Input('cstatus_submit', 'n_clicks'),
        Input('btn_cstatus_head_close', 'n_clicks'),
        Input('btn_cstatus_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('cstatus_name', 'value'),
        State("cstatus_submit", "children"),
        State("cstatus_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('cstatus_id', 'value'),
    ]

)
def processdata(cstatus_submit,btn_cstatus_head_close,btn_cstatus_results_head_return,
    current_user_id, cstatus_name, mode, cstatus_chkmarkfordeletion,url,cstatus_id):
    ctx = dash.callback_context
    stylehead_close = {'display':'none'}
    stylehead_return = {'display':'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False
            ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'cstatus_submit':
            if cstatus_name:
                is_valid_cstatus_name= True
            else:
                is_valid_cstatus_name= False

            validity = [
                is_valid_cstatus_name, not is_valid_cstatus_name,

            ]
            allvalid = [is_valid_cstatus_name]
            if all(allvalid):
                if mode =="Save New Status":
                    sql = """
                        INSERT INTO clearance_office_statuses (clearance_office_status_name, clearance_office_status_delete_ind,
                        clearance_office_status_inserted_by, clearance_office_status_inserted_on)
                        VALUES (%s, %s, %s, %s)
                        RETURNING clearance_office_status_id
                    """
                    values = (cstatus_name, False, current_user_id, datetime.now())
                    clearance_office_status_id = modifydatabasereturnid(sql,values)
                    displayed = True
                    message = "Successfully added new role"
                    status = "1"
                    stylehead_close = {'display':'inline'}
                    stylehead_return = {'display':'none'}
                else:
                    sql = """
                        UPDATE clearance_office_statuses SET clearance_office_status_name = %s,
                            clearance_office_status_delete_ind= %s, clearance_office_status_inserted_by= %s, clearance_office_status_inserted_on= %s WHERE
                            clearance_office_status_id = %s
                    """
                    if '1' in cstatus_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete= False
                    values = (cstatus_name, fordelete, current_user_id, datetime.now(), cstatus_id)
                    modifydatabase(sql,values)
                    validity = [
                        False, False
                        ]
                    stylehead_close = {'display':'none'}
                    stylehead_return = {'display':'inline'}
                    displayed = True
                    message = "Successfully edited status"
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
        elif eventid == 'btn_cstatus_head_close':
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
