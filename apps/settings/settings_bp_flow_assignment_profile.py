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
from apps.commonmodules import checkiflengthzero2, checkstyle2

# bpflowass_emptype_dict = {0:"Any", 1: 'Faculty', 2: 'Administrative Personnel', 3:'Research and Extension Professional Staff (REPS)'}
#
#
# bpflowass_appttype_dict = {0: 'Any', 12:'Original', 13:'Permanency/Tenure', 14:'Promotion', 15: 'Promotion - Automatic', 18:'Promotion - Merit', 19: 'Reappointment - MC 11, Cat II',
#                            20:'Reclassification', 21: 'Reemployement', 22: 'Renewal', 23: 'Renewal with Promotion', 27: 'Transfer - Lateral', 28: 'Transfer - With Promotion'}
#
# bpflowass_numfail_dict = {0:'Any', 1:'0', 2:'At Least 1'}
#
# bpflowass_sg_dict = {0:'Any', 1:'SG 1 to 17', 2:'SG 18 to 33'}
#
# bpflowass_funding_dict = {0:'Any (Yes/No)', 1:'Yes', 2:'No'}
#
# bpflowass_desig_dict = {0:'Any', 1:'Professor Emeritus', 2:'Other (i.e. not Professor Emeritus)'}
#
# bpflowass_srempclass_dict = {0:'Any', 1: 'Faculty', 2: 'Administrative Personnel', 3:'Research and Extension Professional Staff (REPS)'}


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
                html.H4("Add New BP Flow Assignment Criteria", id="bpflowass_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.CardBody([
                dcc.Link('← Back to BP Flow Assignment', href='/settings/settings_bp_flow_assignment'),
                html.Br(),
                html.Br(),
                dbc.Form([
                #     dbc.FormGroup(
                #         [dbc.Label("BP Approval Status Name", width=2, style={"text-align": "left"}),
                #          dbc.Col([
                #              dbc.Input(
                #                  type="text", id="bpflowass_name", placeholder="Enter BP Approval Status"
                #              ),
                #              dbc.FormFeedback("Enter a valid BP approval status", valid=False)
                #          ],
                #             width=8
                #         )],
                #         row=True
                #     ),
                #
                #     dbc.FormGroup(
                #         [dbc.Label("BP Status Description", width=2, style={"text-align": "left"}),
                #          dbc.Col([
                #              dbc.Input(
                #                  type="text", id="bpflowass_description", placeholder="e.g. BP is for VCA Approval"
                #              ),
                #              dbc.FormFeedback("Enter a valid BP approval status description", valid=False)
                #          ],
                #              width=8
                #          )],
                #         row=True
                #     ),
                #
                #     dbc.FormGroup(
                #         [dbc.Label("BP Status Past Name", width=2, style={"text-align": "left"}),
                #          dbc.Col([
                #              dbc.Input(
                #                  type="text", id="bpflowass_pastname", placeholder="e.g. Approved by  VCA"
                #              ),
                #              dbc.FormFeedback("Enter a valid BP approval status description", valid=False)
                #          ],
                #              width=8
                #          )],
                #         row=True
                #     ),

                    dbc.FormGroup(
                        [
                         dbc.Label("BP Employee Type*", width=2, style={"text-align": "left"}, id = 'bpflowass_emptype_label'),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="bpflowass_emptype",
                                 options=[
                                    # {'label': 'Any', 'value': '0'},
                                    # {'label': 'Faculty', 'value': '1'},
                                    # {'label': 'Administrative Personnel', 'value': '2'},
                                    # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                     {'label': 'Any', 'value': 0},
                                     {'label': 'Faculty', 'value': 1},
                                     {'label': 'Administrative Personnel', 'value': 2},
                                     {'label': 'Research and Extension Professional Staff (REPS)', 'value': 3},
                                 ],
                                 value = 0,
                                 searchable=True
                             ),
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("BP Appointment Type*", width=2, style={"text-align": "left"},
                                      id='bpflowass_appttype_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_appttype",
                                    options=[
                                        # {'label': 'Any', 'value': '0'},
                                        # {'label': 'Original', 'value': '12'},
                                        # {'label': 'Permanency/Tenure', 'value': '13'},
                                        # {'label': 'Promotion', 'value': '14'},
                                        # {'label': 'Promotion - Automatic', 'value': '15'},
                                        # {'label': 'Promotion - Merit', 'value': '18'},
                                        # {'label': 'Reappointment - MC 11, Cat II', 'value': '19'},
                                        # {'label': 'Reclassification', 'value': '20'},
                                        # {'label': 'Reemployement', 'value': '21'},
                                        # {'label': 'Renewal', 'value': '22'},
                                        # {'label': 'Renewal with Promotion', 'value': '23'},
                                        # {'label': 'Transfer - Lateral', 'value': '27'},
                                        # {'label': 'Transfer - With Promotion', 'value': '28'},

                                        {'label': 'Any', 'value': 0},
                                        {'label': 'Additional Assignment - Original', 'value': 1},
                                        {'label': 'Additional Assignment - Renewal', 'value': 2},
                                        {'label': 'Additional Assignment - Temporary', 'value': 3},
                                        {'label': 'Original', 'value': 12},
                                        {'label': 'Permanency/Tenure', 'value': 13},
                                        {'label': 'Promotion', 'value': 14},
                                        {'label': 'Promotion - Automatic', 'value': 15},
                                        {'label': 'Promotion - Merit', 'value': 18},
                                        {'label': 'Reappointment - MC 11, Cat II', 'value': 19},
                                        {'label': 'Reclassification', 'value': 20},
                                        {'label': 'Reemployement', 'value': 21},
                                        {'label': 'Renewal', 'value': 22},
                                        {'label': 'Renewal with Promotion', 'value': 23},
                                        {'label': 'Transfer - Lateral', 'value': 27},
                                        {'label': 'Transfer - With Promotion', 'value': 28},

                                    ],
                                    value = 0,
                                    searchable=True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Number of Failing Marks*", width=2, style={"text-align": "left"},
                                      id='bpflowass_numfail_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_numfail",
                                    options=[
                                        # {'label': 'Any', 'value': '0'},
                                        # {'label': '0', 'value': '1'},
                                        # {'label': 'At Least 1', 'value': '2'},

                                        {'label': 'Any', 'value': 0},
                                        {'label': '0', 'value': 1},
                                        {'label': 'At Least 1', 'value': 2},

                                    ],
                                    value=0,
                                    searchable=False
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Salary Grade*", width=2, style={"text-align": "left"},
                                      id='bpflowass_sg_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_sg",
                                    options=[
                                        # {'label': 'Any', 'value': '0'},
                                        # {'label': '0', 'value': '1'},
                                        # {'label': 'At Least 1', 'value': '2'},

                                        {'label': 'Any', 'value': 0},
                                        {'label': 'SG 1 to 17', 'value': 1},
                                        {'label': 'SG 18 to 33', 'value': 2},

                                    ],
                                    value=0,
                                    searchable=False
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Under Trust Account Funding?*", width=2, style={"text-align": "left"},
                                      id='bpflowass_funding_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_funding",
                                    options=[
                                        {'label': 'Any', 'value': 0},
                                        {'label': 'Under Trust Account Funding', 'value': 1},
                                        {'label': 'Not under Trust Account Funding', 'value': 2},

                                    ],

                                    searchable=True
                                ),
                                # dbc.RadioItems(
                                #     id="bpflowass_funding",
                                #     options=[
                                #         # {'label': 'Any', 'value': '0'},
                                #         # {'label': '0', 'value': '1'},
                                #         # {'label': 'At Least 1', 'value': '2'},
                                #
                                #         {'label': 'Yes', 'value': True},
                                #         {'label': 'No', 'value': False},
                                #
                                #     ],
                                #
                                # ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Unit*", width=2, style={"text-align": "left"},
                                      id='bpflowass_unit_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_unit",
                                    options=[


                                    ],

                                    searchable=True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Designation*", width=2, style={"text-align": "left"},
                                      id='bpflowass_desig_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_desig",
                                    options=[
                                        {'label': 'Any', 'value': 0},
                                        {'label': 'Professor Emeritus', 'value': 1},
                                        {'label': 'Instructor/Lecturer', 'value': 3},
                                        {'label': 'Head Librarian', 'value':4},
                                        {'label': 'Other (i.e. not Prof Emeritus/Inst/Lec)', 'value': 2},

                                    ],

                                    searchable=True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("SR Employee Type*", width=2, style={"text-align": "left"},
                                      id='bpflowass_sr_emp_class_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_sr_emp_class",
                                    options=[
                                       # {'label': 'Any', 'value': '0'},
                                       # {'label': 'Faculty', 'value': '1'},
                                       # {'label': 'Administrative Personnel', 'value': '2'},
                                       # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                        {'label': 'Any', 'value': 0},
                                        {'label': 'Faculty', 'value': 1},
                                        {'label': 'Administrative Personnel', 'value': 2},
                                        {'label': 'Research and Extension Professional Staff (REPS)', 'value': 3},
                                    ],

                                    value = 0,
                                    searchable=True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Employee Status*", width=2, style={"text-align": "left"},
                                      id='bpflowass_sr_emp_class_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_emp_status",
                                    options=[

                                    ],

                                    value = 0,
                                    searchable=True,
                                    multi = True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Charge to (Unit):", width=2, style={"text-align": "left"},
                                      id='bpflowass_charge_to_label'),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="bpflowass_charge_to", placeholder="Enter charge to unit (leave blank for any)"
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Number of Days From:*", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options=[

                                            ],  # value=1,
                                            searchable=True, id='bpflowass_numdays_from',
                                        ),

                                    ],
                                        width=4
                                    )
                                ],
                                row=True
                            ),
                        ]),
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("To:*", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options=[

                                            ],
                                            searchable=True, id='bpflowass_numdays_to', multi = False,
                                            disabled = True
                                        ),
                                    ],
                                        width=4
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),

                    # dbc.FormGroup(
                    #     [
                    #         dbc.Label("With replacement designation?", width=2, style={"text-align": "left"},
                    #                   id='bpflowass_replacement_label'),
                    #         dbc.Col([
                    #             dcc.Dropdown(
                    #                 id="bpflowass_replacement",
                    #                 options=[
                    #                     {'label': 'Any', 'value': 0},
                    #                     {'label': 'With replacement designation', 'value': 1},
                    #                     {'label': 'With no replacement designation', 'value': 2},
                    #
                    #                 ],
                    #
                    #                 searchable=True
                    #             ),
                    #             # dbc.RadioItems(  # autofilled, same with previous designation
                    #             #     id='bpflowass_replacement',
                    #             #     options=[
                    #             #         {'label': "Yes", "value": True},
                    #             #         {'label': "No", "value": False},
                    #             #     ]
                    #             # ),
                    #             # dcc.Dropdown(
                    #             #     id="bpflowass_replacement",
                    #             #     options=[
                    #             #         {'label': 'Yes', 'value': 0},
                    #             #         {'label': 'Professor Emeritus', 'value': 1},
                    #             #         {'label': 'Other (i.e. not Professor Emeritus)', 'value': 2},
                    #             #
                    #             #     ],
                    #             #
                    #             #     searchable=True
                    #             # ),
                    #         ],
                    #             width=8
                    #         )],
                    #     row=True
                    # ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Assigned BP Flow 1*", width=2, style={"text-align": "left"},
                                      id='bpflowass_bpflow_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_bpflow",

                                    searchable=True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Assigned BP Flow 2", width=2, style={"text-align": "left"},
                                      id='bpflowass_bpflownew1_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="bpflowass_bpflownew1",

                                    searchable=True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),


                    html.Div([
                        dbc.FormGroup(
                            [
                                dbc.Label("Assigned BP HRDO Flow 3", width=2, style={"text-align": "left"},
                                          id='bpflowass_bpflownew2_label'),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id="bpflowass_bpflownew2",

                                        searchable=True
                                    ),
                                ],
                                    width=8
                                )],
                            row=True
                        ),
                    ], style = {'display':'none'}),



                html.Div([
                    dcc.Checklist(
                        options=[
                            {'label': ' Mark for Deletion?', 'value': '1'},
                        ], id='bpflowass_chkmarkfordeletion', value=[]
                    ),
                ], id='bpflowass_deletediv',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New BP Flow Assignment Criteria", id="bpflowass_submitbtn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="bpflowass_cancel",
                                   href='/settings/settings_bp_flow_assignment', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),


                dbc.Modal(
                    [
                        dbc.ModalHeader("BP Flow Assignment Criteria Entry Confirmation", id='bpflowass_submitmodal1header'),
                        dbc.ModalBody("Confirm BP Flow Assignment Criteria Submission",
                                      id='bpflowass_submitmodal1body'),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id="bpflowass_submitmodal1go", className="mr-1",
                                       color='primary'),
                            dbc.Button("Back", id='bpflowass_submitmodal1back', className="ml-auto")

                            # dbc.Button("Back to Home", id='bpflowass_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="bpflowass_submitmodal1",
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("BP Flow Assignment Criteria Entry", id='bpflowass_submitmodal2_header'),
                        dbc.ModalBody("BP Flow Assignment has been successfully updated.",
                                      id='bpflowass_submitmodal2_body'),
                        dbc.ModalFooter([
                            dbc.Button(
                                "Back to BP Flow Assignment", id='bpflowass_submitmodal2_closebtn', className="ml-auto", color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/settings/settings_bp_flow_assignment',
                            ),
                            dbc.Button(
                                "Close", id='bpflowass_submitmodal2_closebtn', className="ml-auto",color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/home',
                            ),
                            # dbc.Button("Back to Home", id='bpflowass_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="bpflowass_submitmodal2",
                ),


            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('bpflowass_emptype', 'value'),
        Output('bpflowass_appttype', 'value'),
        Output('bpflowass_numfail', 'value'),
        Output('bpflowass_sg', 'value'),
        Output('bpflowass_bpflow', 'value'),
        Output('bpflowass_bpflownew1', 'value'),
        Output('bpflowass_funding', 'value'),
        Output('bpflowass_unit', 'value'),
        Output('bpflowass_desig', 'value'),
        Output('bpflowass_sr_emp_class', 'value'),
        Output('bpflowass_emp_status', 'value'),
        Output('bpflowass_numdays_from', 'value'),
        Output('bpflowass_numdays_to', 'value'),
        Output('bpflowass_charge_to', 'value'),

        # Output('bpflowass_replacement', 'value'),

        Output("bpflowass_editmodalhead", "children"),
        Output("bpflowass_submitbtn", "children"),
        Output("bpflowass_chkmarkfordeletion", "style"),

        Output('bpflowass_bpflow', 'options'),
        Output('bpflowass_bpflownew1', 'options'),
        Output('bpflowass_bpflownew2', 'options'),
        Output('bpflowass_unit', 'options'),
        Output('bpflowass_appttype', 'options'),
        Output('bpflowass_emp_status', 'options'),
        Output('bpflowass_numdays_from', 'options')

    ],
    [
        Input("url", "search"),
    ],
    [

    ]

)
def cleardata(url,

              ):

    flowoptions = commonmodules.queryfordropdown('''
        SELECT approval_flow_name as label, approval_flow_id as value
       FROM bp_approval_flows
       WHERE approval_flow_delete_ind = %s
       ORDER BY approval_flow_name
    ''', (False, ))

    unitoptions = commonmodules.queryfordropdown('''
        SELECT unit_name || ' (' || unit_code || ')' as label,  unit_id as value
       FROM units
       WHERE unit_is_active = %s
       AND unit_delete_ind = %s
       ORDER BY unit_name
    ''', (True, False))

    unitoptions.insert(0, {'label': 'Any', 'value': 0})

    appttypeoptions = commonmodules.queryfordropdown('''
       SELECT appt_type_name as label, appt_type_id as value
       FROM appointment_types
       WHERE appt_type_is_active = %s
       AND appt_type_delete_ind = %s
       ORDER BY appt_type_name
    ''', (True, False))

    appttypeoptions.insert(0, {'label': 'Any', 'value': 0})

    emp_statuses = commonmodules.queryfordropdown('''
        SELECT emp_status_name as label, emp_status_id as value
       FROM emp_statuses
       WHERE emp_status_delete_ind = %s
       ORDER BY emp_status_name
    ''', (False,))

    bpflowass_numdays_from = []

    for i in range(0,51):
        dict_proxy = {}
        dict_proxy['label'] = i
        dict_proxy['value'] = i
        bpflowass_numdays_from.append(dict_proxy)


    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            bpflowass_editmodalhead = "Edit Existing BP Flow Assignment Criteria:"
            bpflowass_submit = "Save Changes"
            bpflowass_chkmarkfordeletion_style = {"display": "inline"}
            bp_flow_assignment_id = parse_qs(parsed.query)['bp_flow_assignment_id'][0]

            sql = '''

            SELECT bp_flow_assignment_emp_class_id, bp_flow_assignment_appt_type_id, bp_flow_assignment_numfail_id,
            bp_flow_assignment_sg_type_id, bp_flow_assignment_flow_id, bp_flow_assignment_unit_id, bp_flow_assignment_is_ta_funding,
            bp_flow_assignment_desig_id, bp_flow_assignment_sr_emp_class_id, bp_flow_assignment_empstatus_id, bp_flow_assignment_numdays_from, bp_flow_assignment_numdays_to, bp_flow_assignment_flow_new1_id,
            bp_flow_assignment_psi_type_extension
            FROM bp_flow_assignment bfa
            WHERE bp_flow_assignment_delete_ind = %s
            AND bp_flow_assignment_id = %s

            '''
            values = (False, bp_flow_assignment_id,)
            columns = ['bp_flow_assignment_emp_class_id', 'bp_flow_assignment_appt_type_id', 'bp_flow_assignment_numfail_id',
                       'bp_flow_assignment_sg_type_id', 'bp_flow_assignment_flow_id', 'bp_flow_assignment_unit_id', 'bp_flow_assignment_is_ta_funding',
                       'bp_flow_assignment_desig_id', 'bp_flow_assignment_sr_emp_class_id',
                       'bp_flow_assignment_empstatus_id', 'bp_flow_assignment_numdays_from', 'bp_flow_assignment_numdays_to', 'bp_flow_assignment_flow_new1_id',
                       'bp_flow_assignment_psi_type_extension']
            df = securequerydatafromdatabase(sql, values, columns)

            bp_flow_assignment_emp_class_id = df["bp_flow_assignment_emp_class_id"][0]
            bp_flow_assignment_appt_type_id = df["bp_flow_assignment_appt_type_id"][0]
            bp_flow_assignment_numfail_id = df["bp_flow_assignment_numfail_id"][0]
            bp_flow_assignment_sg_type_id = df["bp_flow_assignment_sg_type_id"][0]
            bp_flow_assignment_flow_id = df['bp_flow_assignment_flow_id'][0]
            bp_flow_assignment_flow_new1_id = df['bp_flow_assignment_flow_new1_id'][0]
            bp_flow_assignment_unit_id = df['bp_flow_assignment_unit_id'][0]
            bp_flow_assignment_is_ta_funding = df['bp_flow_assignment_is_ta_funding'][0]
            bp_flow_assignment_desig_id = df['bp_flow_assignment_desig_id'][0]
            bp_flow_assignment_sr_emp_class_id = df['bp_flow_assignment_sr_emp_class_id'][0]
            bp_flow_assignment_empstatus_id = df['bp_flow_assignment_empstatus_id'][0]
            bp_flow_assignment_numdays_from = df['bp_flow_assignment_numdays_from'][0]
            bp_flow_assignment_numdays_to = df['bp_flow_assignment_numdays_to'][0]
            bpflowass_charge_to = df['bp_flow_assignment_psi_type_extension'][0]


        elif parse_qs(parsed.query)['mode'][0] == "add":
            bpflowass_editmodalhead = "Add New BP Flow Assignment Criteria"
            bpflowass_submit = "Save New BP Approval Status"
            bpflowass_chkmarkfordeletion_style = {"display": "none"}

            bp_flow_assignment_emp_class_id = ""
            bp_flow_assignment_appt_type_id= ""
            bp_flow_assignment_numfail_id= ""
            bp_flow_assignment_sg_type_id= ""
            bp_flow_assignment_flow_id = ""
            bp_flow_assignment_flow_new1_id = ""
            bp_flow_assignment_unit_id = ""
            bp_flow_assignment_is_ta_funding = ""
            bp_flow_assignment_desig_id = ""
            bp_flow_assignment_sr_emp_class_id = ""
            bp_flow_assignment_empstatus_id = ""
            bp_flow_assignment_numdays_from = ""
            bp_flow_assignment_numdays_to = ""
            bpflowass_charge_to = ""




        return [bp_flow_assignment_emp_class_id, bp_flow_assignment_appt_type_id, bp_flow_assignment_numfail_id,bp_flow_assignment_sg_type_id, bp_flow_assignment_flow_id,
                bp_flow_assignment_flow_new1_id,
                bp_flow_assignment_is_ta_funding, bp_flow_assignment_unit_id, bp_flow_assignment_desig_id, bp_flow_assignment_sr_emp_class_id,
                bp_flow_assignment_empstatus_id,
                bp_flow_assignment_numdays_from,
                bp_flow_assignment_numdays_to,
                bpflowass_charge_to,
                bpflowass_editmodalhead, bpflowass_submit, bpflowass_chkmarkfordeletion_style,
                flowoptions,
                flowoptions,
                flowoptions,
                unitoptions,
                appttypeoptions,
                emp_statuses,
                bpflowass_numdays_from
                ]

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('bpflowass_emptype_label', 'style'),
        Output('bpflowass_appttype_label', 'style'),
        Output('bpflowass_numfail_label', 'style'),
        Output('bpflowass_sg_label', 'style'),
        Output('bpflowass_bpflow_label', 'style'),
        Output('bpflowass_bpflownew1_label', 'style'),
        Output('bpflowass_bpflownew2_label', 'style'),
        Output('bpflowass_funding_label', 'style'),
        # Output('bpflowass_replacement_label', 'style'),
        Output('bpflowass_sr_emp_class_label', 'style'),


        Output('bpflowass_submitmodal1', 'is_open')

    ],

    [
        Input('bpflowass_submitbtn', 'n_clicks'),
        Input('bpflowass_submitmodal1go', 'n_clicks'),
        Input('bpflowass_submitmodal1back', 'n_clicks')

    ],
    [
        State('bpflowass_emptype', 'value'),
        State('bpflowass_appttype', 'value'),
        State('bpflowass_numfail', 'value'),
        State('bpflowass_sg', 'value'),
        State('bpflowass_bpflow', 'value'),
        State('bpflowass_bpflownew1', 'value'),
        State('bpflowass_bpflownew2', 'value'),
        State('bpflowass_funding', 'value'),
        # State('bpflowass_replacement', 'value'),
        State('bpflowass_sr_emp_class', 'value'),

    ]

)

