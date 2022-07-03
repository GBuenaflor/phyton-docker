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
                html.H4(" ", id="admin_emp_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Edit Admin Employees", id="admin_emp_results_head"),
                dbc.ModalBody([
                ], id="admin_emp_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_admin_emp_head_close",
                                       color="primary", block=True),
                        ], id="admin_emp_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_admin_emp_results_head_return",
                                       color="primary", block=True, href='/settings/settings_designation'),
                        ], id="admin_emp_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="admin_emp_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Admin Employee Assignment',
                         href='/settings/settings_admin_emp_assignment'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup([
                        dbc.Label("Employee Name", width=2,
                                  style={"text-align": "left"}),
                        dbc.Col([
                                html.H3("<content>", id="admin_emp_name"),
                                ], width=8)
                    ], row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Administrative Position", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="admin_emp_pos_name",
                                 options=[
                                 ],
                                 value="",
                                 searchable=True,
                                 clearable=True
                             ),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Administrative Position Unit", width=2, style={"text-align": "left"}),
                         #  dbc.Col([
                         #      dcc.Dropdown(
                         #          id="admin_emp_pos_unit",
                         #          options=[
                         #          ],
                         #          searchable=True,
                         #          clearable=True
                         #      ),
                         #  ],
                         #     width=8
                         # ),
                         dbc.Col([
                             html.H5("<content>", id="admin_emp_pos_unit"),
                         ], width=8)
                         ],
                        row=True
                    ),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Mark for Deletion?', 'value': '1'},
                            ], id='admin_emp_chkmarkfordeletion', value=[]
                        ),
                    ], id='divadminempdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save", id="admin_emp_submit",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="admin_emp_cancel",
                                   href='/settings/settings_admin_emp_assignment', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='admin_emp_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='admin_emp_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='admin_emp_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('admin_emp_name', 'children'),
        Output('admin_emp_pos_name', 'value'),
        Output('admin_emp_pos_unit', 'children'),
        Output("admin_emp_process_editmodalhead", "children"),
        Output("admin_emp_submit", "children"),
        Output("admin_emp_id", 'value'),
        Output("admin_emp_chkmarkfordeletion", "value"),
        Output("divadminempdelete", "style"),
    ],
    [
        Input('admin_emp_submit_status', 'value'),
        Input('btn_admin_emp_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('admin_emp_name', 'value'),
        State('admin_emp_pos_name', 'value'),
        State('admin_emp_pos_unit', 'value'),
        State('admin_emp_process_editmodalhead', "children"),
        State("admin_emp_submit", "children"),
        State("admin_emp_id", 'value'),
        State("admin_emp_chkmarkfordeletion", "value"),
    ]

)
def returnvalues(admin_emp_submit_status, btn_admin_emp_head_close,
                 url, admin_emp_name,
                 admin_emp_pos_name, admin_emp_pos_unit,
                 admin_emp_process_editmodalhead,
                 admin_emp_submit, admin_emp_id,
                 admin_emp_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            admin_emp_id = parse_qs(parsed.query)['admin_emp_id'][0]

            sql = '''SELECT ae.admin_emp_id, emp.emp_number, ap.admin_pos_id, ap.admin_pos_unit_id, un.unit_name, per.person_last_name || ', ' || per.person_first_name AS admin_emp_name,
						CASE
						WHEN ae.admin_emp_is_active = True THEN 'True'
						WHEN ae.admin_emp_is_active = False THEN 'False'
						ELSE ''
					END AS admin_emp_is_active
                      FROM admin_employees ae
					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                    INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                    INNER JOIN persons per ON per.person_id = emp.person_id
					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                     WHERE ae.admin_emp_id = %s
                  '''
            values = (admin_emp_id,)
            columns = ['admin_emp_id', 'emp_number', 'admin_pos_id', 'admin_pos_unit', 'unit_name',
                       'admin_emp_name', 'admin_emp_is_active']
            df = securequerydatafromdatabase(sql, values, columns)
            admin_pos_id = df["admin_pos_id"][0]
            admin_pos_unit = df["admin_pos_unit"][0]
            admin_emp_id = df["admin_emp_id"][0]
            admin_emp_name = df["admin_emp_name"][0]
            unit_name = df["unit_name"][0]
            values = [admin_emp_name, admin_pos_id, unit_name, "Edit Existing Administrative Employee",
                      "Save Changes", admin_emp_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("admin_emp_pos_name", "valid"),
        Output("admin_emp_pos_name", "invalid"),
        # Output("admin_emp_pos_unit", "valid"),
        # Output("admin_emp_pos_unit", "invalid"),

        Output('admin_emp_submit_status', "value"),
        Output('admin_emp_results_modal', "is_open"),
        Output('admin_emp_results_body', "children"),
        Output('admin_emp_results_head_close', "style"),
        Output('admin_emp_results_head_return', "style"),
    ],
    [
        Input('admin_emp_submit', 'n_clicks'),
        Input('btn_admin_emp_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('admin_emp_pos_name', 'value'),
        # State("admin_emp_pos_unit", "value"),
        State("admin_emp_submit", "children"),
        State("admin_emp_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('admin_emp_id', 'value'),
    ]

)
def saveadminempchanges(admin_emp_submit, btn_admin_emp_results_head_return,
                        current_user_id, admin_emp_pos_name,  # admin_emp_pos_unit,
                        mode, admin_emp_chkmarkfordeletion, url, admin_emp_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,  # False, False,  # False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'admin_emp_submit':

            if admin_emp_pos_name:
                is_valid_admin_emp_pos_name = True
            else:
                is_valid_admin_emp_pos_name = False

            # if admin_emp_pos_unit:
            #     is_valid_admin_emp_pos_unit = True
            # else:
            #     is_valid_admin_emp_pos_unit = True

            validity = [
                is_valid_admin_emp_pos_name, not is_valid_admin_emp_pos_name,
                # is_valid_admin_emp_pos_unit, not is_valid_admin_emp_pos_unit,

            ]
            allvalid = [
                is_valid_admin_emp_pos_name,  # is_valid_admin_emp_pos_unit
            ]
            if all(allvalid):
                # if mode == "Save New Designation":
                #
                #     sql = """
                #         INSERT INTO designations (admin_emp_pos_name, admin_emp_pos_unit, admin_emp_class_id, admin_emp_delete_ind,
                #         admin_emp_inserted_by, admin_emp_inserted_on)
                #         VALUES (%s, %s, %s, %s, %s, %s)
                #         RETURNING admin_emp_id
                #     """
                #     values = (admin_emp_pos_name, admin_emp_pos_unit,
                #               admin_emp_class_id, False, current_user_id, datetime.now())
                #     admin_emp_id = modifydatabasereturnid(sql, values)
                #     displayed = True
                #     message = "Successfully added new designation"
                #     status = "1"
                #     stylehead_close = {'display': 'inline'}
                #     stylehead_return = {'display': 'none'}
                # else:
                sql = """
                    UPDATE admin_employees
                    SET admin_pos_id = %s,
                        admin_emp_delete_ind= %s,
                        admin_emp_inserted_by= %s,
                        admin_emp_inserted_on= %s
                    WHERE
                        admin_emp_id = %s
                    """

                if '1' in admin_emp_chkmarkfordeletion:
                    fordelete = True
                else:
                    fordelete = False

                values = (admin_emp_pos_name, fordelete,
                          current_user_id, datetime.now(), admin_emp_id)

                modifydatabase(sql, values)
                validity = [
                    False, False,  # False, False,  # False, False
                ]
                stylehead_close = {'display': 'none'}
                stylehead_return = {'display': 'inline'}
                displayed = True
                message = "Successfully edited Admin Position Employee"
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
        elif eventid == 'btn_admin_emp_head_close':
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


@app.callback(
    [
        Output('admin_emp_pos_name', 'options'),
        #Output('admin_emp_pos_unit', 'options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
        State('sessioncurrentunit', 'data'),
        State('sessionlistofunits', 'data'),
    ],)
def admin_emp_fillindropdowns(path, url, sessioncurrentunit, sessionlistofunits):
    parsed = urlparse.urlparse(url)
    if path == "/settings/settings_admin_emp_assignment_profile":

        positions = commonmodules.queryfordropdown('''
            SELECT designation_name || ' - ' || un.unit_name AS admin_pos_name, admin_pos_id
              FROM admin_positions ap
            INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
			INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
             WHERE admin_pos_delete_ind = %s
            ORDER BY admin_pos_name
        ''', (False, ))

        # listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
        # units = commonmodules.queryfordropdown('''
        #     SELECT unit_name as label, unit_id as value
        #       FROM units un
        #      INNER JOIN admin_positions ap ON ap.admin_pos_unit_id = un.unit_id
        #      WHERE un.unit_delete_ind = %s
        #    ORDER BY unit_name
        # ''', (False, ))

        return [positions]
    else:
        raise PreventUpdate

#
# @app.callback([
#     Output('obpsalaryrate', 'value'),
# ],
#     [
#     Input('obppropsg', 'value'),
# ],)
# def toggle_divforeigncit(obppropsg):
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'obppropsg' and obppropsg:
#             sql = "SELECT salary_grade_amount FROM salary_grades WHERE salary_grade_id = %s"
#             values = (obppropsg,)
#             columns = ['salary_grade_amount']
#             dfsql = securequerydatafromdatabase(sql, values, columns)
#             return [dfsql['salary_grade_amount'][0]]
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate
