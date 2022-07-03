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
                html.H4("Add New Unit", id="unit_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Units", id="unit_results_head"),
                dbc.ModalBody([
                ], id="unit_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_unit_head_close",
                                       color="primary", block=True),
                        ], id="unit_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_unit_results_head_return",
                                       color="primary", block=True, href='/settings/settings_units'),
                        ], id="unit_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="unit_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Units', href='/settings/settings_units'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Unit Name*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="unit_name", placeholder="Enter unit Name"
                             ),
                             dbc.FormFeedback("Enter a valid unit name", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Unit Code*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="unit_code", placeholder="Enter Unit Code"
                             ),
                             dbc.FormFeedback("Enter a valid unit code", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Parent Unit*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="unit_parentunit",
                                 options=[
                                    # {'label': 'Faculty', 'value': '1'},
                                    # {'label': 'Administrative Personnel', 'value': '2'},
                                    # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                    # {'label': 'Others', 'value': '11'}
                                 ],
                                 searchable=True
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Academic/Non-Academic*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="unit_academic",
                                 options=[
                                     {'label': 'Academic', 'value': '1'},
                                     {'label': 'Non-Academic', 'value': '2'},
                                 ],
                                 searchable=True
                             ),
                             # dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Unit Abbreviation*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="unit_abbrev", placeholder="Enter Unit Abbreviation"
                             ),
                             dbc.FormFeedback("Enter a valid unit abbreviation", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("BP Unit Approval Type*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="unit_approvaltype",
                                 options=[
                                     {'label': 'Unit/CPC Level Only', 'value': '1'},
                                     {'label': 'DPC Level', 'value': '2'},
                                 ],
                                 searchable=True
                             ),
                             # dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=8
                         )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Leave Unit Approval Type*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leave_unit_approvaltype",
                                 options=[
                                    {'label': 'Leave Recommending Authority Only', 'value': '3'},
                                    {'label': 'Leave Approver Only', 'value': '1'},
                                    {'label': 'Leave Recommending Authority & Leave Approver', 'value': '2'},

                                 ],
                                 searchable=True
                             ),
                             # dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=8
                         )],
                        row=True
                    ),


                    dbc.FormGroup(
                        [dbc.Label(html.Div("Active/Inactive*", id='labelunitinactive'), width=2,
                                   style={"text-align": "left"}),
                         dbc.Col([
                             # html.Div([
                             dcc.Checklist(
                                 options=[
                                     {'label': ' Unit is Active?', 'value': '1'},
                                 ], id='unit_active', value=[]
                             ),
                             # ], id='divunitinactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                             width=8
                         )],
                        row=True,
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Unit DBM Code", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="unit_dbmcode", placeholder="Enter Unit DBM Code"
                             ),
                             dbc.FormFeedback("Enter a valid unit DBM code", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Unit DBM Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="unit_dbmname", placeholder="Enter Unit DBM Name"
                             ),
                             dbc.FormFeedback("Enter a valid unit DBM name", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label(html.Div("Dummy Unit?", id='labelunitdummy'), width=2,
                                   style={"text-align": "left"}),
                         dbc.Col([
                             # html.Div([
                             dcc.Checklist(
                                 options=[
                                     {'label': ' Unit is Dummy?', 'value': '1'},
                                 ], id='unit_dummy', value=[]
                             ),
                             # ], id='divunitinactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                             width=8
                         )],
                        row=True,
                    ),

                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='unit_chkmarkfordeletion', value=[]
                        ),
                    ], id='divunitdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Unit", id="unit_submit",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="unit_cancel",
                                   href='/settings/settings_units', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='unit_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='unit_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='unit_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('unit_name', 'value'),
        Output('unit_code', 'value'),
        Output('unit_parentunit', 'value'),
        Output('unit_academic', 'value'),
        Output('unit_abbrev', 'value'),
        Output('unit_approvaltype', 'value'),
        Output('leave_unit_approvaltype', 'value'),
        Output('unit_active', 'value'),
        Output('unit_dbmcode', 'value'),
        Output('unit_dbmname', 'value'),
        Output('unit_dummy', 'value'),

        Output("unit_process_editmodalhead", "children"),
        Output("unit_submit", "children"),

        Output("unit_chkmarkfordeletion", "value"),
        Output("unit_chkmarkfordeletion", "style")


    ],
    [
        Input('unit_submit_status', 'value'),
        Input('btn_unit_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('unit_name', 'value'),
        State('unit_code', 'value'),
        State('unit_parentunit', 'value'),
        State('unit_academic', 'value'),
        State('unit_abbrev', 'value'),
        State('unit_approvaltype', 'value'),
        State('leave_unit_approvaltype', 'value'),
        State('unit_active', 'value'),
        State('unit_dbmcode', 'value'),
        State('unit_dbmname', 'value'),
        State('unit_dummy', 'value'),



        State('unit_process_editmodalhead', "children"),
        State("unit_submit", "children"),
        State("unit_chkmarkfordeletion", "value"),
    ]

)
def clear_unit_data(unit_submit_status, btn_unit_head_close, url,
              unit_name, unit_code, unit_parentunit, unit_academic,
              unit_abbrev, unit_approvaltype, leave_unit_approvaltype, unit_active, unit_dbmcode, unit_dbmname,
              unit_dummy,
              unit_process_editmodalhead, unit_submit, unit_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            unit_id = parse_qs(parsed.query)['unit_id'][0]
            sql = '''SELECT unit_name, unit_code, unit_parent_id, unit_is_academic, unit_abbrev, unit_approval_type_id, unit_leave_approval_type_id,
                    unit_is_active, unit_dbm_org_code, unit_dbm_name, unit_is_dummy
            FROM units
            WHERE unit_id=%s'''
            values = (unit_id,)
            columns = ['unit_name', 'unit_code', 'unit_parent_id', 'unit_is_academic', 'unit_abbrev', 'unit_approval_type_id', 'unit_leave_approval_type_id',
                    'unit_is_active', 'unit_dbm_org_code', 'unit_dbm_name', 'unit_is_dummy']
            df = securequerydatafromdatabase(sql, values, columns)

            unit_name = df["unit_name"][0]
            unit_code = df["unit_code"][0]
            unit_parent_id = df["unit_parent_id"][0]
            unit_is_academic_proxy = df["unit_is_academic"][0]
            if unit_is_academic_proxy == True:
                unit_is_academic = 1
            else:
                unit_is_academic = 2


            unit_abbrev = df["unit_abbrev"][0]
            unit_approval_type_id = df["unit_approval_type_id"][0]
            leave_unit_approval_type_id = df["unit_leave_approval_type_id"][0]

            unit_is_active_proxy = df["unit_is_active"][0]

            print('printing unit is active, ', unit_is_active_proxy)
            if unit_is_active_proxy == True:
                unit_is_active = ['1']
            else:
                unit_is_active = []
            print('printing unit is active, ', unit_is_active)

            unit_is_dummy_proxy = df["unit_is_dummy"][0]
            print('printing unit is dummy, ', unit_is_dummy_proxy)
            if unit_is_dummy_proxy == True:
                unit_is_dummy = ['1']
            else:
                unit_is_dummy = ['']
            print('printing unit is dummy, ', unit_is_dummy)

            unit_dbm_org_code = df["unit_dbm_org_code"][0]
            unit_dbm_name = df["unit_dbm_name"][0]



            values = [unit_name, unit_code, unit_parent_id, unit_is_academic, unit_abbrev, unit_approval_type_id, leave_unit_approval_type_id, unit_is_active, unit_dbm_org_code,
                      unit_dbm_name, unit_is_dummy,
                      "Edit Existing Unit",
                      "Save Changes",
                     [], {"display": "inline"}]

            return values

        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", "", "", "", "", "", [], "", "",
                      unit_process_editmodalhead,
                      unit_submit, [], {"display": "none"}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('unit_name', 'valid'),
        Output('unit_name', 'invalid'),
        Output('unit_code', 'valid'),
        Output('unit_code', 'invalid'),
        # Output('unit_parentunit', 'valid'),
        # Output('unit_parentunit', 'invalid'),
        Output('unit_academic', 'valid'),
        Output('unit_academic', 'invalid'),
        Output('unit_abbrev', 'valid'),
        Output('unit_abbrev', 'invalid'),
        Output('unit_approvaltype', 'valid'),
        Output('unit_approvaltype', 'invalid'),
        Output('leave_unit_approvaltype', 'valid'),
        Output('leave_unit_approvaltype', 'invalid'),
        # Output('unit_active', 'valid'),
        # Output('unit_active', 'invalid'),
        # Output('unit_dbmcode', 'valid'),
        # Output('unit_dbmcode', 'invalid'),
        # Output('unit_dbmname', 'valid'),
        # Output('unit_dbmname', 'invalid'),



        Output('unit_submit_status', "value"),
        Output('unit_results_modal', "is_open"),
        Output('unit_results_body', "children"),
        Output('unit_results_head_close', "style"),
        Output('unit_results_head_return', "style"),
    ],
    [
        Input('unit_submit', 'n_clicks'),
        Input('btn_unit_head_close', 'n_clicks'),
        Input('btn_unit_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),

        State('unit_name', 'value'),
        State('unit_code', 'value'),
        State('unit_parentunit', 'value'),
        State('unit_academic', 'value'),
        State('unit_abbrev', 'value'),
        State('unit_approvaltype', 'value'),
        State('leave_unit_approvaltype', 'value'),
        State('unit_active', 'value'),
        State('unit_dbmcode', 'value'),
        State('unit_dbmname', 'value'),
        State('unit_dummy', 'value'),

        State("unit_submit", "children"),
        State("unit_chkmarkfordeletion", "value"),
        State("url", "search"),

    ]

)
def process_unit_data(unit_submit, btn_unit_head_close, btn_unit_results_head_return,
                current_user_id,
                unit_name, unit_code, unit_parentunit, unit_academic,
                unit_abbrev, unit_approvaltype, leave_unit_approvaltype, unit_active, unit_dbmcode, unit_dbmname,
                unit_dummy,
                mode, unit_chkmarkfordeletion, url):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,
            False, False,
            # False, False,
            False, False,
            False, False,
            False, False,
            False, False,
            # False, False,
            # False, False,
            # False, False,
        ]

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'unit_submit':
            if unit_name:
                is_valid_unit_name = True
            else:
                is_valid_unit_name = False

            if unit_code:
                is_valid_unit_code= True
            else:
                is_valid_unit_code= True

            if unit_academic:
                is_valid_unit_academic = True
            else:
                is_valid_unit_academic = False

            if unit_abbrev:
                is_valid_unit_abbrev = True
            else:
                is_valid_unit_abbrev = False

            if unit_approvaltype:
                is_valid_unit_approvaltype = True
            else:
                is_valid_unit_approvaltype = False

            if leave_unit_approvaltype:
                is_valid_leave_unit_approvaltype = True
            else:
                is_valid_leave_unit_approvaltype = False

            if unit_dbmcode:
                is_valid_unit_dbmcode = True
            else:
                is_valid_unit_dbmcode = False

            if unit_dbmname:
                is_valid_unit_dbmname = True
            else:
                is_valid_unit_dbmname = False

            validity = [
                is_valid_unit_name, not is_valid_unit_name,
                is_valid_unit_code, not is_valid_unit_code,
                is_valid_unit_academic, not is_valid_unit_academic,
                is_valid_unit_abbrev, not is_valid_unit_abbrev,
                is_valid_unit_approvaltype, not is_valid_unit_approvaltype,
                is_valid_leave_unit_approvaltype, not is_valid_leave_unit_approvaltype,
                # is_valid_unit_dbmcode, not is_valid_unit_dbmcode,
                # is_valid_unit_dbmcode, not is_valid_unit_dbmcode


            ]
            allvalid = [is_valid_unit_name,  is_valid_unit_code, is_valid_unit_academic,
                        is_valid_unit_abbrev, is_valid_unit_approvaltype,
                        is_valid_leave_unit_approvaltype
                        # is_valid_unit_dbmcode, is_valid_unit_dbmcode
                        ]

            if all(allvalid):
                if mode == "Save New unit":

                    sql = """
                        INSERT INTO units (unit_code, unit_name, unit_parent_id,
                        unit_is_academic, unit_abbrev,
                        unit_approval_type_id, unit_is_active, unit_dbm_org_code,
                        unit_inserted_by, unit_inserted_on, unit_delete_ind, unit_dbm_name,
                        unit_leave_approval_type_id,
                        unit_is_dummy)
                        VALUES (%s, %s, %s,
                         %s, %s,
                         %s, %s, %s,
                          %s, %s, %s, %s,
                          %s, %s)
                        RETURNING unit_id
                    """

                    if '1' in unit_active:
                        foractive = True
                    else:
                        foractive = False

                    if '1' in unit_dummy:
                        fordummy = True
                    else:
                        fordummy = False

                    if unit_academic == 1:
                        foracad = True
                    else:
                        foracad = False

                    values = (unit_code, unit_name, unit_parentunit,
                              foracad, unit_abbrev,
                              unit_approvaltype, foractive, unit_dbmcode,
                              current_user_id, datetime.now(), False, unit_dbmname, leave_unit_approvaltype, fordummy)
                    unit_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new unit"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}

                else:
                    unit_id = parse_qs(parsed.query)['unit_id'][0]
                    sql = """
                        UPDATE units SET unit_code = %s, unit_name = %s, unit_parent_id = %s,
                            unit_is_academic = %s, unit_abbrev = %s,
                            unit_approval_type_id= %s, unit_is_active= %s, unit_dbm_org_code= %s,
                            unit_inserted_by = %s, unit_inserted_on = %s, unit_delete_ind = %s, unit_dbm_name = %s,
                            unit_leave_approval_type_id= %s,
                            unit_is_dummy = %s
                            WHERE unit_id = %s
                    """

                    if '1' in unit_active:
                        foractive = True
                    else:
                        foractive = False

                    if unit_academic == 1:
                        foracad = True
                    else:
                        foracad = False

                    if '1' in unit_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False

                    if '1' in unit_dummy:
                        fordummy = True
                    else:
                        fordummy = False

                    values = (
                            unit_code, unit_name, unit_parentunit,
                            foracad, unit_abbrev,
                            unit_approvaltype, foractive, unit_dbmcode,
                            current_user_id, datetime.now(), fordelete, unit_dbmname,
                            leave_unit_approvaltype,fordummy,
                            unit_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False,
                        False, False,
                        # False, False,
                        False, False,
                        False, False,
                        False, False,
                        False, False,
                        # False, False,
                        # False, False,
                        # False, False,
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited unit"
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
        elif eventid == 'btn_unit_head_close':
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

    Output('unit_parentunit', 'options'),

],
    [
    Input('url', 'search'),
],
    [
    ],


)

def fill_in_dropdowns_for_units(url):
    emp_desig = []
    emp_unit = []

    unitoptions = commonmodules.queryfordropdown('''
            SELECT unit_name || ' (' || unit_code || ')' as label,  unit_id as value
              FROM units
            ORDER BY unit_name ASC
           ''', (False, True))

    return [unitoptions]
