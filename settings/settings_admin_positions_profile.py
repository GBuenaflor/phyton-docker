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
                html.H4("Add New Administrative Positions", id="admin_pos_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Administrative Positions", id="admin_pos_results_head"),
                dbc.ModalBody([
                ], id="admin_pos_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_admin_pos_head_close",
                                       color="primary", block=True),
                        ], id="admin_pos_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_admin_pos_results_head_return",
                                       color="primary", block=True, href='/settings/settings_admin_positions'),
                        ], id="admin_pos_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="admin_pos_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Administrative Positions',
                         href='/settings/settings_admin_positions'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Administrative Position Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="admin_pos_name",
                                 options=[
                                 ],
                                 # value="",
                                 searchable=True,
                                 clearable=True,
                                 placeholder="Search for position first",
                             )
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=8
                        )
                        ],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Administrative Position Description", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="admin_pos_description", placeholder="Enter Administrative Position description"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Unit", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="admin_pos_unit",
                                    options=[
                                    ],
                                    # value="",
                                    searchable=True,
                                    clearable=True
                                )
                                #dbc.FormFeedback("Too short or already taken", valid = False)
                            ],
                                width=8
                            )
                        ],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Attach Role", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="admin_role_id",
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
                                {'label': 'Mark for Deletion?', 'value': '1'},
                            ], id='admin_pos_chkmarkfordeletion', value=[]
                        ),
                    ], id='divadminposdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Admin Position", id="admin_pos_submit",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="admin_pos_cancel",
                                   href='/settings/settings_admin_positions', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                html.Div([
                    dcc.Input(id='admin_pos_load_data', type='text', value="0")
                ], style={'display': 'none'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='admin_pos_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='admin_pos_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='admin_pos_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('admin_pos_name', 'value'),
        Output('admin_pos_description', 'value'),
        Output('admin_pos_unit', 'value'),
        Output("admin_pos_process_editmodalhead", "children"),
        Output("admin_pos_submit", "children"),
        Output("admin_pos_id", 'value'),
        Output('admin_role_id', 'value'),
        Output("admin_pos_chkmarkfordeletion", "value"),
        Output("divadminposdelete", "style"),
    ],
    [
        Input('admin_pos_submit_status', 'value'),
        Input('btn_admin_pos_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('admin_pos_name', 'value'),
        State('admin_pos_description', 'value'),
        State('admin_pos_unit', 'value'),
        State('admin_pos_process_editmodalhead', "children"),
        State("admin_pos_submit", "children"),
        State("admin_pos_id", 'value'),
        State("admin_pos_chkmarkfordeletion", "value"),
    ]

)
def clear_admin_pos_data(admin_pos_submit_status, btn_admin_pos_head_close, url,
              admin_pos_name, admin_pos_description, admin_pos_unit,
              admin_pos_process_editmodalhead, admin_pos_submit, admin_pos_id, admin_pos_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            admin_pos_id = parse_qs(parsed.query)['admin_pos_id'][0]
            sql = '''
                    SELECT designation_id, admin_pos_description, admin_pos_unit_id, admin_role_id
                       FROM admin_positions ap
                     INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                      WHERE admin_pos_id = %s
                  '''
            values = (admin_pos_id,)
            columns = ['designation_name', 'admin_pos_description',
                       'admin_pos_unit', 'admin_role_id']
            df = securequerydatafromdatabase(sql, values, columns)
            admin_pos_name = df["designation_name"][0]
            admin_pos_description = df["admin_pos_description"][0]
            admin_pos_unit = df["admin_pos_unit"][0]
            admin_role_id = df["admin_role_id"][0]

            values = [admin_pos_name, admin_pos_description, admin_pos_unit, "Edit Existing Admin Position:",
                      "Save Changes", admin_pos_id, admin_role_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", admin_pos_process_editmodalhead,
                      admin_pos_submit, admin_pos_id, "", [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("admin_pos_name", "valid"),
        Output("admin_pos_name", "invalid"),
        # Output("admin_pos_description", "valid"),
        # Output("admin_pos_description", "invalid"),
        Output("admin_pos_unit", "valid"),
        Output("admin_pos_unit", "invalid"),
        Output('admin_pos_submit_status', "value"),
        Output('admin_pos_results_modal', "is_open"),
        Output('admin_pos_results_body', "children"),
        Output('admin_pos_results_head_close', "style"),
        Output('admin_pos_results_head_return', "style"),
    ],
    [
        Input('admin_pos_submit', 'n_clicks'),
        Input('btn_admin_pos_head_close', 'n_clicks'),
        Input('btn_admin_pos_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('admin_pos_name', 'value'),
        State("admin_pos_description", "value"),
        State("admin_pos_unit", "value"),
        State("admin_pos_submit", "children"),
        State("admin_pos_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('admin_pos_id', 'value'),
        State('admin_role_id', 'value')
    ]

)
def process_admin_pos_data(admin_pos_submit, btn_admin_pos_head_close, btn_admin_pos_results_head_return,
                current_user_id, admin_pos_name, admin_pos_description, admin_pos_unit,
                mode, admin_pos_chkmarkfordeletion, url, admin_pos_id, admin_role_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,  False, False,  # False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'admin_pos_submit':
            if admin_pos_name:
                is_valid_admin_pos_name = True
            else:
                is_valid_admin_pos_name = False

            if admin_pos_unit:
                is_valid_admin_pos_unit = True
            else:
                is_valid_admin_pos_unit = False

            validity = [
                is_valid_admin_pos_name,
                not is_valid_admin_pos_name,
                is_valid_admin_pos_unit,
                not is_valid_admin_pos_unit,
            ]

            allvalid = [
                is_valid_admin_pos_name,
                is_valid_admin_pos_unit
            ]

            if admin_pos_name and admin_pos_unit and admin_pos_description and admin_role_id:
                #admin_pos_name_search = "%"+admin_pos_name_label+"%"
                admin_pos_name_search = admin_pos_name
                admin_pos_description_search = "%"+admin_pos_description+"%"
                if parse_qs(parsed.query)['mode'][0] == "add":
                    sqlcommand = '''
                                SELECT admin_designation_id, designation_name, admin_pos_description, un.unit_id, un.unit_name
                                  FROM admin_positions ap
                                INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                                INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                                 WHERE  admin_pos_unit_id = %s
                                   AND designation_id = %s
                                ORDER BY designation_name ASC
                            '''
                    values = (admin_pos_unit, admin_pos_name_search)
                elif parse_qs(parsed.query)['mode'][0] == "edit":
                    sqlcommand = '''
                                SELECT admin_designation_id, designation_name, admin_pos_description, un.unit_id, un.unit_name
                                  FROM admin_positions ap
                                INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                                INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                                 WHERE  admin_pos_unit_id = %s
                                   AND designation_id = %s
                                   AND admin_role_id = %s
                                ORDER BY designation_name ASC
                            '''
                    values = (admin_pos_unit, admin_pos_name_search, admin_role_id)
                columns = ['admin_designation_id', 'designation_name',
                           'admin_pos_description', 'unit_id', 'unit_name']
                df = securequerydatafromdatabase(sqlcommand, values, columns)

                if df.empty:
                    is_valid_admin_pos_name = True
                else:
                    is_valid_admin_pos_name = False
            else:
                is_valid_admin_pos_name = False

            if all(allvalid):
                if mode == "Save New Admin Position":
                    sql = """
                        INSERT INTO admin_positions (admin_designation_id, admin_pos_description, admin_pos_unit_id,
                        admin_pos_inserted_by, admin_pos_inserted_on, admin_pos_delete_ind, admin_role_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING admin_pos_id
                    """
                    values = (admin_pos_name, admin_pos_description, admin_pos_unit,
                              current_user_id, datetime.now(), False, admin_role_id)
                    admin_pos_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new admin position"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE admin_positions
                           SET admin_designation_id = %s,
                               admin_pos_description = %s,
                               admin_pos_unit_id = %s,
                               admin_pos_delete_ind = %s,
                               admin_pos_inserted_by = %s,
                               admin_pos_inserted_on= %s,
                               admin_role_id = %s
                         WHERE admin_pos_id = %s
                    """
                    if '1' in admin_pos_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (admin_pos_name, admin_pos_description, admin_pos_unit,
                              fordelete, current_user_id, datetime.now(), admin_role_id, admin_pos_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False,  False, False,  # False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited an admin position"
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
        elif eventid == 'btn_admin_pos_head_close':
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
    Output('admin_pos_unit', 'options'),
    Output('admin_pos_load_data', 'value'),
    Output('admin_pos_name', 'options'),
    Output('admin_role_id', 'options')
],
    [
    Input('url', 'pathname'),
    # Input("admin_pos_name", "search_value")
],
    [
    State('url', 'search'),
    State('sessioncurrentunit', 'data'),
    State('sessionlistofunits', 'data'),
    State('admin_pos_id', 'data')
],)
def admin_pos_fillindropdowns(path, url, sessioncurrentunit, sessionlistofunits, admin_pos_id):
    parsed = urlparse.urlparse(url)
    print("sessioncurrentunit", sessioncurrentunit)
    if path == "/settings/settings_admin_positions_profile":
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":
            admin_pos_load_data = 1
        else:
            admin_pos_load_data = 2
        listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

        units = commonmodules.queryfordropdown('''
            SELECT unit_name as label, unit_id as value
              FROM units un
             WHERE un.unit_delete_ind = %s
           ORDER BY unit_name
        ''', (False, ))

        positions = commonmodules.queryfordropdown('''
            SELECT designation_name AS LABEL, designation_id AS VALUE
              FROM designations design
             WHERE design.designation_delete_ind = %s
           ORDER BY designation_name
        ''', (False, ))

        roles = commonmodules.queryfordropdown('''
            SELECT role_name AS LABEL, role_id AS VALUE
              FROM roles r
             WHERE r.role_delete_ind = %s
           ORDER BY role_name
        ''', (False, ))

        # if not search_value:
        #     raise PreventUpdate
        # positions = [o for o in positions if search_value in o["label"]]

        return [units, admin_pos_load_data, positions, roles]
    else:
        raise PreventUpdate
