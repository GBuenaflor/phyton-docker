import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
from dash.dependencies import Input, Output, State
from apps import commonmodules
from apps.commonmodules import queryfordropdown
from dash.exceptions import PreventUpdate
from app import app
import urllib.parse as urlparse
from urllib.parse import parse_qs
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid
from apps.commonmodules import checkiflengthzero2, checkstyle2, generate_empnum
import hashlib
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
from datetime import datetime as dt



layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),

    html.Div([
        html.H1("Employee Management"),
        dcc.Link('← Back to list of Employees', href='/settings/settings_employee_management'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                # dbc.Button("Create Personal Data Entry", color="primary", className="mr-1",
                #            id="add_pds", href="/settings/settings_personal_data_profile?mode=add"),
            ])
        ]),
        dbc.Card([
            dbc.CardHeader(
                html.H4("Create Employee Profile", id = "empman_header"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
            #     html.Div([
            #         dbc.FormGroup(
            #             [
            #                 dbc.RadioItems(
            #                     options=[
            #                         {"label": "Search Persons Without BPs", "value": 1},
            #                         {"label": "Search Persons from Original BPs", "value": 2},
            #
            #                     ],
            #                     value=1,
            #                     id="empman_personradio",
            #                 ),
            #             ]
            #         )
            #
            #     ]),

                html.Div([
                    dbc.FormGroup(
                        [
                            dbc.RadioItems(
                                options=[
                                    {"label": "Search Persons Without BPs", "value": 1},
                                    {"label": "Search Persons from Original BPs", "value": 2},

                                ],
                                value=1,
                                id="empman_personradio",
                            ),
                        ]
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Select Person to Create Employee Profile For", width=4,
                                      style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='empoptions'
                                ),

                            ],
                                width=8
                            )
                        ],
                        row=True
                    ),
                    html.Br(),
                    html.Hr(),
                    html.Br(),
                ], id = 'empman_empdd_div'),


                html.Div([
                    html.H3("Personal Data"),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Last Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label("<content>", id = 'emp_last_name', style={"text-align": "left"})
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("First Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label("<content>", id = 'emp_first_name', style={"text-align": "left"})
                                ], width=8)
                            ], row=True),

                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Middle Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label("<content>", id = 'emp_middle_name', style={"text-align": "left"})
                                ], width=8)
                            ], row=True),

                        ])

                    ]),
                    html.Br(),
                    html.Hr(),
                    html.Br(),
                ], id = 'empman_personaldata_div'),



                dbc.FormGroup(
                    [
                        dbc.Label("Employee Type*", id = 'emp_typelabel', width=4,
                                  style={"text-align": "left"}),
                        dbc.Col([
                            dcc.Dropdown(
                                id='emp_type',
                            ),
                        ],
                            width=4
                        )
                    ],
                    row=True, style = {'display':'none'}
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Employee Number*", width=4,
                                  style={"text-align": "left"}, id = 'emp_num_label'),
                        dbc.Col([
                            dbc.Label(
                                # type="text",
                                id='emp_num'
                            ),
                        ],
                            width=2
                        ),

                        # dbc.Col([
                        #     dbc.Button("Generate Employee Number", color="primary", className="mr-1",
                        #                id="generate_emp_num"),
                        # ],
                        #     width=2
                        # )
                    ],
                    row=True
                ),

                dbc.FormGroup(
                    [
                        dbc.Label("Employee Status*", id = 'emp_statuslabel', width=4,
                                  style={"text-align": "left"}),
                        dbc.Col([
                            dcc.Dropdown(
                                id='emp_status',
                            ),
                        ],
                            width=4
                        )
                    ],
                    row=True
                ),

                dbc.FormGroup([
                    dbc.Label("UP Email Address", width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dbc.Input(
                            type="text", id='emp_email'
                        )
                    ],width=4)
                ],row=True),

                dbc.FormGroup([
                    dbc.Label("Primary Designation*", id = 'emp_desiglabel', width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dcc.Dropdown(
                            id='emp_desig',
                        ),
                    ], width=4)
                ], row=True),

                dbc.FormGroup([
                    dbc.Label("Home Unit*", id = 'emp_unitlabel', width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dcc.Dropdown(
                            id='emp_unit',
                        ),
                    ], width=4)
                ], row=True),

                dbc.FormGroup([
                    dbc.Label("Salary Grade", width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dcc.Dropdown(
                            id='emp_sg',
                        ),
                    ], width=4)
                ], row=True),

                dbc.FormGroup([
                    dbc.Label("Salary", width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dbc.Input(
                            type="text", id='emp_salary'
                        )
                    ], width=4)
                ], row=True),

                dbc.FormGroup([
                    dbc.Label("UP Provident Fund Number", width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dbc.Input(
                            type="text", id='emp_uppf'
                        )
                    ], width=4)
                ], row=True),

                dbc.FormGroup([
                    dbc.Label("Active/Inactive*", id = 'emp_is_activelabel', width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dcc.Dropdown(
                            id='emp_is_active',
                            options=[
                                {'label': 'Active', 'value': 1},
                                {'label': 'Inactive', 'value': 0},
                            ],
                        ),
                    ], width=4)
                ], row=True),

                html.Div([
                    html.Hr(),
                    html.H3("Employee Class Input (For BP Error Correction Only)"),
                    dbc.FormGroup([
                    dbc.Label("Employee Class", id = 'emp_is_activelabel', width=4,
                              style={"text-align": "left"}),
                    dbc.Col([
                        dcc.Dropdown(
                            id='emp_class',
                            options=[
                                {'label': 'Faculty', 'value': 1},
                                {'label': 'Admin', 'value': 2},
                                {'label': 'REPS', 'value': 3},
                            ],
                        ),
                    ], width=4)
                ], row=True),


                ], id = 'empman_empclassdiv', style = {'display':'none'}),



                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Employee Profile", color="primary", className="mr-1",
                                   id="empman_submitbtn", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="school_cancel",
                                   href='/settings/settings_employee_management', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Employee Entry Confirmation", id='empman_submitmodal1_header'),
                        dbc.ModalBody("Confirm Employee Entry Submission", id='empman_submitmodal1_body'),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id="empman_submitmodal1go", className="mr-1", color='primary'),
                            dbc.Button("Back", id='empman_submitmodal1back', className="ml-auto")
                        ]),
                    ],
                    id="empman_submitmodal1",
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("Update Successful", id = 'empman_submitmodal2_header'),
                        dbc.ModalBody("Employee Database has been successfully updated.", id = 'empman_submitmodal2_body'),
                        dbc.ModalFooter([
                            dbc.Button("Back to Home", id='empman_submitmodal2home', className="ml-auto",
                                       href='/home'),
                            dbc.Button("Back to Employee Management", id='empman_submitmodal2back', className="ml-auto", href = '/settings/settings_employee_management')
                        ]),
                    ],
                    id="empman_submitmodal2",
                ),


            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        ),

        html.Div([
            dcc.Input(id='empman_valid_status', type='text', value="0")
        ], style={'display': 'none'}),
        html.Div([
            dcc.Input(id='empman_pagemode', type='text', value="0")
        ], style={'display': 'none'}),
    ], id = 'empman_maindiv'),

])


