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
                html.H4("Add New Module", id="module_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dcc.ConfirmDialog(
                id='module_usermessage',
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Modules", id="module_results_head"),
                dbc.ModalBody([
                ], id="module_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_module_head_close",
                                       color="primary", block=True),
                        ], id="modules_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_module_results_head_return",
                                       color="primary", block=True, href='/settings/settings_modules'),
                        ], id="modules_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="modules_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Modules', href='/settings/settings_modules'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dcc.Markdown('''NOTE: By default, saving a new module will set it to OPEN status, meaning available for usage.''',
                                     style={'font-style': 'italic'})
                    ])
                ]),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Module Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="module_name", placeholder="Enter module name"
                             ),
                             dbc.FormFeedback(
                                 "Too short, already taken, or has spaces", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Module Link", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="module_link", placeholder="Enter module link"
                             ),
                             dbc.FormFeedback(
                                 "Too short, already taken, or has spaces", valid=False)

                         ], width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Module Header", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="module_header", placeholder="Enter module header"
                             ),
                             dbc.FormFeedback(
                                 "please enter a valid module header text", valid=False)
                         ], width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Module Icon", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="module_icon", placeholder="Enter icon name"
                             ),
                             dbc.FormText(
                                 "Search for icons in Font Awesome: https://fontawesome.com/icons?d=gallery",
                                 color="secondary",
                             ),
                             dbc.FormFeedback(
                                 "Please enter a valid module icon in text", valid=False)
                         ], width=8
                        )],
                        row=True
                    ),
                    html.Br(),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': '  Module is Open?', 'value': '1'},
                            ], id='module_is_open', value=[]
                        ),
                    ], id='divmoduleisopen',  style={'text-align': 'middle', 'display': 'inline'}),
                    html.Br(),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': '  Invisible from Sidebar?', 'value': '1'},
                            ], id='module_is_report', value=[]
                        ),
                    ], style={'text-align': 'middle', 'display': 'inline'}),


                    html.Br(),

                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': '  Mark for Deletion?', 'value': '1'},
                            ], id='module_chkmarkfordeletion', value=[]
                        ),
                    ], id='divmoduledelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Module", id="module_submit", color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="module_cancel",
                                   color="secondary", className="ml-auto", href='/settings/settings_modules')
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='module_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='module_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='module_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('module_name', 'value'),
        Output('module_link', 'value'),
        Output('module_header', 'value'),
        Output('module_icon', 'value'),
        Output("module_process_editmodalhead", "children"),
        Output("module_submit", "children"),
        Output("module_id", 'value'),
        Output('module_is_report', 'value'),
        Output("module_chkmarkfordeletion", "value"),
        Output("module_is_open", "value"),
        Output("divmoduledelete", "style"),
        Output("divmoduleisopen", "style"),

    ],
    [
        Input('module_submit_status', 'value'),
        Input('btn_module_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('module_name', 'value'),
        State('module_link', 'value'),
        State('module_header', 'value'),
        State('module_icon', 'value'),
        State('module_process_editmodalhead', "children"),
        State("module_submit", "children"),
        State("module_id", 'value'),
        State("module_chkmarkfordeletion", "value"),
        State("module_is_open", "value"),
    ]

)
def cleardata(module_submit_status, btn_module_head_close, url,
              module_name, module_link, module_header, module_icon, module_process_editmodalhead, module_submit, module_id, module_chkmarkfordeletion, module_is_open):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            module_id = parse_qs(parsed.query)['module_id'][0]
            sql = '''SELECT module_name, module_link, module_header, module_is_report, module_icon, module_is_open FROM modules WHERE module_id=%s'''
            values = (module_id,)
            columns = ["module_name", "module_link",
                       "module_header", "module_is_report", "module_icon", "module_is_open"]
            df = securequerydatafromdatabase(sql, values, columns)
            module_name = df["module_name"][0]
            module_link = df["module_link"][0]
            module_header = df["module_header"][0]
            module_is_report = df["module_is_report"][0]
            module_icon = df["module_icon"][0]
            module_is_open = df["module_is_open"][0]

            if module_is_report:
                module_is_report_return = ['1']
            else:
                module_is_report_return = []

            if module_is_open == True:
                module_is_open_return = ['1']
            else:
                module_is_open_return = []

            values = [module_name, module_link, module_header, module_icon, "Edit Existing Module:", "Save Changes",
                      module_id, module_is_report_return, [], module_is_open_return, {'text-align': 'middle', 'display': 'inline'}, {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", "", module_process_editmodalhead,
                      module_submit, module_id, [], [], [], {'display': 'none'}, {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("module_name", "valid"),
        Output("module_name", "invalid"),
        Output("module_link", "valid"),
        Output("module_link", "invalid"),
        Output("module_header", "valid"),
        Output("module_header", "invalid"),
        Output('module_submit_status', "value"),
        Output('modules_results_modal', "is_open"),
        Output('module_results_body', "children"),
        Output('modules_results_head_close', "style"),
        Output('modules_results_head_return', "style"),
    ],
    [
        Input('module_submit', 'n_clicks'),
        Input('btn_module_head_close', 'n_clicks'),
        Input('btn_module_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('module_name', 'value'),
        State('module_link', 'value'),
        State('module_header', 'value'),
        State('module_icon', 'value'),
        State("module_submit", "children"),
        State('module_is_report', 'value'),
        State("module_chkmarkfordeletion", "value"),
        State("module_is_open", "value"),
        State("url", "search"),
        State('module_id', 'value'),
    ]

)
def processdata(module_submit, btn_module_head_close, btn_module_results_head_return,
                current_user_id, module_name, module_link, module_header, module_icon, mode, module_is_report, module_chkmarkfordeletion, module_is_open, url, module_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False,
            False, False, False,
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'module_submit':
            if module_name:
                is_valid_module_name = True
            else:
                is_valid_module_name = False
            if module_link:
                is_valid_module_link = True
            else:
                is_valid_module_link = False
            if module_header:
                is_valid_bank_module_header = True
            else:
                is_valid_bank_module_header = False

            validity = [
                is_valid_module_name, not is_valid_module_name,
                is_valid_module_link, not is_valid_module_link,
                is_valid_bank_module_header, not is_valid_bank_module_header
            ]
            allvalid = [is_valid_module_name, is_valid_module_link, is_valid_bank_module_header]

            if all(allvalid):

                if mode == "Save New Module":
                    sql = """
                        INSERT INTO modules (module_name, module_link, module_header, module_icon, module_delete_ind,
                        module_modified_by, module_modified_on, module_is_report, module_is_open)
                        VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
                        RETURNING module_id
                    """

                    if '1' in module_is_report:
                        is_report = True
                    else:
                        is_report = False

                    # if '1' in module_is_open:
                    #     is_open = True
                    # else:
                    #     is_open = False

                    values = (module_name, module_link, module_header, module_icon, False,
                              current_user_id, datetime.now(), is_report, True)
                    module_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new module"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE modules SET module_name = %s, module_link= %s, module_header= %s, module_icon = %s,
                            module_delete_ind= %s, module_modified_by= %s, module_modified_on= %s, module_is_report = %s, module_is_open = %s
                            WHERE module_id = %s
                    """
                    if '1' in module_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False

                    if '1' in module_is_report:
                        is_report = True
                    else:
                        is_report = False

                    if '1' in module_is_open:
                        is_open = True
                    else:
                        is_open = False

                    values = (module_name, module_link, module_header, module_icon, fordelete,
                              current_user_id, datetime.now(), is_report, is_open, module_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False,
                        False, False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited module"
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
        elif eventid == 'btn_module_head_close':
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