def bpflowass_modal1open(bpflowass_submitbtn, bpflowass_submitmodal1go, bpflowass_submitmodal1back,
                          bpflowass_emptype, bpflowass_appttype, bpflowass_numfail, bpflowass_sg, bpflowass_bpflow,
                         bpflowass_bpflownew1, bpflowass_bpflownew2,
                         bpflowass_funding, bpflowass_sr_emp_class):

    bpflowass_submitmodal1 = False
    ctx = dash.callback_context
    if ctx.triggered:

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        bpflowass_emptypevalid = checkiflengthzero2(str(bpflowass_emptype))
        bpflowass_appttypevalid = checkiflengthzero2(str(bpflowass_appttype))
        bpflowass_numfailvalid = checkiflengthzero2(str(bpflowass_numfail))
        bpflowass_sgvalid = checkiflengthzero2(str(bpflowass_sg))
        bpflowass_bpflowvalid = checkiflengthzero2(bpflowass_bpflow)
        bpflowass_bpflownew1valid = checkiflengthzero2(bpflowass_bpflownew1)
        bpflowass_bpflownew2valid = checkiflengthzero2(bpflowass_bpflownew2)
        bpflowass_fundingvalid = checkiflengthzero2(str(bpflowass_funding))
        bpflowass_sr_emp_classvalid = checkiflengthzero2(str(bpflowass_sr_emp_class))
        # bpflowass_replacement = checkiflengthzero2(str(bpflowass_replacement))

        bpflowass_emptype_label = checkstyle2(bpflowass_emptypevalid)
        bpflowass_appttype_label = checkstyle2(bpflowass_appttypevalid)
        bpflowass_numfail_label = checkstyle2(bpflowass_numfailvalid)
        bpflowass_sg_label = checkstyle2(bpflowass_sgvalid)
        bpflowass_bpflow_label = checkstyle2(bpflowass_bpflowvalid)
        bpflowass_bpflownew1_label = checkstyle2(bpflowass_bpflownew1valid)
        bpflowass_bpflownew2_label = checkstyle2(bpflowass_bpflownew2valid)
        bpflowass_funding_label = checkstyle2(bpflowass_fundingvalid)
        # bpflowass_replacement_label = checkstyle2(bpflowass_replacementvalid)
        bpflowass_sr_emp_class_label = checkstyle2(bpflowass_sr_emp_classvalid)

        allvalid = [bpflowass_emptypevalid, bpflowass_appttypevalid, bpflowass_numfailvalid, bpflowass_sgvalid,
                    # bpflowass_bpflowvalid,
                    # bpflowass_bpflownew1valid, bpflowass_bpflownew2valid,
                    bpflowass_fundingvalid, bpflowass_sr_emp_classvalid]

        if all(allvalid):

            bpflowass_submitmodal1 = True

        if eventid in ['bpflowass_submitbtn','bpflowass_submitmodal1go', 'bpflowass_submitmodal1back']:
            if eventid in ['bpflowass_submitmodal1go', 'bpflowass_submitmodal1back']:

                bpflowass_submitmodal1 = False


            return [bpflowass_emptype_label,
                    bpflowass_appttype_label,
                    bpflowass_numfail_label,
                    bpflowass_sg_label,
                    bpflowass_bpflow_label,
                    bpflowass_bpflownew1_label,
                    bpflowass_bpflownew2_label,
                    bpflowass_funding_label,
                    bpflowass_sr_emp_class_label,
                    # bpflowass_replacement_label,
                    bpflowass_submitmodal1]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('bpflowass_submitmodal2', 'is_open')

    ],
    [
        Input('bpflowass_submitmodal1go', 'n_clicks'),
        Input('bpflowass_submitmodal2_closebtn', 'n_clicks')

    ],
    [
        State('bpflowass_emptype', 'value'),
        State('bpflowass_appttype', 'value'),
        State('bpflowass_numfail', 'value'),
        State('bpflowass_sg', 'value'),
        State('bpflowass_bpflow', 'value'),
        State('bpflowass_bpflownew1', 'value'),
        State('bpflowass_bpflownew2', 'value'),
        State('bpflowass_funding', 'value'),
        State('bpflowass_unit', 'value'),
        State('bpflowass_desig', 'value'),
        State('bpflowass_sr_emp_class', 'value'),
        State('bpflowass_emp_status', 'value'),
        State('bpflowass_numdays_from', 'value'),
        State('bpflowass_numdays_to', 'value'),
        State('bpflowass_charge_to', 'value'),
        # State('bpflowass_replacement', 'value'),
        State('bpflowass_chkmarkfordeletion', 'value'),
        State('url', 'search'),
        State('current_user_id', 'data'),


    ]
)