@app.callback([

    Output('emp_desig', 'options'),
    Output('emp_unit', 'options'),

],
    [
    Input('empman_pagemode', 'value'),
    Input('empoptions', 'value')
],
    [
        State('url', 'search'),
        State('empman_personradio', 'value')
    ],


)

def fillindropdowns(empman_pagemode, empoptions, url, empman_personradio):
    emp_desig = []
    emp_unit = []

    ctx = dash.callback_context
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]

    if empman_personradio == 2:#select persons from BP
        if empman_pagemode == 1:
            if eventid == "empoptions":
                desigoptions = commonmodules.queryfordropdown('''
                            SELECT d.designation_name as label, bp.bp_designation_id as value
                            FROM persons p
                            INNER JOIN basic_papers bp ON p.person_id = bp.person_id
                            INNER JOIN designations d ON d.designation_id = bp.bp_designation_id
                            WHERE p.person_id = %s
                            AND bp_delete_ind = %s

                       ''', (empoptions, False,))

                unitoptions = commonmodules.queryfordropdown('''
                            SELECT u.unit_name as label, bp.bp_designation_unit_id as value
                            FROM persons p
                            INNER JOIN basic_papers bp ON p.person_id = bp.person_id
                            INNER JOIN units u on u.unit_id = bp.bp_designation_unit_id
                            WHERE p.person_id = %s
                            AND bp_delete_ind = %s

                       ''', (empoptions, False,))
            else:
                raise PreventUpdate


        elif empman_pagemode == 2:


            parsed = urlparse.urlparse(url)
            emp_id = str(parse_qs(parsed.query)['emp_id'][0])


            desigoptions = commonmodules.queryfordropdown('''
                        SELECT DISTINCT d.designation_name as label, sr.sr_design_id as value
                        FROM employees e
                        INNER JOIN service_records sr ON sr.emp_id = e.emp_id
                        INNER JOIN designations d ON d.designation_id = sr.sr_design_id
                        WHERE e.emp_id = %s
                        AND sr.sr_delete_ind = %s


                   ''', (emp_id, False,))


            unitoptions = commonmodules.queryfordropdown('''
                        SELECT DISTINCT u.unit_name as label, sr.sr_unit_id as value
                        FROM employees e
                        INNER JOIN service_records sr ON sr.emp_id = e.emp_id
                        INNER JOIN units u on u.unit_id = sr.sr_unit_id
                        WHERE e.emp_id = %s
                        AND sr.sr_delete_ind = %s

                   ''', (emp_id, False,))



            return [desigoptions, unitoptions]

    elif empman_personradio == 1:#select persons without BP

        desigoptions = commonmodules.queryfordropdown('''
                    SELECT designation_name as label, designation_id as value
                    FROM designations
                    WHERE designation_delete_ind = %s


               ''', (False,))

        unitoptions = commonmodules.queryfordropdown('''
                    SELECT unit_name as label, unit_id as value
                    FROM units
                    WHERE unit_delete_ind = %s

               ''', (False,))

        return [desigoptions, unitoptions]

    else:
        raise PreventUpdate



