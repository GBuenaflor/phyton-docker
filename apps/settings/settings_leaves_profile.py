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
    html.H1("Leaves Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Leave", id="leave_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Leaves", id="leave_results_head"),
                dbc.ModalBody([
                ], id="leave_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_leave_head_close",
                                       color="primary", block=True),
                        ], id="leave_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_leave_results_head_return",
                                       color="primary", block=True, href='/settings/settings_leaves'),
                        ], id="leave_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="leave_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Leaves', href='/settings/settings_leaves'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Leave Type", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leave_name", placeholder="Enter Leave Type Name"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Leave Code", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leave_code", placeholder="Enter Leave Code"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    # dbc.FormGroup(
                    #     [dbc.Label(html.Div("Make inactive", id='labelleaveinactive'), width=2, style={"text-align": "left"}),
                    #      dbc.Col([
                    #          html.Div([
                    #              dcc.Checklist(
                    #                  options=[
                    #                      {'label': ' Inactive?', 'value': '1'},
                    #                  ], id='leave_chkmarkforinactive', value=[]
                    #              ),
                    #          ], id='divleaveinactive', style={'text-align': 'middle', 'display': 'inline'}),
                    #      ],
                    #         width=8
                    #     )],
                    #     row=True,
                    #
                    # ),


                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='leave_chkmarkfordeletion', value=[]
                        ),
                    ], id='divleavedelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Leave", id="leave_submit",
                                   color="info", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="leave_cancel",
                                   href='/settings/settings_leaves', color="warning", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='leave_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='leave_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='leave_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('leave_name', 'value'),
        Output('leave_code', 'value'),
        Output("leave_process_editmodalhead", "children"),
        Output("leave_submit", "children"),
        Output("leave_id", 'value'),
        # Output("leave_chkmarkforinactive", "value"),
        Output("leave_chkmarkfordeletion", "value"),
        # Output("labelleaveinactive", "style"),
        # Output("divleaveinactive", "style"),
        Output("divleavedelete", "style"),
    ],
    [
        Input('leave_submit_status', 'value'),
        Input('btn_leave_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('leave_name', 'value'),
        State('leave_code', 'value'),
        State('leave_process_editmodalhead', "children"),
        State("leave_submit", "children"),
        State("leave_id", 'value'),
        # State("leave_chkmarkforinactive", "value"),
        State("leave_chkmarkfordeletion", "value"),
    ]

)
def cleardata(leave_submit_status, btn_leave_head_close, url,
              leave_name, leave_code, leave_process_editmodalhead, leave_submit, leave_id,  # leave_chkmarkforinactive,
              leave_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            leave_id = parse_qs(parsed.query)['leave_id'][0]
            sql = '''SELECT leave_name, leave_code
                       FROM leaves
                      WHERE leave_id=%s'''
            values = (leave_id,)
            columns = ['leave_name', 'leave_code']
            df = securequerydatafromdatabase(sql, values, columns)
            leave_name = df["leave_name"][0]
            leave_code = df["leave_code"][0]
            values = [leave_name, leave_code, "Edit Existing Leave Type:",
                      "Save Changes", leave_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", leave_process_editmodalhead,
                      leave_submit, leave_id, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("leave_name", "valid"),
        Output("leave_name", "invalid"),
        Output("leave_code", "valid"),
        Output("leave_code", "invalid"),
        Output('leave_submit_status', "value"),
        Output('leave_results_modal', "is_open"),
        Output('leave_results_body', "children"),
        Output('leave_results_head_close', "style"),
        Output('leave_results_head_return', "style"),
    ],
    [
        Input('leave_submit', 'n_clicks'),
        Input('btn_leave_head_close', 'n_clicks'),
        Input('btn_leave_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('leave_name', 'value'),
        State("leave_code", "value"),
        State("leave_submit", "children"),
        # State("leave_chkmarkforinactive", "value"),
        State("leave_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('leave_id', 'value'),
    ]

)
def processdata(leave_submit, btn_leave_head_close, btn_leave_results_head_return,
                current_user_id, leave_name, leave_code, mode,  # leave_chkmarkforinactive,
                leave_chkmarkfordeletion, url, leave_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False,
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'leave_submit':
            if leave_name:
                is_valid_leave_name = True
            else:
                is_valid_leave_name = False
            if leave_code:
                is_valid_leave_code = True
            else:
                is_valid_leave_code = True

            validity = [
                is_valid_leave_name, not is_valid_leave_name,
                is_valid_leave_code, not is_valid_leave_code,
            ]
            allvalid = [is_valid_leave_name,  is_valid_leave_code, ]
            if all(allvalid):
                if mode == "Save New Leave":

                    sql = """
                        INSERT INTO leaves (leave_name, leave_code,  leave_delete_ind,
                                           leave_inserted_by, leave_inserted_on)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING leave_id
                    """
                    values = (leave_name, leave_code, False, current_user_id, datetime.now())
                    leave_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new leave type"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE leaves SET leave_name = %s, leave_code = %s,
                            leave_delete_ind= %s, leave_inserted_by= %s, leave_inserted_on= %s
                        WHERE leave_id = %s
                    """
                    # if '1' in leave_chkmarkforinactive:
                    #     forinactive = False
                    # else:
                    #     forinactive = True

                    if '1' in leave_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (leave_name, leave_code, fordelete, current_user_id,
                              datetime.now(), leave_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False,  False,
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited leave"
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
        elif eventid == 'btn_leave_head_close':
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