def bpflowass_submitmodal2(bpflowass_submitmodal1go, bpflowass_submitmodal2_closebtn,
                            bpflowass_emptype, bpflowass_appttype, bpflowass_numfail, bpflowass_sg, bpflowass_bpflow,
                            bpflowass_bpflownew1, bpflowass_bpflownew2,
                            bpflowass_funding, bpflowass_unit, bpflowass_desig,
                            bpflowass_sr_emp_class,
                            bpflowass_emp_status,
                            bpflowass_numdays_from,
                            bpflowass_numdays_to,
                            bpflowass_charge_to,
                            bpflowass_chkmarkfordeletion,
                            url,
                            current_user_id):
    # print('HERE435747', bpflowass_bpflownew1)
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        if ctx.triggered:
            mode = str(parse_qs(parsed.query)['mode'][0])
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'bpflowass_submitmodal1go':

                if mode == "add":

                    sql6 = '''
                        SELECT MAX(bp_flow_assignment_priority_id) as flow_max_priority
                        FROM bp_flow_assignment
                        WHERE bp_flow_assignment_delete_ind = False

                    '''

                    values6 = (False,)
                    columns6 = ['flow_max_priority']
                    df6 = securequerydatafromdatabase(sql6, values6, columns6)
                    flow_max_priority = int(df6["flow_max_priority"][0])


                    sql1 = """
                        INSERT INTO bp_flow_assignment(bp_flow_assignment_emp_class_id, bp_flow_assignment_appt_type_id, bp_flow_assignment_numfail_id,
                                                bp_flow_assignment_sg_type_id,
                                                bp_flow_assignment_flow_id, bp_flow_assignment_flow_new1_id, bp_flow_assignment_flow_new2_id,
                                                bp_flow_assignment_inserted_by, bp_flow_assignment_inserted_on, bp_flow_assignment_delete_ind,
                                                bp_flow_assignment_priority_id, bp_flow_assignment_unit_id, bp_flow_assignment_is_ta_funding, bp_flow_assignment_desig_id, bp_flow_assignment_sr_emp_class_id,
                                                bp_flow_assignment_empstatus_id,
                                                bp_flow_assignment_numdays_from,
                                                bp_flow_assignment_numdays_to,
                                                bp_flow_assignment_psi_type_extension
                                                )
                        VALUES (%s, %s, %s,
                                %s,
                                %s, %s, %s,
                                %s, %s, %s,
                                %s, %s, %s, %s, %s,
                                %s, %s, %s,
                                %s)
                    """

                    if len(str(bpflowass_bpflow)) == 0:
                        bpflowass_bpflow = None

                    if len(str(bpflowass_bpflownew1)) == 0:
                        bpflowass_bpflownew1 = None

                    values1 = [bpflowass_emptype, bpflowass_appttype, bpflowass_numfail,
                               bpflowass_sg,
                               bpflowass_bpflow, bpflowass_bpflownew1, bpflowass_bpflownew2,
                               current_user_id, datetime.now(), False, flow_max_priority+1, bpflowass_unit, bpflowass_funding, bpflowass_desig, bpflowass_sr_emp_class,
                               bpflowass_emp_status,
                               bpflowass_numdays_from,
                               bpflowass_numdays_to,
                               bpflowass_charge_to
                               ]


                    modifydatabase(sql1, values1)


                elif mode == "edit":
                    # print('bpflowass_chkmarkfordeletion', bpflowass_chkmarkfordeletion)
                    bp_flow_assignment_id = str(parse_qs(parsed.query)['bp_flow_assignment_id'][0])

                    bpflowass_deletevalue = False
                    if 1 in bpflowass_chkmarkfordeletion or '1' in bpflowass_chkmarkfordeletion:
                        bpflowass_deletevalue = True


                    sql1 = """
                        UPDATE bp_flow_assignment SET bp_flow_assignment_emp_class_id=%s, bp_flow_assignment_appt_type_id=%s, bp_flow_assignment_numfail_id=%s,
                            bp_flow_assignment_sg_type_id = %s, bp_flow_assignment_flow_id = %s, bp_flow_assignment_inserted_by = %s, bp_flow_assignment_inserted_on = %s, bp_flow_assignment_delete_ind = %s,
                            bp_flow_assignment_unit_id = %s, bp_flow_assignment_is_ta_funding = %s, bp_flow_assignment_desig_id = %s, bp_flow_assignment_sr_emp_class_id = %s,
                            bp_flow_assignment_empstatus_id = %s, bp_flow_assignment_numdays_from = %s, bp_flow_assignment_numdays_to = %s, bp_flow_assignment_flow_new1_id = %s,
                            bp_flow_assignment_psi_type_extension = %s
                        WHERE bp_flow_assignment_id=%s
                    """

                    values1 = [bpflowass_emptype, bpflowass_appttype, bpflowass_numfail,
                               bpflowass_sg, bpflowass_bpflow, current_user_id, datetime.now(), bpflowass_deletevalue,
                               bpflowass_unit, bpflowass_funding, bpflowass_desig, bpflowass_sr_emp_class,
                               bpflowass_emp_status, bpflowass_numdays_from, bpflowass_numdays_to, bpflowass_charge_to, bpflowass_bpflownew1,
                               bp_flow_assignment_id]

                    modifydatabase(sql1, values1)

                return [True]

            elif eventid == "bpflowass_submitmodal2_closebtn":

                return [False]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('bpflowass_numdays_to', 'disabled'),
        Output('bpflowass_numdays_to', 'options'),
    ],
    [
        Input('bpflowass_numdays_from', 'value')
    ],
    [
        State('url', 'search'),

    ]

)

def populatetodays(bpflowass_numdays_from, url):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        if ctx.triggered:
            mode = str(parse_qs(parsed.query)['mode'][0])
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'bpflowass_numdays_from':
                # print('HERE2346', bpflowass_numdays_from)
                if str(bpflowass_numdays_from) in ['None', 'NONE', 'none', ""]:
                    to_dropdown_disabled = True
                    bpflowass_numdays_to = []

                else:
                    bpflowass_numdays_to = []
                    for i in range(bpflowass_numdays_from, 101):
                        dict_proxy = {}
                        dict_proxy['label'] = i
                        dict_proxy['value'] = i
                        bpflowass_numdays_to.append(dict_proxy)
                        to_dropdown_disabled = False
                    bpflowass_numdays_to.insert(0, {'label': 'No Limit', 'value': 0})
                return [to_dropdown_disabled, bpflowass_numdays_to]

            else:
                raise PreventUpdate

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
