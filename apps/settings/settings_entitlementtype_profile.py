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
                html.H4("Add New Entitlement Type", id = "enttype_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Entitlement Types", id = "enttype_results_head"),
                dbc.ModalBody([
                ], id = "enttype_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_enttype_head_close", color="primary", block=True),
                        ], id="enttype_results_head_close", style={'display':'none'} ),
                        dbc.Col([
                            dbc.Button("Return", id="btn_enttype_results_head_return", color="primary", block=True, href ='/settings/settings_entitlements'),
                        ], id="enttype_results_head_return", style={'display':'none'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="enttype_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Entitlements', href='/settings/settings_entitlements'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Entitlement Type Code", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="enttype_code", placeholder="Enter Entitlement Type Code"
                            ),
                            #dbc.FormFeedback("Too short or already taken", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Entitlement Type Name", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="enttype_name", placeholder="Enter Entitlement Type Name"
                            ),
                            dbc.FormFeedback("Too short or already taken", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),
                    # dbc.FormGroup(
                    #     [dbc.Label("Entitlement Description", width=2, style={"text-align":"left"}),
                    #     dbc.Col([
                    #         dbc.Input(
                    #             type="text", id="ent_desc", placeholder="Enter Entitlement description"
                    #         ),
                    #         #dbc.FormFeedback("Too short or already taken", valid = False)
                    #     ],
                    #     width=8
                    #     )],
                    #     row = True
                    # ),


                    html.Div([
                        dcc.Checklist(
                                options=[
                                    {'label': 'Mark for Deletion?', 'value': '1'},
                                ], id='enttype_chkmarkfordeletion', value=[]
                            ),
                    ],id='diventtypedelete',  style={'text-align':'middle', 'display':'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Entitlement Type", id="enttype_submit", color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="enttype_cancel", color="secondary", className="ml-auto", href='/settings/settings_entitlements')
                    ]),
                ], style={'width':'100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='enttype_submit_status', type='text', value="0")
                    ], style={'display':'none'}),
                    html.Div([
                        dcc.Input(id='enttype_id', type='text', value="0")
                    ], style={'display':'none'}),
                    dcc.ConfirmDialog(
                        id='enttype_message',
                    ),], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback(
    [
        Output('enttype_code', 'value'),
        Output('enttype_name', 'value'),
        #Output('ent_desc', 'value'),
        Output("enttype_process_editmodalhead", "children"),
        Output("enttype_submit", "children"),
        Output("enttype_id",'value'),
        Output("enttype_chkmarkfordeletion", "value"),
        Output("diventtypedelete", "style"),
    ],
    [
        Input('enttype_submit_status', 'value'),
        Input('btn_enttype_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('enttype_code', 'value'),
        State('enttype_name', 'value'),
        #State('enttype_desc', 'value'),
        State('enttype_process_editmodalhead',"children"),
        State("enttype_submit", "children"),
        State("enttype_id",'value'),
        State("enttype_chkmarkfordeletion", "value"),
    ]

)
def cleardata(enttype_submit_status,btn_enttype_head_close,url,
    enttype_code, enttype_name, enttype_process_editmodalhead,enttype_submit, enttype_id,enttype_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            enttype_id = parse_qs(parsed.query)['entitle_type_id'][0]
            sql = '''SELECT entitle_type_code, entitle_type_name FROM entitlement_types WHERE entitle_type_id=%s'''
            values = (enttype_id, )
            columns = ['entitle_type_code', 'entitle_type_name']
            df = securequerydatafromdatabase(sql,values,columns)
            enttype_code = df["entitle_type_code"][0]
            enttype_name = df["entitle_type_name"][0]
            # ent_desc = df["entitle_desc"][0]
            values = [enttype_code, enttype_name, "Edit Existing Entitlement Type:","Save Changes", enttype_id,[],{'text-align':'middle', 'display':'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["","",enttype_process_editmodalhead,enttype_submit,enttype_id,[],{'display':'none'}]
            return values
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("enttype_code", "valid"),
        Output("enttype_code", "invalid"),
        Output("enttype_name", "valid"),
        Output("enttype_name", "invalid"),
        # Output("ent_desc", "valid"),
        # Output("ent_desc", "invalid"),
        Output('enttype_submit_status',"value"),
        Output('enttype_results_modal',"is_open"),
        Output('enttype_results_body',"children"),
        Output('enttype_results_head_close',"style"),
        Output('enttype_results_head_return',"style"),
    ],
    [
        Input('enttype_submit', 'n_clicks'),
        Input('btn_enttype_head_close', 'n_clicks'),
        Input('btn_enttype_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('enttype_code', 'value'),
        State('enttype_name', 'value'),
        # State('ent_desc', 'value'),
        State("enttype_submit", "children"),
        State("enttype_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('enttype_id', 'value'),
    ]

)
def processdata(enttype_submit,btn_entype_head_close,btn_enttype_results_head_return,
    current_user_id, enttype_code, enttype_name, mode, enttype_chkmarkfordeletion, url, enttype_id):
    ctx = dash.callback_context
    stylehead_close = {'display':'none'}
    stylehead_return = {'display':'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,
            False, False

            ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'enttype_submit':
            if enttype_code:
                if len(enttype_code) == 0:
                    is_valid_enttype_code = False
                else:
                    is_valid_enttype_code = True
            else:
                is_valid_enttype_code = False

            if enttype_name:
                if len(enttype_name) == 0:
                    is_valid_enttype_name = False
                else:
                    is_valid_enttype_name = True
            else:
                is_valid_enttype_name = False

            # if ent_desc:
            #     is_valid_ent_desc= True
            # else:
            #     is_valid_ent_desc= True

            # if ent_desc:
            #     if len(ent_desc) == 0:
            #         is_valid_ent_desc = False
            #     else:
            #         is_valid_ent_desc = True
            # else:
            #     is_valid_ent_desc = False

            validity = [
                is_valid_enttype_code, not is_valid_enttype_code,
                is_valid_enttype_name, not is_valid_enttype_name,
                # is_valid_ent_desc, not is_valid_ent_desc,

            ]
            allvalid = [is_valid_enttype_code, is_valid_enttype_name]
            if all(allvalid):
                if mode =="Save New Entitlement Type":
                    sql = """
                        INSERT INTO entitlement_types (entitle_type_code, entitle_type_name, entitle_type_inserted_by, entitle_type_inserted_on, entitle_type_delete_ind)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING entitle_type_id
                    """
                    values = (enttype_code, enttype_name, current_user_id, datetime.now(), False)
                    entitle_type_id = modifydatabasereturnid(sql,values)
                    displayed = True
                    message = "Successfully added new entitlement type"
                    status = "1"
                    stylehead_close = {'display':'inline'}
                    stylehead_return = {'display':'none'}
                else:
                    sql = """
                        UPDATE entitlement_types SET entitle_type_code = %s, entitle_type_name = %s,
                            entitle_type_delete_ind= %s, entitle_type_inserted_by= %s, entitle_type_inserted_on= %s WHERE
                            entitle_type_id = %s
                    """
                    if '1' in enttype_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete= False
                    values = (enttype_code, enttype_name, fordelete, current_user_id, datetime.now(), enttype_id)
                    modifydatabase(sql,values)
                    validity = [
                        False, False,
                        False, False,

                        ]
                    stylehead_close = {'display':'none'}
                    stylehead_return = {'display':'inline'}
                    displayed = True
                    message = "Successfully edited entitlement type"
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
        elif eventid == 'btn_enttype_head_close':
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