@app.callback([
    Output('empoptions', 'options'),
    Output('emp_type', 'options'),
    Output('emp_status', 'options'),
    Output('emp_sg', 'options'),
],
    [
    Input('empman_pagemode', 'value'),
    Input('empman_personradio', 'value')
],
    [
        State('url', 'search'),

    ],


)

def fillindropdowns(empman_pagemode, empman_personradio, url):


    parsed = urlparse.urlparse(url)
    mode = str(parse_qs(parsed.query)['mode'][0])

    emp_id = 0
    emplist = []
    emp_type = []
    emp_status = []
    emp_sg = []

    emp_type = commonmodules.queryfordropdown('''
                SELECT emp_class_name as label, emp_class_id as value
                FROM emp_classes
                WHERE emp_class_delete_ind = %s

           ''', (False,))

    emp_status = commonmodules.queryfordropdown('''
                SELECT emp_status_name as label, emp_status_id as value
                FROM emp_statuses
                WHERE emp_status_delete_ind = %s

           ''', (False,))

    emp_sg = commonmodules.queryfordropdown('''
                SELECT sg_number_step as label, sg_id as value
                FROM salary_grades
                WHERE sg_delete_ind = %s

           ''', (False,))

    if empman_pagemode == 1:
        if empman_personradio == 2:

    #     print("HEREEEE@2")
            emplist = commonmodules.queryfordropdown('''
                        SELECT p.person_xname || ' - ' || d.designation_name || ' - ' || u.unit_code as label, p.person_id as value
                        FROM bp_status_changes bsc
                        INNER JOIN basic_papers bp ON bp.bp_id = bsc.bp_id
                        INNER JOIN persons p on p.person_id = bp.person_id
                        INNER JOIN designations d on d.designation_id = bp.bp_designation_id
                        INNER JOIN units u on u.unit_id = bp.bp_designation_unit_id
                        WHERE bsc.bp_status_id IN %s
                        AND bsc.bp_status_change_current_ind = %s
                        ORDER BY p.person_last_name

                   ''', ((26, 34), True))

        if empman_personradio == 1:


            emplist = commonmodules.queryfordropdown('''
                SELECT CASE WHEN p.person_last_name IS NULL THEN '' ELSE p.person_last_name END || ', ' || CASE WHEN p.person_first_name IS NULL THEN '' ELSE p.person_first_name END || ' ' || CASE WHEN p.person_middle_name IS NULL THEN '' ELSE p.person_middle_name END as label, p.person_id as value
                FROM persons p
                WHERE person_id NOT IN (SELECT p.person_id
                FROM persons p
                INNER JOIN employees e ON p.person_id = e.person_id)
                AND person_delete_ind = %s
                ORDER BY p.person_last_name

                               ''', (False,))

    return [emplist, emp_type, emp_status, emp_sg]


