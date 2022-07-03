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

leaveflowass_emptype_dict = {0:"Any", 1: 'Faculty (Full-time)', 2: 'Administrative Personnel', 3:'Research and Extension Professional Staff (REPS)', 4:'Faculty (Administrator)'}


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

leaveflowass_days_dict = {0:'Any', 1: '1 to less than 4 days', 2: '4 to less than 30 days', 3:'30 to less than 365 days', 4:'365 days and above'}
leaveflowass_ishead_dict = {0:'Any', 1:'Yes', 2:'No'}

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
    html.H1("Leave Approval Flow Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Leave Flow Assignment Criteria", id="leave_flowass_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.CardBody([
                dcc.Link('← Back to Leave Flow Assignment', href='/settings/settings_leave_flow_assignment'),
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
                         dbc.Label("Leave Type", width=2, style={"text-align": "left"}, id = 'leave_flowass_leavetype_label'),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leave_flowass_leavetype",
                                 options=[
                                    # # {'label': 'Any', 'value': '0'},
                                    # # {'label': 'Faculty', 'value': '1'},
                                    # # {'label': 'Administrative Personnel', 'value': '2'},
                                    # # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                    #  {'label': 'Any', 'value': 0},
                                    #  {'label': 'Faculty', 'value': 1},
                                    #  {'label': 'Administrative Personnel', 'value': 2},
                                    #  {'label': 'Research and Extension Professional Staff (REPS)', 'value': 3},
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
                            dbc.Label("Designation", width=2, style={"text-align": "left"},
                                      id='leave_flowass_desig_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="leave_flowass_desig",
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
                         dbc.Label("Employee Class", width=2, style={"text-align": "left"}, id = 'leave_flowass_emptype_label'),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leave_flowass_emptype",
                                 options=[
                                    # {'label': 'Any', 'value': '0'},
                                    # {'label': 'Faculty', 'value': '1'},
                                    # {'label': 'Administrative Personnel', 'value': '2'},
                                    # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                     {'label': 'Any', 'value': 0},
                                     {'label': 'Faculty (Full-time)', 'value': 1},
                                     {'label': 'Administrative Personnel', 'value': 2},
                                     {'label': 'Research and Extension Professional Staff (REPS)', 'value': 3},
                                     {'label': 'Faculty (Administrator)', 'value': 4},
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
                         dbc.Label("Head of Unit/Sub-unit?", width=2, style={"text-align": "left"}, id = 'leave_flowass_ishead_label'),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leave_flowass_ishead",
                                 options=[
                                    # {'label': 'Any', 'value': '0'},
                                    # {'label': 'Faculty', 'value': '1'},
                                    # {'label': 'Administrative Personnel', 'value': '2'},
                                    # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                     {'label': 'Any', 'value': 0},
                                     {'label': 'Yes', 'value': 1},
                                     {'label': 'No', 'value': 2},
                                     # {'label': 'Research and Extension Professional Staff (REPS)', 'value': 3},
                                     # {'label': 'Faculty (Administrator)', 'value': 4},
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
                            dbc.Label("# of Days of Leave", width=2, style={"text-align": "left"},
                                      id='leave_flowass_numdays_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="leave_flowass_numdays",
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
                                        {'label': '1 to less than 4 days', 'value': 1},
                                        {'label': '4 to 29 days', 'value': 2},
                                        {'label': '30 to less than 365 days', 'value': 3},
                                        {'label': '365 days and above', 'value': 4},


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
                            dbc.Label("Unit", width=2, style={"text-align": "left"},
                                      id='leave_flowass_unit_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="leave_flowass_unit",
                                    options=[


                                    ],

                                    searchable=True,
                                    multi=True

                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),


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
                            dbc.Label("Assigned Leave Flow", width=2, style={"text-align": "left"},
                                      id='leave_flowass_leaveflow_label'),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="leave_flowass_leaveflow",

                                    searchable=True
                                ),
                            ],
                                width=8
                            )],
                        row=True
                    ),



                html.Div([
                    dcc.Checklist(
                        options=[
                            {'label': ' Mark for Deletion?', 'value': '1'},
                        ], id='leave_flowass_chkmarkfordeletion', value=[]
                    ),
                ], id='leave_flowass_deletediv',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Leave Flow Assignment Criteria", id="leave_flowass_submitbtn",
                                   color="info", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="leave_flowass_cancel",
                                   href='/settings/settings_leave_flow_assignment', color="warning", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),


                dbc.Modal(
                    [
                        dbc.ModalHeader("Leave Flow Assignment Criteria Entry Confirmation", id='leave_flowass_submitmodal1header'),
                        dbc.ModalBody("Confirm Leave Flow Assignment Criteria Submission",
                                      id='leave_flowass_submitmodal1body'),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id="leave_flowass_submitmodal1go", className="mr-1",
                                       color='primary'),
                            dbc.Button("Back", id='leave_flowass_submitmodal1back', className="ml-auto")

                            # dbc.Button("Back to Home", id='bpflowass_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="leave_flowass_submitmodal1",
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("Leave Flow Assignment Criteria Entry", id='leave_flowass_submitmodal2_header'),
                        dbc.ModalBody("Leave Flow Assignment has been successfully updated.",
                                      id='leave_flowass_submitmodal2_body'),
                        dbc.ModalFooter([
                            dbc.Button(
                                "Back to Leave Flow Assignment", id='leave_flowass_submitmodal2_closebtn', className="ml-auto", color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/settings/settings_leave_flow_assignment',
                            ),
                            dbc.Button(
                                "Close", id='leave_flowass_submitmodal2_closebtn', className="ml-auto",color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/home',
                            ),
                            # dbc.Button("Back to Home", id='bpflowass_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="leave_flowass_submitmodal2",
                ),


            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('leave_flowass_leavetype', 'value'),
        Output('leave_flowass_desig', 'value'),
        Output('leave_flowass_emptype', 'value'),
        Output('leave_flowass_ishead', 'value'),
        Output('leave_flowass_numdays', 'value'),
        Output('leave_flowass_unit', 'value'),
        Output('leave_flowass_leaveflow', 'value'),
        # Output('bpflowass_unit', 'value'),
        # Output('bpflowass_desig', 'value'),
        # Output('bpflowass_sr_emp_class', 'value'),
        # Output('bpflowass_replacement', 'value'),

        Output("leave_flowass_editmodalhead", "children"),
        Output("leave_flowass_submitbtn", "children"),
        Output("leave_flowass_chkmarkfordeletion", "style"),

        Output('leave_flowass_leaveflow', 'options'),
        Output('leave_flowass_unit', 'options'),
        Output('leave_flowass_leavetype', 'options'),
        Output('leave_flowass_desig', 'options')

    ],
    [
        Input("url", "search"),
    ],
    [

    ]

)
def leavefa_cleardata(url,

              ):

    flowoptions = commonmodules.queryfordropdown('''
        SELECT leave_approval_flow_name as label, leave_approval_flow_id as value
       FROM leave_approval_flows
       WHERE leave_approval_flow_delete_ind = %s
       ORDER BY leave_approval_flow_name
    ''', (False, ))

    unitoptions = commonmodules.queryfordropdown('''
        SELECT CONCAT(unit_name,' (',unit_code,') ')  as label, unit_id as value
       FROM units
       WHERE unit_is_active = %s
       AND unit_delete_ind = %s
       ORDER BY unit_name
    ''', (True, False))

    unitoptions.insert(0, {'label': 'Any', 'value': 0})

    leavetypeoptions = commonmodules.queryfordropdown('''
        SELECT leave_type_name || ' (' || leave_type_code || ')' as label, leave_type_id as value
       FROM leave_types
       WHERE leave_type_delete_ind = %s
       ORDER BY leave_type_name
    ''', (False, ))

    leavetypeoptions.insert(0, {'label': 'Any', 'value': 0})

    # roleoptions = commonmodules.queryfordropdown('''
    #     SELECT role_name as label, role_id as value
    #    FROM roles
    #    WHERE role_delete_ind = %s
    #    ORDER BY role_name
    # ''', (False, ))

    desigoptions = commonmodules.queryfordropdown('''
        SELECT designation_name as label, designation_id as value
       FROM designations
       WHERE designation_delete_ind = %s
       ORDER BY designation_name
    ''', (False, ))

    desigoptions.insert(0, {'label': 'Any', 'value': 0})

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            leave_flowass_editmodalhead = "Edit Existing Leave Flow Assignment Criteria"
            leave_flowass_submit = "Save Changes"
            leave_flowass_chkmarkfordeletion_style = {"display": "inline"}
            leave_flow_assignment_id = parse_qs(parsed.query)['leave_flow_assignment_id'][0]

            sql = '''

            SELECT leave_flow_assignment_designation_id, leave_flow_assignment_numdays, leave_flow_assignment_emp_class_id, leave_flow_assignment_flow_id,
            leave_flow_assignment_unit_id, leave_flow_assignment_leavetype_id, leave_flow_assignment_ishead_id
            FROM leave_flow_assignment bs
            WHERE leave_flow_assignment_delete_ind = %s
            AND leave_flow_assignment_id = %s

            '''
            values = (False, leave_flow_assignment_id,)
            columns = ['leave_flow_assignment_designation_id', 'leave_flow_assignment_numdays', 'leave_flow_assignment_emp_class_id', 'leave_flow_assignment_flow_id',
                'leave_flow_assignment_unit_id', 'leave_flow_assignment_leavetype_id', 'leave_flow_assignment_ishead_id']
            df = securequerydatafromdatabase(sql, values, columns)

            leave_flow_assignment_desig_id = df["leave_flow_assignment_designation_id"][0]
            leave_flow_assignment_numdays = df["leave_flow_assignment_numdays"][0]
            leave_flow_assignment_emp_class_id = df["leave_flow_assignment_emp_class_id"][0]
            leave_flow_assignment_ishead_id = df["leave_flow_assignment_ishead_id"][0]
            leave_flow_assignment_leaveflow_id = df["leave_flow_assignment_flow_id"][0]
            leave_flow_assignment_unit_id = df["leave_flow_assignment_unit_id"][0]
            leave_flow_assignment_leavetype_id = df["leave_flow_assignment_leavetype_id"][0]
            # leave_flow_assignment_unit_id_new = df["leave_flow_assignment_unit_id_new"][0]
            # if leave_flow_assignment_unit_id_new == None:
            #     leave_flow_assignment_unit_id_new = None
            # else:
            #
            #     leave_flow_assignment_unit_id_new = re.split("[{|}|;|,]", leave_flow_assignment_unit_id_new)
            #     leave_flow_assignment_unit_id_new = list(filter(None, leave_flow_assignment_unit_id_new))

            # bp_flow_assignment_emp_class_id = df["bp_flow_assignment_emp_class_id"][0]
            # bp_flow_assignment_appt_type_id = df["bp_flow_assignment_appt_type_id"][0]
            # bp_flow_assignment_numfail_id = df["bp_flow_assignment_numfail_id"][0]
            # bp_flow_assignment_sg_type_id = df["bp_flow_assignment_sg_type_id"][0]
            # bp_flow_assignment_flow_id = df['bp_flow_assignment_flow_id'][0]
            # bp_flow_assignment_unit_id = df['bp_flow_assignment_unit_id'][0]
            # bp_flow_assignment_is_ta_funding = df['bp_flow_assignment_is_ta_funding'][0]
            # bp_flow_assignment_desig_id = df['bp_flow_assignment_desig_id'][0]
            # bp_flow_assignment_sr_emp_class_id = df['bp_flow_assignment_sr_emp_class_id'][0]


        elif parse_qs(parsed.query)['mode'][0] == "add":
            leave_flowass_editmodalhead = "Add New Leave Flow Assignment Criteria"
            leave_flowass_submit = "Save New Leave Flow Assignment Criteria"
            leave_flowass_chkmarkfordeletion_style = {"display": "none"}

            leave_flow_assignment_desig_id = ""
            leave_flow_assignment_numdays = ""
            leave_flow_assignment_emp_class_id = ""
            leave_flow_assignment_ishead_id = ""
            leave_flow_assignment_leaveflow_id = ""
            leave_flow_assignment_unit_id = ""
            leave_flow_assignment_leavetype_id = ""
            # leave_flow_assignment_unit_id_new = ""






        return [leave_flow_assignment_leavetype_id, leave_flow_assignment_desig_id, leave_flow_assignment_emp_class_id, leave_flow_assignment_ishead_id, leave_flow_assignment_numdays,
            leave_flow_assignment_unit_id, leave_flow_assignment_leaveflow_id,
            leave_flowass_editmodalhead, leave_flowass_submit, leave_flowass_chkmarkfordeletion_style,
            flowoptions, unitoptions, leavetypeoptions, desigoptions]



        # bp_flow_assignment_emp_class_id, bp_flow_assignment_appt_type_id, bp_flow_assignment_numfail_id,bp_flow_assignment_sg_type_id, bp_flow_assignment_flow_id,
        #         bp_flow_assignment_is_ta_funding, bp_flow_assignment_unit_id, bp_flow_assignment_desig_id, bp_flow_assignment_sr_emp_class_id,
        #         bpflowass_editmodalhead, bpflowass_submit, bpflowass_chkmarkfordeletion_style,
        #         flowoptions,
        #         unitoptions
        #         ]

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('leave_flowass_leavetype_label', 'style'),
        Output('leave_flowass_desig_label', 'style'),
        Output('leave_flowass_emptype_label', 'style'),
        Output('leave_flowass_ishead_label', 'style'),
        Output('leave_flowass_numdays_label', 'style'),
        Output('leave_flowass_unit_label', 'style'),
        Output('leave_flowass_leaveflow_label', 'style'),
        # Output('bpflowass_replacement_label', 'style'),
        # Output('bpflowass_sr_emp_class_label', 'style'),


        Output('leave_flowass_submitmodal1', 'is_open')

    ],

    [
        Input('leave_flowass_submitbtn', 'n_clicks'),
        Input('leave_flowass_submitmodal1go', 'n_clicks'),
        Input('leave_flowass_submitmodal1back', 'n_clicks')

    ],
    [
        State('leave_flowass_leavetype', 'value'),
        State('leave_flowass_desig', 'value'),
        State('leave_flowass_emptype', 'value'),
        State('leave_flowass_ishead', 'value'),
        State('leave_flowass_numdays', 'value'),
        State('leave_flowass_unit', 'value'),
        State('leave_flowass_leaveflow', 'value'),

        # State('bpflowass_emptype', 'value'),
        # State('bpflowass_appttype', 'value'),
        # State('bpflowass_numfail', 'value'),
        # State('bpflowass_sg', 'value'),
        # State('bpflowass_bpflow', 'value'),
        # State('bpflowass_funding', 'value'),
        # # State('bpflowass_replacement', 'value'),
        # State('bpflowass_sr_emp_class', 'value'),

    ]

)

