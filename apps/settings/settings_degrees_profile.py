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
                html.H4("Add New Degree", id="degree_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Degrees", id="degree_results_head"),
                dbc.ModalBody([
                ], id="degree_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_degree_head_close",
                                       color="primary", block=True),
                        ], id="degrees_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_degree_results_head_return",
                                       color="primary", block=True, href='/settings/settings_degrees'),
                        ], id="degrees_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="degrees_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Degrees', href='/settings/settings_degrees'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Degree Code", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="degree_code", placeholder="Enter Degree Code"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Degree Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="degree_name", placeholder="Enter Degree Name"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Degree Description", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="degree_description", placeholder="Enter Degree Description"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Degree Level", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="degree_level",
                                    options=[
                                    ],
                                    # value="",
                                    searchable=True,
                                    clearable=True
                                )
                                #dbc.FormFeedback("Too short or already taken", valid = False)
                            ],
                                width=8
                            )],
                        row=True
                    ),


                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='degree_chkmarkfordeletion', value=[]
                        ),
                    ], id='divdegreedelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Degree", id="degree_submit", color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="degree_cancel", color="secondary",
                                   className="ml-auto", href='/settings/settings_degrees')
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='degree_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='degree_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='degree_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('degree_code', 'value'),
        Output('degree_name', 'value'),
        Output('degree_description', 'value'),
        Output('degree_level', 'value'),
        Output("degree_process_editmodalhead", "children"),
        Output("degree_submit", "children"),
        Output("degree_id", 'value'),
        Output("degree_chkmarkfordeletion", "value"),
        Output("divdegreedelete", "style"),
    ],
    [
        Input('degree_submit_status', 'value'),
        Input('btn_degree_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('degree_code', 'value'),
        State('degree_name', 'value'),
        State('degree_description', 'value'),
        State('degree_level', 'value'),
        State('degree_process_editmodalhead', "children"),
        State("degree_submit", "children"),
        State("degree_id", 'value'),
        State("degree_chkmarkfordeletion", "value"),
    ]

)
def cleardata(degree_submit_status, btn_degree_head_close, url,
              degree_code, degree_name, degree_description,
              degree_level,
              degree_process_editmodalhead, degree_submit, degree_id, degree_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            degree_id = parse_qs(parsed.query)['degree_id'][0]
            sql = '''SELECT degree_code, degree_name, degree_description, degree_level_id FROM degrees WHERE degree_id=%s'''
            values = (degree_id, )
            columns = ['degree_code', 'degree_name', 'degree_description', 'degree_level_id']
            df = securequerydatafromdatabase(sql, values, columns)
            degree_code = df["degree_code"][0]
            degree_name = df["degree_name"][0]
            degree_description = df["degree_description"][0]
            degree_level = df["degree_level_id"][0]
            values = [degree_code, degree_name, degree_description, degree_level, "Edit Existing Degree",
                      "Save Changes", degree_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", "", degree_process_editmodalhead,
                      degree_submit, degree_id, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("degree_code", "valid"),
        Output("degree_code", "invalid"),
        Output("degree_name", "valid"),
        Output("degree_name", "invalid"),
        Output("degree_description", "valid"),
        Output("degree_description", "invalid"),
        Output("degree_level", "valid"),
        Output("degree_level", "invalid"),
        Output('degree_submit_status', "value"),
        Output('degrees_results_modal', "is_open"),
        Output('degree_results_body', "children"),
        Output('degrees_results_head_close', "style"),
        Output('degrees_results_head_return', "style"),
    ],
    [
        Input('degree_submit', 'n_clicks'),
        Input('btn_degree_head_close', 'n_clicks'),
        Input('btn_degree_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('degree_code', 'value'),
        State('degree_name', 'value'),
        State('degree_description', 'value'),
        State('degree_level', 'value'),
        State("degree_submit", "children"),
        State("degree_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('degree_id', 'value'),
    ]

)
def processdata(degree_submit, btn_degree_head_close, btn_degree_results_head_return,
                current_user_id, degree_code, degree_name, degree_description, degree_level, mode, degree_chkmarkfordeletion, url, degree_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,
            False, False,
            False, False,
            False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'degree_submit':
            if degree_code:
                if len(degree_code) == 0:
                    is_valid_degree_code = False
                else:
                    is_valid_degree_code = True
            else:
                is_valid_degree_code = False

            if degree_name:
                if len(degree_name) == 0:
                    is_valid_degree_name = False
                else:
                    is_valid_degree_name = True
            else:
                is_valid_degree_name = False

            if degree_description:
                if len(degree_description) == 0:
                    is_valid_degree_description = False
                else:
                    is_valid_degree_description = True
            else:
                is_valid_degree_description = False

            if degree_level:
                is_valid_degree_level = True
            else:
                is_valid_degree_level = False

            validity = [
                is_valid_degree_code, not is_valid_degree_code,
                is_valid_degree_name, not is_valid_degree_name,
                is_valid_degree_description, not is_valid_degree_description,
                is_valid_degree_level, not is_valid_degree_level,

            ]
            allvalid = [is_valid_degree_code, is_valid_degree_name,
                        is_valid_degree_description, is_valid_degree_level]
            if all(allvalid):
                if mode == "Save New Degree":
                    sql = """
                        INSERT INTO degrees (degree_code, degree_name, degree_description, degree_level_id, degree_delete_ind,
                        degree_inserted_by, degree_inserted_on)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING degree_id
                    """
                    values = (degree_code, degree_name, degree_description,
                              degree_level, False, current_user_id, datetime.now())
                    degree_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new degree"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE degrees SET degree_code = %s, degree_name = %s, degree_description = %s, degree_level_id = %s,
                            degree_delete_ind= %s, degree_inserted_by= %s, degree_inserted_on= %s WHERE
                            degree_id = %s
                    """
                    if '1' in degree_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (degree_code, degree_name, degree_description, degree_level,
                              fordelete, current_user_id, datetime.now(), degree_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False,
                        False, False,
                        False, False,
                        False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited degree"
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
        elif eventid == 'btn_degree_head_close':
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


@app.callback([
    Output('degree_level', 'options'),

],
    [
    Input('url', 'pathname'),
],
    [
    State('url', 'search'),
    # State('sessioncurrentunit', 'data'),
    # State('sessionlistofunits', 'data'),
    # State('admin_pos_id', 'data')

],)
def degree_level_fillindropdowns(path, url):
    parsed = urlparse.urlparse(url)
    if path == "/settings/settings_degrees_profile":
        # mode = str(parse_qs(parsed.query)['mode'][0])
        # if mode == "edit":
        #     admin_pos_load_data = 1
        # else:
        #     admin_pos_load_data = 2
        # listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

        degreelevel = commonmodules.queryfordropdown('''
            SELECT degree_level as label, degree_level_id as value
              FROM degree_levels dl
             WHERE dl.degree_level_delete_ind = %s
           ORDER BY degree_level
        ''', (False, ))

        return [degreelevel]
    else:
        raise PreventUpdate