@app.callback(
    [
        Output('empman_pagemode', 'value')
    ],
    [
        Input("url", "search"),
    ]
)

def determode(url):

    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        if parse_qs(parsed.query)['mode'][0] == "add":
            empman_pagemode = 1
        elif parse_qs(parsed.query)['mode'][0] == "edit":
            empman_pagemode = 2


        return [empman_pagemode]

    else:
        raise PreventUpdate



@app.callback(
    [
     Output('emp_last_name', 'children'),
     Output('emp_first_name', 'children'),
     Output('emp_middle_name', 'children'),

     Output('emp_num', 'children'),
     Output('emp_status', 'value'),
     Output('emp_email', 'value'),
     Output('emp_desig', 'value'),

     Output('emp_unit', 'value'),
     Output('emp_sg', 'value'),
     Output('emp_salary', 'value'),
     Output('emp_uppf', 'value'),
     Output('emp_is_active', 'value'),
     Output('emp_class', 'value'),
     Output('empman_empclassdiv', 'style'),
     Output('emp_num_label', 'children'),
     Output('empman_header', 'children'),
     ],

    [Input("url", "search"),
     Input("empoptions", "value"),
     Input('emp_type', 'value')],
    [State('url','path'),
     State('empman_header', 'children'),
     State('empman_valid_status', 'value'),
     State('sessioncurrentunit', 'data'),
     State('sessionlistofunits', 'data'),
     ]

)
def loadempprofile(url, empoptions, emp_type,
                   url_state, empman_header, empman_valid_status, sessioncurrentunit, sessionlistofunits):


    person_id = empoptions

    ctx = dash.callback_context
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    parsed = urlparse.urlparse(url)

    if parse_qs(parsed.query):
        if parse_qs(parsed.query)['mode'][0] == "edit":
            emp_id = str(parse_qs(parsed.query)['emp_id'][0])
            sqlcommand = '''SELECT emp_primary_home_unit_id
                                            FROM employees
                                            WHERE emp_id = %s
                            '''
            values = (emp_id,)
            columns = ['emp_primary_home_unit_id']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            if df["emp_primary_home_unit_id"][0] in sessionlistofunits[str(sessioncurrentunit)]:

                empman_valid_status = 1
                style = {'display': 'inline'}
            else:

                empman_valid_status = 0
                style = {'display': 'none'}

            if empman_valid_status == 1:

                emp_num_label = "Employee Number*"
                emp_id = parse_qs(parsed.query)['emp_id'][0]

                sql = '''
                    SELECT emp_class_id,  emp_number, emp_status_id, emp_up_email_add, emp_primary_designation_id,
                            emp_primary_home_unit_id, emp_salary_grade_id, emp_salary_amount, emp_uppf_number, person_last_name,
                            person_first_name, person_middle_name, emp_is_active
                    FROM employees e
                    INNER JOIN persons p ON p.person_id = e.person_id
                    WHERE emp_id = %s
                '''

                values = (int(emp_id),)
                columns = ['emp_class_id', 'emp_number', 'emp_status_id', 'emp_up_email_add', 'emp_primary_designation_id',
                           'emp_primary_home_unit_id', 'emp_salary_grade_id', 'emp_salary_amount', 'emp_uppf_number', 'person_last_name',
                            'person_first_name', 'person_middle_name', 'emp_is_active']


                df = securequerydatafromdatabase(sql, values, columns)
                print('HERE234234', sql, values, df)

                emp_class_id = df["emp_class_id"][0]
                emp_number = df["emp_number"][0]
                emp_status_id = df["emp_status_id"][0]
                emp_up_email_add = df["emp_up_email_add"][0]
                emp_primary_designation_id = df["emp_primary_designation_id"][0]
                emp_primary_home_unit_id = df["emp_primary_home_unit_id"][0]
                emp_salary_grade_id = df["emp_salary_grade_id"][0]
                emp_salary_amount = df["emp_salary_amount"][0]
                emp_uppf_number = df["emp_uppf_number"][0]
                person_last_name = df["person_last_name"][0]
                person_first_name = df["person_first_name"][0]
                person_middle_name = df["person_middle_name"][0]
                if df["emp_is_active"][0] == True:
                    emp_is_active = 1
                else:
                    emp_is_active = 0

                if df['emp_class_id'][0] is None:
                    emp_class_id = ""
                    emp_class_edit_div_style = {'display':'inline'}
                else:
                    emp_class_id = df['emp_class_id'][0]
                    emp_class_edit_div_style = {'display':'none'}

                return [person_last_name, person_first_name, person_middle_name, emp_number,
                        emp_status_id, emp_up_email_add, emp_primary_designation_id, emp_primary_home_unit_id, emp_salary_grade_id,
                        emp_salary_amount, emp_uppf_number, emp_is_active, emp_class_id,emp_class_edit_div_style,emp_num_label, "Edit Employee Profile"]

            else:
                raise PreventUpdate

        elif parse_qs(parsed.query)['mode'][0] == "add":

            if empoptions or emp_type:

                emp_num_label = "Autogenerated Employee Number*:"

                sql = '''
                        SELECT p.person_last_name, p.person_first_name, p.person_middle_name, bp.bp_emp_class_id, bp.bp_designation_status_id,
                                bp.bp_designation_id, bp.bp_designation_unit_id, bp.bp_salary_grade_id, bp.bp_salary_hon_amount
                        FROM persons p
                        LEFT JOIN basic_papers bp ON bp.person_id = p.person_id
                        WHERE p.person_id = %s
                '''

                values = (person_id,)

                columns = ['person_last_name', 'person_first_name', 'person_middle_name', 'bp_emp_class_id', 'bp_designation_status_id',
                                'bp_designation_id', 'bp_designation_unit_id', 'bp_salary_grade_id', 'bp_salary_hon_amount' ]

                df = securequerydatafromdatabase(sql, values, columns)

                person_last_name = df["person_last_name"][0]
                person_first_name = df["person_first_name"][0]
                person_middle_name = df["person_middle_name"][0]
                bp_emp_class_id = df["bp_emp_class_id"][0]
                bp_designation_status_id = df["bp_designation_status_id"][0]
                bp_designation_id = df["bp_designation_id"][0]
                bp_designation_unit_id = df["bp_designation_unit_id"][0]
                bp_salary_grade_id = df["bp_salary_grade_id"][0]
                bp_salary_hon_amount = df["bp_salary_hon_amount"][0]


                emp_num = generate_empnum(person_id, emp_type)

                return [person_last_name, person_first_name, person_middle_name, emp_num,
                            bp_designation_status_id, "", bp_designation_id, bp_designation_unit_id,
                            bp_salary_grade_id,
                            bp_salary_hon_amount, "", True, "",{'display':'none'},emp_num_label, empman_header]


            else:
                raise PreventUpdate

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([

    Output('empman_empdd_div', 'style'),
    Output('empman_personaldata_div', 'style'),
],
    [
    Input('url', 'search'),

],
)