def leavefa_modalopen(leave_flowass_submitbtn, leave_flowass_submitmodal1go, leave_flowass_submitmodal1back,
                        leave_flowass_leavetype, leave_flowass_desig, leave_flowass_emptype, leave_flowass_ishead, leave_flowass_numdays, leave_flowass_unit,
                        leave_flowass_leaveflow):
                          # bpflowass_emptype, bpflowass_appttype, bpflowass_numfail, bpflowass_sg, bpflowass_bpflow, bpflowass_funding, bpflowass_sr_emp_class):

    leave_flowass_submitmodal1 = False
    ctx = dash.callback_context
    if ctx.triggered:

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        leave_flowass_leavetypevalid = checkiflengthzero2(str(leave_flowass_leavetype))
        leave_flowass_desigvalid = checkiflengthzero2(str(leave_flowass_desig))
        leave_flowass_emptypevalid = checkiflengthzero2(str(leave_flowass_emptype))
        leave_flowass_isheadvalid = checkiflengthzero2(str(leave_flowass_ishead))
        leave_flowass_numdaysvalid = checkiflengthzero2(str(leave_flowass_numdays))
        leave_flowass_unitvalid = checkiflengthzero2(str(leave_flowass_unit))
        leave_flowass_leaveflowvalid = checkiflengthzero2(str(leave_flowass_leaveflow))

        # bpflowass_emptypevalid = checkiflengthzero2(str(bpflowass_emptype))
        # bpflowass_appttypevalid = checkiflengthzero2(str(bpflowass_appttype))
        # bpflowass_numfailvalid = checkiflengthzero2(str(bpflowass_numfail))
        # bpflowass_sgvalid = checkiflengthzero2(str(bpflowass_sg))
        # bpflowass_bpflowvalid = checkiflengthzero2(bpflowass_bpflow)
        # bpflowass_fundingvalid = checkiflengthzero2(str(bpflowass_funding))
        # bpflowass_sr_emp_classvalid = checkiflengthzero2(str(bpflowass_sr_emp_class))
        # bpflowass_replacement = checkiflengthzero2(str(bpflowass_replacement))

        leave_flowass_leavetype_label = checkstyle2(leave_flowass_leavetypevalid)
        leave_flowass_desig_label = checkstyle2(leave_flowass_desigvalid)
        leave_flowass_emptype_label = checkstyle2(leave_flowass_emptypevalid)
        leave_flowass_ishead_label = checkstyle2(leave_flowass_isheadvalid)
        leave_flowass_numdays_label = checkstyle2(leave_flowass_numdaysvalid)
        leave_flowass_unit_label = checkstyle2(leave_flowass_unitvalid)
        leave_flowass_leaveflow_label = checkstyle2(leave_flowass_leaveflowvalid)

        # bpflowass_emptype_label = checkstyle2(bpflowass_emptypevalid)
        # bpflowass_appttype_label = checkstyle2(bpflowass_appttypevalid)
        # bpflowass_numfail_label = checkstyle2(bpflowass_numfailvalid)
        # bpflowass_sg_label = checkstyle2(bpflowass_sgvalid)
        # bpflowass_bpflow_label = checkstyle2(bpflowass_bpflowvalid)
        # bpflowass_funding_label = checkstyle2(bpflowass_fundingvalid)
        # # bpflowass_replacement_label = checkstyle2(bpflowass_replacementvalid)
        # bpflowass_sr_emp_class_label = checkstyle2(bpflowass_sr_emp_classvalid)

        allvalid = [leave_flowass_leavetypevalid, leave_flowass_desigvalid, leave_flowass_emptypevalid, leave_flowass_isheadvalid, leave_flowass_numdaysvalid, leave_flowass_unitvalid, leave_flowass_leaveflowvalid]

        # bpflowass_emptypevalid, bpflowass_appttypevalid, bpflowass_numfailvalid, bpflowass_sgvalid, bpflowass_bpflowvalid, bpflowass_fundingvalid, bpflowass_sr_emp_classvalid]

        if all(allvalid):

            leave_flowass_submitmodal1 = True

        if eventid in ['leave_flowass_submitbtn','leave_flowass_submitmodal1go', 'leave_flowass_submitmodal1back']:
            if eventid in ['leave_flowass_submitmodal1go', 'leave_flowass_submitmodal1back']:

                leave_flowass_submitmodal1 = False


            return [leave_flowass_leavetype_label,
                leave_flowass_desig_label,
                leave_flowass_emptype_label,
                leave_flowass_ishead_label,
                leave_flowass_numdays_label,
                leave_flowass_unit_label,
                leave_flowass_leaveflow_label,
                leave_flowass_submitmodal1]


            # bpflowass_emptype_label,
            #         bpflowass_appttype_label,
            #         bpflowass_numfail_label,
            #         bpflowass_sg_label,
            #         bpflowass_bpflow_label,
            #         bpflowass_funding_label,
            #         bpflowass_sr_emp_class_label,
            #         # bpflowass_replacement_label,
            #         bpflowass_submitmodal1]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('leave_flowass_submitmodal2', 'is_open')

    ],
    [
        Input('leave_flowass_submitmodal1go', 'n_clicks'),
        Input('leave_flowass_submitmodal2_closebtn', 'n_clicks')

    ],
    [
        State('leave_flowass_leavetype', 'value'),
        State('leave_flowass_desig', 'value'),
        State('leave_flowass_emptype', 'value'),
        State('leave_flowass_ishead', 'value'),
        State('leave_flowass_numdays', 'value'),
        State('leave_flowass_unit', 'value'),
        State('leave_flowass_leaveflow', 'value'),

        # State('bpflowass_emptype', 'value'),
        # State('bpflowass_appttype', 'value'),
        # State('bpflowass_numfail', 'value'),
        # State('bpflowass_sg', 'value'),
        # State('bpflowass_bpflow', 'value'),
        # State('bpflowass_funding', 'value'),
        # State('bpflowass_unit', 'value'),
        # State('bpflowass_desig', 'value'),
        # State('bpflowass_sr_emp_class', 'value'),
        # State('bpflowass_replacement', 'value'),
        State('leave_flowass_chkmarkfordeletion', 'value'),
        State('url', 'search'),
        State('current_user_id', 'data'),

    ]
)

