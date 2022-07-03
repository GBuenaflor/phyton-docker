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
                html.H4("Add New Degree Program", id="degprog_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Degree Program", id="degprog_results_head"),
                dbc.ModalBody([
                ], id="degprog_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_degprog_head_close",
                                       color="primary", block=True),
                        ], id="degprog_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_degprog_results_head_return",
                                       color="primary", block=True, href='/settings/settings_degrees'),
                        ], id="degprog_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="degprog_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Degrees and Degree Programs',
                         href='/settings/settings_degrees'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Degree Program Code", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="degprog_code", placeholder="Enter Degree Program Code"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Degree Program Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="degprog_name", placeholder="Enter Degree Program Name"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Degree Program Description", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="degprog_desc", placeholder="Enter Degree Program Description"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),


                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='degprog_chkmarkfordeletion', value=[]
                        ),
                    ], id='divdegprogdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Degree Program Name",
                                   id="degprog_submit", color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="degprog_cancel", color="secondary",
                                   className="ml-auto", href='/settings/settings_degrees')
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='degprog_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='program_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='degprog_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('degprog_code', 'value'),
        Output('degprog_name', 'value'),
        Output('degprog_desc', 'value'),
        Output("degprog_process_editmodalhead", "children"),
        Output("degprog_submit", "children"),
        Output("program_id", 'value'),
        Output("degprog_chkmarkfordeletion", "value"),
        Output("divdegprogdelete", "style"),
    ],
    [
        Input('degprog_submit_status', 'value'),
        Input('btn_degprog_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('degprog_code', 'value'),
        State('degprog_name', 'value'),
        State('degprog_desc', 'value'),
        State('degprog_process_editmodalhead', "children"),
        State("degprog_submit", "children"),
        State("program_id", 'value'),
        State("degprog_chkmarkfordeletion", "value"),
    ]

)
def cleardata(degprog_submit_status, btn_degprog_head_close, url,
              degprog_code, degprog_name, degprog_desc, degprog_process_editmodalhead, degprog_submit, program_id, degprog_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            program_id = parse_qs(parsed.query)['program_id'][0]
            sql = '''SELECT program_code, program_name, program_description FROM programs WHERE program_id=%s'''
            values = (program_id, )
            columns = ['program_code', 'program_name', 'program_description']
            df = securequerydatafromdatabase(sql, values, columns)

            degprog_code = df["program_code"][0]
            degprog_name = df["program_name"][0]
            degprog_desc = df["program_description"][0]

            values = [degprog_code, degprog_name, degprog_desc, "Edit Existing Degree Program",
                      "Save Changes", program_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", degprog_process_editmodalhead,
                      degprog_submit, program_id, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("degprog_code", "valid"),
        Output("degprog_code", "invalid"),
        Output("degprog_name", "valid"),
        Output("degprog_name", "invalid"),
        Output("degprog_desc", "valid"),
        Output("degprog_desc", "invalid"),
        Output('degprog_submit_status', "value"),
        Output('degprog_results_modal', "is_open"),
        Output('degprog_results_body', "children"),
        Output('degprog_results_head_close', "style"),
        Output('degprog_results_head_return', "style"),
    ],
    [
        Input('degprog_submit', 'n_clicks'),
        Input('btn_degprog_head_close', 'n_clicks'),
        Input('btn_degprog_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('degprog_code', 'value'),
        State('degprog_name', 'value'),
        State('degprog_desc', 'value'),
        State("degprog_submit", "children"),
        State("degprog_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('program_id', 'value'),
    ]

)
def processdata(degprog_submit, btn_degprog_head_close, btn_degprog_results_head_return,
                current_user_id, degprog_code, degprog_name, degprog_desc, mode, degprog_chkmarkfordeletion, url, program_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,
            False, False,
            False, False

        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'degprog_submit':
            if degprog_code:
                if len(degprog_code) == 0:
                    is_valid_degprog_code = False
                else:
                    is_valid_degprog_code = True
            else:
                is_valid_degprog_code = False

            if degprog_name:
                if len(degprog_name) == 0:
                    is_valid_degprog_name = False
                else:
                    is_valid_degprog_name = True
            else:
                is_valid_degprog_name = False

            if degprog_desc:
                if len(degprog_desc) == 0:
                    is_valid_degprog_desc = False
                else:
                    is_valid_degprog_desc = True
            else:
                is_valid_degprog_desc = False

            validity = [
                is_valid_degprog_code, not is_valid_degprog_code,
                is_valid_degprog_name, not is_valid_degprog_name,
                is_valid_degprog_desc, not is_valid_degprog_desc

            ]
            allvalid = [is_valid_degprog_code, is_valid_degprog_name, is_valid_degprog_desc]
            if all(allvalid):
                if mode == "Save New Degree Program Name":
                    sql = """
                        INSERT INTO programs (program_code, program_name, program_description, program_inserted_by, program_inserted_on, program_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING program_id
                    """
                    values = (degprog_code, degprog_name, degprog_desc,
                              current_user_id, datetime.now(), False)
                    program_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new degree program"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE programs SET program_code = %s, program_name = %s, program_description = %s,
                            program_delete_ind= %s, program_inserted_by= %s, program_inserted_on= %s WHERE
                            program_id = %s
                    """
                    if '1' in degprog_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (degprog_code, degprog_name, degprog_desc, fordelete,
                              current_user_id, datetime.now(), program_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False,
                        False, False,
                        False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited degree program"
                    status = "1"
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display': 'inline'}
                stylehead_return = {'display': 'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out

            return out
        elif eventid == 'btn_degprog_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display': 'inline'}
            stylehead_return = {'display': 'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