def fillindropdowns(url):

    ctx = dash.callback_context
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "add":
            empman_empdd_div_style = {'display':'inline'}
            empman_personaldata_div_style = {'display':'none'}
        elif parse_qs(parsed.query)['mode'][0] == "edit":
            empman_empdd_div_style = {'display':'none'}
            empman_personaldata_div_style =  {'display':'inline'}

        return [empman_empdd_div_style, empman_personaldata_div_style]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("empman_submitmodal2", "is_open")
    ],
    [
        Input("empman_submitmodal1go", "n_clicks"),
        Input('empman_submitmodal2home', 'n_clicks'),
        Input("empman_submitmodal2back", "n_clicks")
     ],
    [

        State("url", "search"),
        State("emp_type", "value"),

        State("emp_num", "children"),
        State("emp_status", "value"),
        State("emp_email", "value"),
        State("emp_desig", "value"),
        State("emp_unit", "value"),

        State("emp_sg", "value"),
        State("emp_salary", "value"),
        State("emp_uppf", "value"),
        State('current_user_id', 'data'),
        State('empoptions', 'value'),
        State('emp_class', 'value'),
        State('emp_is_active', 'value')

     ],
)
def toggle_modal(empman_submitmodal1go, empman_submitmodal2home, empman_submitmodal2back,
                 url, emp_type,
                 emp_num,emp_status, emp_email, emp_desig, emp_unit,
                 emp_sg, emp_salary, emp_uppf, current_user_id,
                 person_id, emp_class, emp_is_active):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'empman_submitmodal1go':
            if parse_qs(parsed.query)['mode'][0] == "edit":
                emp_id = str(parse_qs(parsed.query)['emp_id'][0])
                # print('edit mode')
                if emp_is_active == 1:
                    emp_is_active_bool = True
                else:
                    emp_is_active_bool = False


                sqlupdate = '''
                    UPDATE employees
                    SET emp_class_id = %s, emp_status_id = %s, emp_up_email_add = %s, emp_primary_designation_id = %s, emp_primary_home_unit_id = %s,
                    emp_salary_grade_id = %s, emp_salary_amount = %s, emp_uppf_number = %s, emp_last_modified_by = %s, emp_last_modified_on = %s, emp_is_active = %s
                    WHERE emp_id = %s

                '''
                values = (emp_class, emp_status, emp_email, emp_desig, emp_unit, emp_sg, emp_salary, emp_uppf, current_user_id,datetime.now(), emp_is_active_bool, emp_id)

                modifydatabase(sqlupdate, values)

            if parse_qs(parsed.query)['mode'][0] == "add":

                sqlupdate = """
                    INSERT INTO employees(
                    person_id, emp_class_id, emp_number, emp_status_id, emp_up_email_add, emp_primary_designation_id, emp_primary_home_unit_id,
                    emp_salary_grade_id, emp_salary_amount, emp_uppf_number, emp_entry_id, emp_inserted_by, emp_inserted_on, emp_delete_ind, emp_class)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

                """


                values = (person_id, emp_type, emp_num, emp_status, emp_email, emp_desig, emp_unit, emp_sg, emp_salary, emp_uppf,1, current_user_id, datetime.now(), False, emp_class)

                modifydatabase(sqlupdate, values)

                sql1 = '''
                        SELECT emp_id
                        FROM employees
                        WHERE person_id = %s
                        AND emp_class_id = %s
                        AND emp_number = %s
                        AND emp_delete_ind = %s
                        ORDER BY emp_inserted_on DESC
                            '''

                values1 = (person_id, emp_type, emp_num, False)
                columns1 = ['emp_id']
                df1 = securequerydatafromdatabase(sql1, values1, columns1)

                new_emp_id = int(df1["emp_id"][0])

                sqlupdate8 = """
                    INSERT INTO emp_units(emp_id, unit_id, emp_unit_is_primary_home_unit,
                    emp_unit_inserted_by, emp_unit_inserted_on, emp_unit_delete_ind, emp_unit_is_active
                    )
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """
                values8= (new_emp_id, emp_unit, True, current_user_id, datetime.now(), False, True)
                modifydatabase(sqlupdate8, values8)


                sqlupdate = """
                    UPDATE persons SET person_temp_unit_id = %s
                    WHERE person_id = %s
                """
                values = (None, person_id)
                modifydatabase(sqlupdate, values)

            return [True]

        elif eventid in ['empman_submitmodal2home', 'empman_submitmodal2back']:

            return [False]

    else:
        raise PreventUpdate






