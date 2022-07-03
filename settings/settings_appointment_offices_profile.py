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
                html.H4("Add New Appointment Offices",
                        id="appointment_office_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Appointment Offices", id="appointment_office_results_head"),
                dbc.ModalBody([
                ], id="appointment_office_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_appointment_office_head_close",
                                       color="primary", block=True),
                        ], id="appointment_office_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_appointment_office_results_head_return",
                                       color="primary", block=True, href='/settings/settings_appointment_offices'),
                        ], id="appointment_office_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="appointment_office_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Appointment Offices',
                         href='/settings/settings_appointment_offices'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Appointment Office Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="appointment_office_name", placeholder="Enter trunkline"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Trunkline", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="appointment_office_trunkline", placeholder="Enter trunkline"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Telefax", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="appointment_office_telefax", placeholder="Enter telefax"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Email", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="appointment_office_email", placeholder="Enter email"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Website", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="appointment_office_website", placeholder="Enter website"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Direct Line", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="appointment_office_directline", placeholder="Enter directline"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Link Administrative Position",
                                      width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="appointment_office_admin_pos_dd",
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
                    # dbc.FormGroup(
                    #     [
                    #         dbc.Label("Unit", width=2, style={"text-align": "left"}),
                    #         dbc.Col([
                    #             dcc.Dropdown(
                    #                 id="appointment_office_admin_pos_dd",
                    #                 options=[
                    #                 ],
                    #                 # value="",
                    #                 searchable=True,
                    #                 clearable=True
                    #             )
                    #             #dbc.FormFeedback("Too short or already taken", valid = False)
                    #         ],
                    #             width=8
                    #         )
                    #     ],
                    #     row=True
                    # ),
                    # dbc.FormGroup(
                    #     [
                    #         dbc.Label("Attach Role", width=2, style={"text-align": "left"}),
                    #         dbc.Col([
                    #             dcc.Dropdown(
                    #                 id="admin_role_id",
                    #                 options=[
                    #                 ],
                    #                 # value="",
                    #                 searchable=True,
                    #                 clearable=True
                    #             )
                    #             #dbc.FormFeedback("Too short or already taken", valid = False)
                    #         ],
                    #             width=8
                    #         )],
                    #     row=True
                    # ),

                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Mark for Deletion?', 'value': '1'},
                            ], id='appointment_office_chkmarkfordeletion', value=[]
                        ),
                    ], id='divappointmentofficedelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Appointment Office", id="appointment_office_submit",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="appointment_office_cancel",
                                   href='/settings/settings_appointment_offices', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                html.Div([
                    dcc.Input(id='appointment_office_load_data', type='text', value="0")
                ], style={'display': 'none'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='appointment_office_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='appointment_office_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='appointment_office_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('appointment_office_name', 'value'),
        Output('appointment_office_trunkline', 'value'),
        Output('appointment_office_telefax', 'value'),
        Output('appointment_office_email', 'value'),
        Output('appointment_office_website', 'value'),
        Output('appointment_office_directline', 'value'),
        Output('appointment_office_admin_pos_dd', 'value'),
        Output("appointment_office_process_editmodalhead", "children"),
        Output("appointment_office_submit", "children"),
        Output("appointment_office_id", 'value'),
        Output("appointment_office_chkmarkfordeletion", "value"),
        Output("divappointmentofficedelete", "style"),
    ],
    [
        Input('appointment_office_submit_status', 'value'),
        Input('btn_appointment_office_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('appointment_office_name', 'value'),
        State('appointment_office_trunkline', 'value'),
        State('appointment_office_admin_pos_dd', 'value'),
        State('appointment_office_process_editmodalhead', "children"),
        State("appointment_office_submit", "children"),
        State("appointment_office_id", 'value'),
        State("appointment_office_chkmarkfordeletion", "value"),
    ]

)
def cleardata(appointment_office_submit_status, btn_appointment_office_head_close, url,
              appointment_office_name, appointment_office_trunkline, appointment_office_admin_pos_dd,
              appointment_office_process_editmodalhead, appointment_office_submit, appointment_office_id, appointment_office_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            appointment_office_id = parse_qs(parsed.query)['appointment_office_id'][0]
            sql = '''
                    SELECT office_id, office_name, office_trunkline, office_telefax, office_email, office_website, office_direct_line, ao.admin_pos_id
                      FROM appointment_offices ao
                    INNER JOIN admin_positions ap ON ap.admin_pos_id = ao.admin_pos_id
                    INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                    INNER JOIN units unn ON unn.unit_id = ap.admin_pos_unit_id
                     WHERE office_delete_ind = %s
                       AND designation_delete_ind = %s
                       AND unit_delete_ind = %s
                       AND office_id = %s
                  '''
            values = (False, False, False, appointment_office_id,)
            columns = ['office_id', 'office_name', 'office_trunkline', 'office_telefax',
                       'office_email', 'office_website', 'office_direct_line', 'admin_pos_id']
            df = securequerydatafromdatabase(sql, values, columns)
            appointment_office_name = df["office_name"][0]
            appointment_office_trunkline = df["office_trunkline"][0]
            appointment_office_telefax = df["office_telefax"][0]
            appointment_office_email = df["office_email"][0]
            appointment_office_website = df["office_website"][0]
            appointment_office_direct_line = df["office_direct_line"][0]
            admin_pos_id = df["admin_pos_id"][0]

            values = [appointment_office_name, appointment_office_trunkline, appointment_office_telefax, appointment_office_email,
                      appointment_office_website,  appointment_office_direct_line, admin_pos_id, "Edit Existing Appointment Office",
                      "Save Changes", appointment_office_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", "", "", "", "", appointment_office_process_editmodalhead,
                      "Save New Appointment Office", appointment_office_id, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("appointment_office_name", "valid"),
        Output("appointment_office_name", "invalid"),
        Output("appointment_office_trunkline", "valid"),
        Output("appointment_office_trunkline", "invalid"),
        Output('appointment_office_telefax', 'valid'),
        Output('appointment_office_telefax', 'invalid'),
        Output('appointment_office_email', 'valid'),
        Output('appointment_office_email', 'invalid'),
        Output('appointment_office_website', 'valid'),
        Output('appointment_office_website', 'invalid'),
        Output('appointment_office_directline', 'valid'),
        Output('appointment_office_directline', 'invalid'),
        Output("appointment_office_admin_pos_dd", "valid"),
        Output("appointment_office_admin_pos_dd", "invalid"),
        Output('appointment_office_submit_status', "value"),
        Output('appointment_office_results_modal', "is_open"),
        Output('appointment_office_results_body', "children"),
        Output('appointment_office_results_head_close', "style"),
        Output('appointment_office_results_head_return', "style"),
    ],
    [
        Input('appointment_office_submit', 'n_clicks'),
        Input('btn_appointment_office_head_close', 'n_clicks'),
        Input('btn_appointment_office_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('appointment_office_name', 'value'),
        State("appointment_office_trunkline", "value"),
        State('appointment_office_telefax', 'value'),
        State('appointment_office_email', 'value'),
        State('appointment_office_website', 'value'),
        State('appointment_office_directline', 'value'),
        State("appointment_office_admin_pos_dd", "value"),
        State("appointment_office_submit", "children"),
        State("appointment_office_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('appointment_office_id', 'value'),
    ]
)
def processdata(appointment_office_submit, btn_appointment_office_head_close, btn_appointment_office_results_head_return,
                current_user_id, appointment_office_name, appointment_office_trunkline,
                appointment_office_telefax, appointment_office_email, appointment_office_website, appointment_office_directline,
                appointment_office_admin_pos_dd,
                mode, appointment_office_chkmarkfordeletion, url, appointment_office_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,  False, False,
            False, False,  False, False,
            False, False,  False, False,
            False, False,
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'appointment_office_submit':
            if appointment_office_name:
                is_valid_appointment_office_name = True
            else:
                is_valid_appointment_office_name = False

            if appointment_office_trunkline:
                is_valid_appointment_office_trunkline = True
            else:
                is_valid_appointment_office_trunkline = False

            if appointment_office_telefax:
                is_valid_appointment_office_telefax = True
            else:
                is_valid_appointment_office_telefax = False

            if appointment_office_email:
                is_valid_appointment_office_email = True
            else:
                is_valid_appointment_office_email = False

            if appointment_office_website:
                is_valid_appointment_office_website = True
            else:
                is_valid_appointment_office_website = False

            if appointment_office_directline:
                is_valid_appointment_office_directline = True
            else:
                is_valid_appointment_office_directline = False

            if appointment_office_admin_pos_dd:
                is_valid_appointment_office_admin_pos_dd = True
            else:
                is_valid_appointment_office_admin_pos_dd = False

            validity = [
                is_valid_appointment_office_name, not is_valid_appointment_office_name,
                is_valid_appointment_office_trunkline, not is_valid_appointment_office_trunkline,
                is_valid_appointment_office_telefax, not is_valid_appointment_office_telefax,
                is_valid_appointment_office_email, not is_valid_appointment_office_email,
                is_valid_appointment_office_website, not is_valid_appointment_office_website,
                is_valid_appointment_office_directline, not is_valid_appointment_office_directline,
                is_valid_appointment_office_admin_pos_dd, not is_valid_appointment_office_admin_pos_dd,
            ]

            allvalid = [
                is_valid_appointment_office_name,
                is_valid_appointment_office_trunkline,
                is_valid_appointment_office_telefax,
                is_valid_appointment_office_email,
                is_valid_appointment_office_website,
                is_valid_appointment_office_directline,
                is_valid_appointment_office_admin_pos_dd
            ]

            if appointment_office_name and appointment_office_admin_pos_dd:
                #appointment_office_name_search = "%"+appointment_office_name_label+"%"
                appointment_office_name_search = "%"+appointment_office_name+"%"
                # appointment_office_trunkline_search = "%"+appointment_office_trunkline+"%"
                appointment_office_admin_pos_dd_search = appointment_office_admin_pos_dd

                if parse_qs(parsed.query)['mode'][0] == "add":
                    sqlcommand = '''
                                SELECT office_id, office_name, office_trunkline, office_telefax, office_email, office_website, office_direct_line, ao.admin_pos_id
                                  FROM appointment_offices ao
                                INNER JOIN admin_positions ap ON ap.admin_pos_id = ao.admin_pos_id
                                INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                                INNER JOIN units unn ON unn.unit_id = ap.admin_pos_unit_id
                                  WHERE office_delete_ind = %s
                                   AND designation_delete_ind = %s
                                   AND unit_delete_ind = %s
                                   AND office_name ILIKE %s
                                   AND ao.admin_pos_id = %s
                                ORDER BY office_name ASC
                            '''
                    values = (False, False, False, appointment_office_name_search,
                              appointment_office_admin_pos_dd_search)

                elif parse_qs(parsed.query)['mode'][0] == "edit":
                    sqlcommand = '''
                                SELECT office_id, office_name, office_trunkline, office_telefax, office_email, office_website, office_direct_line, ao.admin_pos_id
                                  FROM appointment_offices ao
                                INNER JOIN admin_positions ap ON ap.admin_pos_id = ao.admin_pos_id
                                INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                                INNER JOIN units unn ON unn.unit_id = ap.admin_pos_unit_id
                                  WHERE office_delete_ind = %s
                                   AND designation_delete_ind = %s
                                   AND unit_delete_ind = %s
                                   AND office_name ILIKE %s
                                   AND ao.admin_pos_id = %s
                                   AND ao.office_id <> %s
                                ORDER BY office_name ASC
                            '''
                    values = (False, False, False, appointment_office_name_search,
                              appointment_office_admin_pos_dd_search, appointment_office_id)
                columns = ['office_id', 'office_name', 'office_trunkline', 'office_telefax',
                           'office_email', 'office_website', 'office_direct_line', 'admin_pos_id']
                df = securequerydatafromdatabase(sqlcommand, values, columns)

                if df.empty:
                    is_valid_appointment_office_name = True
                    is_valid_appointment_office_trunkline = True
                    is_valid_appointment_office_telefax = True
                    is_valid_appointment_office_email = True
                    is_valid_appointment_office_website = True
                    is_valid_appointment_office_directline = True
                    is_valid_appointment_office_admin_pos_dd = True
                else:
                    is_valid_appointment_office_name = False
                    is_valid_appointment_office_trunkline = False
                    is_valid_appointment_office_telefax = False
                    is_valid_appointment_office_email = False
                    is_valid_appointment_office_website = False
                    is_valid_appointment_office_directline = False
                    is_valid_appointment_office_admin_pos_dd = False
            else:
                is_valid_appointment_office_name = False
                is_valid_appointment_office_trunkline = False
                is_valid_appointment_office_telefax = False
                is_valid_appointment_office_email = False
                is_valid_appointment_office_website = False
                is_valid_appointment_office_directline = False
                is_valid_appointment_office_admin_pos_dd = False

            if all(allvalid):
                if mode == "Save New Appointment Office":
                    sql = """
                        INSERT INTO appointment_offices (office_name, office_trunkline, office_telefax, office_email, office_website, office_direct_line,
                                                        admin_pos_id, office_inserted_by, office_inserted_on, office_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING office_id
                    """
                    values = (appointment_office_name, appointment_office_trunkline,
                              appointment_office_telefax, appointment_office_email,
                              appointment_office_website, appointment_office_directline,
                              appointment_office_admin_pos_dd,
                              current_user_id, datetime.now(), False)
                    appointment_office_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new appointment office"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE appointment_offices
                           SET office_name = %s,
                           	   office_trunkline = %s,
                        	   office_telefax = %s,
                        	   office_email = %s,
                        	   office_website = %s,
                        	   office_direct_line = %s,
                        	   admin_pos_id = %s,
                               office_delete_ind = %s,
                               office_modified_by = %s,
                               office_modified_on = %s
                         WHERE office_id = %s
                    """
                    if '1' in appointment_office_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (appointment_office_name, appointment_office_trunkline,
                              appointment_office_telefax, appointment_office_email,
                              appointment_office_website, appointment_office_directline,
                              appointment_office_admin_pos_dd,
                              fordelete, current_user_id, datetime.now(), appointment_office_id)
                    modifydatabase(sql, values)
                    # validity = [
                    #     # False, False,  False, False,
                    #     # False, False,  False, False,
                    #     # False, False,  False, False,
                    #     # False, False,
                    # ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited an appointment office"
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
        elif eventid == 'btn_appointment_office_head_close':
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
    Output('appointment_office_admin_pos_dd', 'options'),
    # Output('appointment_office_load_data', 'value'),
    # Output('appointment_office_name', 'options'),
    # Output('admin_role_id', 'options')
],
    [
    Input('url', 'pathname'),
    # Input("appointment_office_name", "search_value")
],
    [
    State('url', 'search'),
    State('sessioncurrentunit', 'data'),
    State('sessionlistofunits', 'data'),
    State('appointment_office_id', 'data')
],)
def appointment_office_fillindropdowns(path, url, sessioncurrentunit, sessionlistofunits, appointment_office_id):
    parsed = urlparse.urlparse(url)
    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    if path == "/settings/settings_appointment_offices_profile":
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":
            appointment_office_load_data = 1
            positions = commonmodules.queryfordropdown('''
                SELECT design.designation_name || ' - ' || unn.unit_name AS label, admin_pos_id AS value
                  FROM admin_positions ap
                INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                INNER JOIN units unn ON unn.unit_id = ap.admin_pos_unit_id
                 WHERE admin_pos_delete_ind = %s
                   AND designation_delete_ind = %s
                   AND unn.unit_delete_ind = %s
                   AND admin_pos_id NOT IN (SELECT DISTINCT admin_pos_id
                                              FROM appointment_offices
                                             WHERE office_delete_ind = %s
                                               AND office_id = %s)
            ''', (False, False, False, False, appointment_office_id))
        else:
            appointment_office_load_data = 2
            positions = commonmodules.queryfordropdown('''
                SELECT design.designation_name || ' - ' || unn.unit_name AS label, admin_pos_id AS value
                  FROM admin_positions ap
                INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                INNER JOIN units unn ON unn.unit_id = ap.admin_pos_unit_id
                 WHERE admin_pos_delete_ind = %s
                   AND designation_delete_ind = %s
                   AND unn.unit_delete_ind = %s
                   AND admin_pos_id NOT IN (SELECT DISTINCT admin_pos_id
                                              FROM appointment_offices
                                             WHERE office_delete_ind = %s)
            ''', (False, False, False, False))

        return [positions]
    else:
        raise PreventUpdate