def leavefa_submitmodal(leave_flowass_submitmodal1go, leave_flowass_submitmodal2_closebtn,
                            leave_flowass_leavetype, leave_flowass_desig, leave_flowass_emptype, leave_flowass_ishead, leave_flowass_numdays, leave_flowass_unit,
                            leave_flowass_leaveflow,
                            leave_flowass_chkmarkfordeletion,
                            url,
                            current_user_id):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        if ctx.triggered:
            mode = str(parse_qs(parsed.query)['mode'][0])
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'leave_flowass_submitmodal1go':

                if mode == "add":



                    print(leave_flowass_unit, 'leave_flowass_unit')
                    for i in leave_flowass_unit:
                        # sql6 = '''
                        #     SELECT MAX(leave_flow_assignment_priority_id) as flow_max_priority
                        #     FROM leave_flow_assignment
                        #     WHERE leave_flow_assignment_delete_ind = %s
                        #
                        # '''
                        #
                        # values6 = (False, )
                        # columns6 = ['flow_max_priority']
                        # df6 = securequerydatafromdatabase(sql6, values6, columns6)
                        # if df6["flow_max_priority"][0] == None:
                        #     flow_max_priority = 0
                        # else:
                        #     flow_max_priority = int(df6["flow_max_priority"][0])

                        sql1 = """
                            INSERT INTO leave_flow_assignment(leave_flow_assignment_designation_id, leave_flow_assignment_numdays, leave_flow_assignment_emp_class_id, leave_flow_assignment_ishead_id,
                                leave_flow_assignment_flow_id,
                                leave_flow_assignment_unit_id,
                                leave_flow_assignment_inserted_by, leave_flow_assignment_inserted_on, leave_flow_assignment_delete_ind,
                                leave_flow_assignment_leavetype_id)
                            VALUES (%s, %s, %s, %s, %s,
                                %s,
                                %s, %s, %s,
                                %s)
                            RETURNING leave_flow_assignment_id

                        """

                        values1 = [leave_flowass_desig, leave_flowass_numdays, leave_flowass_emptype, leave_flowass_ishead, leave_flowass_leaveflow,
                            i,
                            current_user_id, datetime.now(), False,
                            leave_flowass_leavetype
                        ]

                        leave_flow_assignment_id = modifydatabasereturnid(sql1, values1)
                        print(leave_flow_assignment_id, 'leave_flow_assignment_id')

                        sql2 = """
                            UPDATE leave_flow_assignment SET
                                leave_flow_assignment_priority_id=%s

                            WHERE leave_flow_assignment_id=%s

                        """

                        values2 = [leave_flow_assignment_id, leave_flow_assignment_id]
                        modifydatabase(sql2, values2)



                elif mode == "edit":
                    # print('bpflowass_chkmarkfordeletion', bpflowass_chkmarkfordeletion)
                    leave_flow_assignment_id = str(parse_qs(parsed.query)['leave_flow_assignment_id'][0])

                    leave_flowass_deletevalue = False
                    if type(leave_flowass_unit) is list:
                        leave_flowass_unitfirst = leave_flowass_unit[0]
                    else:
                        leave_flowass_unitfirst = leave_flowass_unit

                    if 1 in leave_flowass_chkmarkfordeletion or '1' in leave_flowass_chkmarkfordeletion:
                        leave_flowass_deletevalue = True
                    else:
                        leave_flowass_deletevalue = False


                    print(leave_flowass_unitfirst, 'leave_flowass_unitfirst')
                    # print(leave_flowass_unit[0], 'leave_flowass_unit[0]')

                    sql1 = """
                        UPDATE leave_flow_assignment SET
                            leave_flow_assignment_designation_id=%s, leave_flow_assignment_numdays=%s, leave_flow_assignment_emp_class_id=%s, leave_flow_assignment_ishead_id=%s,
                                leave_flow_assignment_flow_id=%s,
                                leave_flow_assignment_unit_id=%s,
                                leave_flow_assignment_inserted_by=%s, leave_flow_assignment_inserted_on=%s, leave_flow_assignment_delete_ind=%s,
                                leave_flow_assignment_leavetype_id=%s

                        WHERE leave_flow_assignment_id=%s
                    """

                    values1 = [leave_flowass_desig, leave_flowass_numdays, leave_flowass_emptype, leave_flowass_ishead, leave_flowass_leaveflow,
                            leave_flowass_unitfirst,
                            current_user_id, datetime.now(), leave_flowass_deletevalue,
                            leave_flowass_leavetype,
                            leave_flow_assignment_id]

                    modifydatabase(sql1, values1)

                    if leave_flowass_deletevalue == False and type(leave_flowass_unit) is list:

                        for i in leave_flowass_unit[1:]:
                            print(i, 'i')
                            sql12 = """
                                INSERT INTO leave_flow_assignment(leave_flow_assignment_designation_id, leave_flow_assignment_numdays, leave_flow_assignment_emp_class_id, leave_flow_assignment_ishead_id,
                                    leave_flow_assignment_flow_id,
                                    leave_flow_assignment_unit_id,
                                    leave_flow_assignment_inserted_by, leave_flow_assignment_inserted_on, leave_flow_assignment_delete_ind,
                                    leave_flow_assignment_leavetype_id)
                                VALUES (%s, %s, %s, %s, %s,
                                    %s,
                                    %s, %s, %s,
                                    %s)
                                RETURNING leave_flow_assignment_id

                            """

                            values12 = [leave_flowass_desig, leave_flowass_numdays, leave_flowass_emptype, leave_flowass_ishead, leave_flowass_leaveflow,
                                i,
                                current_user_id, datetime.now(), False,
                                leave_flowass_leavetype
                            ]
                            leave_flow_assignment_id = modifydatabasereturnid(sql12, values12)

                            sql22 = """
                                UPDATE leave_flow_assignment SET
                                    leave_flow_assignment_priority_id=%s

                                WHERE leave_flow_assignment_id=%s

                            """

                            values22 = [leave_flow_assignment_id, leave_flow_assignment_id]
                            modifydatabase(sql22, values22)

                    else:
                        pass

                return [True]

            elif eventid == "leave_flowass_submitmodal2_closebtn":

                return [False]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