#uideditsecurity
@app.callback([ Output('empman_maindiv','style'),
                Output('empman_valid_status', 'value'),
                Output('empman_submitbtn', 'children')
                ],
                [
                Input('url','pathname'),
                ],[
                  State('sessioncurrentunit','data'),
                  State('sessionlistofunits','data'),
                  State("url","search"),
                  State('empman_valid_status', 'value')
                ])
def empman_unit_security(url,sessioncurrentunit,sessionlistofunits, search, empman_valid_status):
    parsed = urlparse.urlparse(search)
    if parse_qs(parsed.query):
        if url=="/settings/settings_employee_management_profile":
            # print('HERE')
            mode = str(parse_qs(parsed.query)['mode'][0])
            if mode == "edit":
                emp_id = str(parse_qs(parsed.query)['emp_id'][0])
                sqlcommand = '''SELECT emp_primary_home_unit_id
                                FROM employees
                                WHERE emp_id = %s
                '''

                values = (emp_id,)
                columns = ['emp_primary_home_unit_id']
                df = securequerydatafromdatabase(sqlcommand,values,columns)

                if df["emp_primary_home_unit_id"][0] in sessionlistofunits[str(sessioncurrentunit)]:
                    # print('INHERE61', empman_valid_status)
                    empman_valid_status= 1
                    style = {'display':'inline'}
                else:
                    # print('INHERE62', empman_valid_status)
                    empman_valid_status= 0
                    style = {'display':'none'}

                return [style, empman_valid_status, "Save Changes"]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('empman_submitmodal1', 'is_open'),
        Output('emp_typelabel', 'style'),
        Output('emp_statuslabel', 'style'),
        Output('emp_desiglabel', 'style'),
        Output('emp_unitlabel', 'style'),
        Output('emp_is_activelabel', 'style'),
    ],
    [
        Input('empman_submitbtn', 'n_clicks'),
        Input('empman_submitmodal1go', 'n_clicks'),
        Input('empman_submitmodal1back','n_clicks')
    ],
    [
        State('emp_type', 'value'),
        State('emp_status', 'value'),
        State('emp_desig', 'value'),
        State('emp_unit', 'value'),
        State('emp_is_active', 'value'),

    ]
)

def empman_modal1(empman_submitbtn, empman_submitmodal1go, empman_submitmodal1back,
                  emp_type, emp_status, emp_desig, emp_unit, emp_is_active):

    empman_submitmodal1 = False
    # parsed = urlparse.urlparse(url)
    # if parsed.query:
    #     if parse_qs(parsed.query)['mode'][0] == "add":

    ctx = dash.callback_context
    if ctx.triggered:

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        # print('HERe25', emp_is_active, checkiflengthzero2(emp_is_active))

        emp_typevalid = checkiflengthzero2(emp_type)
        emp_statusvalid = checkiflengthzero2(emp_status)
        emp_desigvalid = checkiflengthzero2(emp_desig)
        emp_unitvalid = checkiflengthzero2(emp_unit)
        emp_is_activevalid = checkiflengthzero2(str(emp_is_active))

        emp_typelabel = checkstyle2(emp_typevalid)
        emp_statuslabel = checkstyle2(emp_statusvalid)
        emp_desiglabel = checkstyle2(emp_desigvalid)
        emp_unitlabel = checkstyle2(emp_unitvalid)
        emp_is_activelabel = checkstyle2(emp_is_activevalid)

        allvalid = [emp_statusvalid, emp_desigvalid, emp_unitvalid, emp_is_activevalid]

        if all(allvalid):

            empman_submitmodal1 = True
        print('HERE345', eventid, empman_submitmodal1)

        if eventid in ['empman_submitbtn', 'empman_submitmodal1go', 'empman_submitmodal1back']:
            print('HERE346', eventid, empman_submitmodal1)
            if eventid in ['empman_submitmodal1go', 'empman_submitmodal1back']:
                print('HERE347', eventid, empman_submitmodal1)
                empman_submitmodal1 = False
                print('HERE348', eventid, empman_submitmodal1)

            print('HERE34544', empman_submitmodal1)
            return [empman_submitmodal1,
                    emp_typelabel,
                    emp_statuslabel,
                    emp_desiglabel,
                    emp_unitlabel,
                    emp_is_activelabel]

    else:
        raise PreventUpdate
