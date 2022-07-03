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
from apps.commonmodules import checkiflengthzero, checkiflengthx, checkiflengthzero2, checkiflengthx2, safeupper, checkstyle2, ispersonexisting
from datetime import date as date
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
        html.H1("Person/Employee Encoding"),
        # dcc.Link('← Back to list of Employees', href='/settings/settings_employee_management'),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                # dbc.Button("Create Personal Data Entry", color="primary", className="mr-1",
                #            id="add_pds", href="/settings/settings_personal_data_profile?mode=add"),
            ])
        ]),
        dbc.Card([
            dbc.CardHeader(
                html.H4("Encode Employee Profile", id = "empman_header"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Spinner([


                dbc.CardBody([

                    dbc.FormGroup([
                        dbc.Label("First Name*", width=4,
                                  style={"text-align": "left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id='peremp_firstname'
                            ),
                            dbc.FormFeedback(
                                "Please enter valid last name", valid=False)
                        ], width=4)
                    ], row=True),

                    dbc.FormGroup([
                        dbc.Label("Middle Name", width=4,
                                  style={"text-align": "left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id='peremp_middlename'
                            ),
                            # dbc.FormFeedback(
                            #     "Please enter valid middle name", valid=False)
                        ], width=4)
                    ], row=True),

                    dbc.FormGroup([
                        dbc.Label("Last Name*", width=4,
                                  style={"text-align": "left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id='peremp_lastname'
                            ),
                            dbc.FormFeedback(
                                "Please enter valid last name", valid=False)
                        ], width=4)
                    ], row=True),

                    dbc.FormGroup([
                        dbc.Label("Name Extension", width=4,
                                  style={"text-align": "left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id='peremp_extension'
                            ),

                        ], width=4)
                    ], row=True),

                    dbc.FormGroup([
                        dbc.Label(
                            "Date of Birth*", id = 'peremp_doblabel',width=4, style={"text-align": "left", 'color': 'black'}),
                        dbc.Col([
                            dcc.DatePickerSingle(id='peremp_dob', placeholder="mm/dd/yyyy",
                                                 max_date_allowed=date.today()),
                            dbc.FormFeedback(
                                "Please enter valid date of birth", valid=False)
                            # dbc.FormFeedback(
                            #     "Please enter valid date", valid=False)
                        ], width=8)
                    ], row=True),

                    dbc.FormGroup([
                        dbc.Label("Place of Birth Local?*", width=4,
                                  id = 'peremp_pobislocallabel',style={"text-align": "left"}),
                        dbc.Col([
                            dcc.Dropdown(
                                id='peremp_pobislocal',
                                options=[
                                    {"label": "Local", "value": 1},
                                    {"label": "Other Country", "value": 2},
                                ],
                            ),

                            dbc.FormFeedback(
                                "Please select an option", valid=False)
                        ], width=4)
                    ], row=True),

                    html.Div([
                        dbc.FormGroup([
                            dbc.Label("Province of Birth*", width=4,
                                      id = 'peremp_pobprovincelabel',style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='peremp_pobprovince',
                                    options=[

                                    ],
                                ),

                            ], width=4)
                        ], row=True),
                    ], id = 'peremp_pobprovincediv', style = {'display':'none'}),


                    html.Div([
                        dbc.FormGroup([
                        dbc.Label("City of Birth*", width=4,
                                  id = 'peremp_pobcitylabel', style={"text-align": "left"}),
                        dbc.Col([
                            dcc.Dropdown(
                                id='peremp_pobcity',
                                options=[

                                ],
                            ),

                        ], width=4)
                    ], row=True),
                    ], id = 'peremp_pobcitydiv', style = {'display':'none'}),

                    html.Div([
                        dbc.FormGroup([
                            dbc.Label("Country of Birth*", width=4,
                                      id = 'peremp_pobcountrylabel', style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='peremp_pobcountry',
                                    options=[

                                    ],
                                ),

                            ], width=4)
                        ], row=True),
                    ], id = 'peremp_pobcountrydiv', style = {'display':'none'}),

                    html.Div([
                        dbc.FormGroup([
                            dbc.Label("City of Birth*", width=4,
                                      style={"text-align": "left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id='peremp_pob'
                                ),
                                dbc.FormFeedback(
                                    "Please enter valid city of birth", valid=False)
                            ], width=4)
                        ], row=True),
                    ], id = 'peremp_pobdiv', style = {'display':'none'}),

                    dbc.FormGroup([
                        dbc.Label("Employee Number*", width=4,
                                  style={"text-align": "left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id='peremp_empno'
                            ),
                            dbc.FormFeedback(
                                "Incorrect length or already taken", valid=False)
                        ], width=4)
                    ], row=True),

                    dbc.FormGroup(
                        [dbc.Label("Primary Unit*", id = 'peremp_unitlabel', width=4, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="peremp_unit",
                                 options=[
                                     # {'label': 'Faculty', 'value': '1'},
                                     # {'label': 'Administrative Personnel', 'value': '2'},
                                     # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                     # {'label': 'Others', 'value': '11'}
                                 ],
                                 searchable=True
                             ),
                             # dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=4
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Active/Inactive*", id='peremp_isactivelabel', width=4, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="peremp_isactive",
                                 options=[
                                     {'label': 'Active', 'value': True},
                                     {'label': 'Inactive', 'value': False},
                                     # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                     # {'label': 'Others', 'value': '11'}
                                 ],
                                 searchable=True
                             ),
                             # dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=4
                         )],
                        row=True
                    ),


                    dbc.Spinner([
                        dbc.Button("Submit Employee Profile", color="primary", className="mr-1",
                                   id="peremp_submitbtn",
                                   # href = '/settings/settings_person_employee_encoding?mode=add'
                                   )
                    ]),

                    dbc.Modal(
                        [
                            dbc.ModalHeader("Duplicate Person Detected", id='peremp_submitmodal1header'),
                            dbc.ModalBody("Person/Employee entry submission has been blocked since a duplicate person entry has been detected.",
                                          id='peremp_submitmodal1body'),
                            dbc.ModalFooter([

                                dbc.Button("Close", id='peremp_dupliclose', className="ml-auto")

                                # dbc.Button("Back to Home", id='peremp_submitmodal2_returnbtn', className="ml-auto", href = '/')
                            ]),
                        ],
                        id="peremp_duplimodal",
                    ),

                    dbc.Modal(
                        [
                            dbc.ModalHeader("Person/Employee Encoding Confirmation", id='peremp_submitmodal1header'),
                            dbc.ModalBody("Confirm Person/Employee Entry Submission",
                                          id='peremp_submitmodal1body'),
                            dbc.ModalFooter([
                                    dbc.Button("Confirm", id="peremp_submitmodal1go", className="mr-1",
                                               color='primary'),
                                    dbc.Button("Back", id='peremp_submitmodal1back', className="ml-auto")

                                # dbc.Button("Back to Home", id='peremp_submitmodal2_returnbtn', className="ml-auto", href = '/')
                            ]),
                        ],
                        id="peremp_submitmodal1",
                    ),



                    dbc.Modal(
                        [
                            dbc.ModalHeader("Person/Employee Encoding", id = 'peremp_submitmodal2_header'),
                            dbc.ModalBody("Employee Database has been successfully updated.", id = 'peremp_submitmodal2_body'),
                            dbc.ModalFooter([
                                dbc.Button(
                                    "Close", id='peremp_submitmodal2_closebtn', className="ml-auto",
                                           # href = '/settings/settings_person_employee_encoding',
                                           href = '/home',
                                           ),
                                # dbc.Button("Back to Home", id='peremp_submitmodal2_returnbtn', className="ml-auto", href = '/')
                            ]),
                        ],
                        id="peremp_submitmodal2",
                    ),


                ], style={'line-height': "1em", "display": "block"}),
            ]),
        ], style={'line-height': "1em", "display": "block"}
        ),

        # html.Div([
        #     dcc.Input(id='empman_valid_status', type='text', value="0")
        # ], style={'display': 'none'}),
        # html.Div([
        #     dcc.Input(id='empman_pagemode', type='text', value="0")
        # ], style={'display': 'none'}),
    ], id = 'peremp_maindiv'),

])

@app.callback(
    [
        Output("peremp_submitmodal2", "is_open"),

     ],
    [Input("peremp_submitmodal1go", "n_clicks"),
     Input("peremp_submitmodal2_closebtn", "n_clicks")],
    [

        State("peremp_firstname", "value"),
        State("peremp_middlename", "value"),
        State("peremp_lastname", "value"),
        State('peremp_extension', 'value'),
        State("peremp_dob", "date"),
        State("peremp_pob", "value"),
        State("peremp_empno", "value"),
        State('peremp_unit', 'value'),
        State('peremp_isactive', 'value'),
        State('current_user_id', 'data'),

        State('peremp_pobislocal', 'value'),
        State('peremp_pobprovince', 'value'),
        State('peremp_pobcity', 'value'),
        State('peremp_pobcountry', 'value'),



     ],
)
def toggle_modal(peremp_submitbtn, peremp_submitmodal2_closebtn,
                 peremp_firstname, peremp_middlename, peremp_lastname, peremp_extension,
                 peremp_dob, peremp_pob, peremp_empno, peremp_unit, peremp_isactive, current_user_id,
                 peremp_pobislocal, peremp_pobprovince, peremp_pobcity, peremp_pobcountry

                 ):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'peremp_submitmodal1go':


            peremp_firstname = safeupper(peremp_firstname)
            peremp_lastname = safeupper(peremp_lastname)
            peremp_middlename = safeupper(peremp_middlename)
            peremp_pob = safeupper(peremp_pob)
            peremp_extension = safeupper(peremp_extension)
            peremp_xname = peremp_firstname + " " + peremp_middlename + " " + peremp_lastname

            sql1 = """
                INSERT INTO persons(person_last_name,person_first_name,person_middle_name, person_dob, person_pob,
                                    person_inserted_by, person_inserted_on, person_delete_ind, person_name_extension,
                                    person_pob_is_local, person_pob_country_id, person_pob_city_id, person_pob_prov_id, person_entry_id,
                                    person_xname, person_is_active)
                VALUES (%s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s)
            """
            if peremp_pobislocal == 1:
                peremp_pobislocal = True
            elif peremp_pobislocal == 2:
                peremp_pobislocal = False
            else:
                raise PreventUpdate

            values1 = [peremp_lastname, peremp_firstname, peremp_middlename, peremp_dob, peremp_pob,
                            current_user_id, datetime.now(), False, peremp_extension,
                       peremp_pobislocal, peremp_pobcountry, peremp_pobcity,  peremp_pobprovince, 2, peremp_xname, peremp_isactive]

            modifydatabase(sql1, values1)

            sql4 = '''
                            SELECT person_id
                            FROM persons
                            WHERE person_last_name = %s
                            AND person_first_name = %s
                            AND person_middle_name = %s
                            AND person_delete_ind = %s
                        '''

            values4 = (peremp_lastname, peremp_firstname, peremp_middlename, False)
            columns4 = ['person_id']
            df4 = securequerydatafromdatabase(sql4, values4, columns4)

            person_id = int(df4['person_id'][0])

            # person_id = modifydatabasereturnid(sql1, values1)

            sql2 = """
                INSERT INTO employees(person_id, emp_number, emp_inserted_by, emp_inserted_on, emp_delete_ind, emp_primary_home_unit_id, emp_is_active, emp_entry_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values2 = [person_id, peremp_empno, current_user_id, datetime.now(), False, peremp_unit, False, 2]
            modifydatabase(sql2, values2)

            return [True]

        elif eventid == 'peremp_submitmodal2_closebtn':

            return [False]

    else:
        raise PreventUpdate




@app.callback([

    Output('peremp_unit', 'options'),
    Output('peremp_pobprovince', 'options'),
    Output('peremp_pobcountry', 'options'),

],
    [
    Input('url', 'search'),
],
    [
    ],


)

def fillindropdowns4(url):
    emp_desig = []
    emp_unit = []

    sql1 = '''
        WITH RECURSIVE subordinates AS (
            SELECT unit_id,	unit_parent_id,	unit_name
            FROM units
            WHERE unit_id = %s
            UNION
                SELECT e.unit_id,e.unit_parent_id,e.unit_name
                FROM units e
                INNER JOIN subordinates s ON s.unit_id = e.unit_parent_id
        ) SELECT * FROM subordinates

        '''

    values1 = (2,)
    columns1 = ['unit_id', 'unit_parent_id', 'unit_name']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)

    updunits = df1["unit_id"]
    updunits = tuple(updunits)

    unitoptions = commonmodules.queryfordropdown('''
                SELECT unit_name as label, unit_id as value
                FROM units
                WHERE unit_id IN %s
                ORDER BY unit_name ASC
           ''', (updunits,))

    peremp_pobprovinces = commonmodules.queryfordropdown('''
       SELECT prov_name as label, prov_id as value
       FROM provinces
       WHERE prov_delete_ind = %s
       ORDER BY prov_id
      ''', (False,))

    peremp_pobcountries = commonmodules.queryfordropdown('''
       SELECT country_name as label, country_id as value
       FROM countries
       WHERE country_delete_ind = %s
       ORDER BY country_name
      ''', (False,))



    return [unitoptions, peremp_pobprovinces, peremp_pobcountries]

# @app.callback([
#
#     Output('peremp_firstname', 'value'),
#     Output('peremp_middlename', 'value'),
#     Output('peremp_lastname', 'value'),
#     Output('peremp_extension', 'value'),
#     Output('peremp_dob', 'date'),
#     Output('peremp_pob', 'value'),
#     Output('peremp_empno', 'value'),
#     Output('peremp_unit', 'value'),
#
# ],
#     [
#     Input('url', 'pathname'),
# ],
#     [
#     ],
#
#
# )
#
# def fillindropdowns4(url):
#
#     return ["", "", "", "", datetime.now(), "", "", ""]

@app.callback([
    Output('peremp_pobcity', 'options'),

],
    [
    Input('peremp_pobprovince', 'value'),
],
    )
def toggle_cities_from_provinces_pob(peremp_pobprovince):
    if isinstance(peremp_pobprovince, int):

        peremp_citymuncurrent = commonmodules.queryfordropdown('''
                SELECT city_name as label, city_id as value
               FROM cities
               WHERE city_delete_ind = %s and prov_id = %s
               ORDER BY city_name
            ''', (False, peremp_pobprovince))

        return [peremp_citymuncurrent]

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('peremp_pobprovincediv', 'style'),
        Output('peremp_pobcitydiv', 'style'),
        Output('peremp_pobcountrydiv', 'style'),
        Output('peremp_pobdiv', 'style')

     ],
    [
        Input('peremp_pobislocal', 'value')

    ]
)

def peremp_pobdds(peremp_pobislocal):
    if peremp_pobislocal == 1:
        return [{'display':'inline'}, {'display':'inline'}, {'display':'none'}, {'display':'none'}]
    elif peremp_pobislocal == 2:
        return [{'display':'none'}, {'display':'none'}, {'display':'inline'}, {'display':'inline'}]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('peremp_submitmodal1', 'is_open'),
        Output('peremp_lastname', 'valid'), Output('peremp_lastname', 'invalid'),
        Output('peremp_firstname', 'valid'), Output('peremp_firstname', 'invalid'),
        # Output('peremp_middlename', 'valid'), Output('peremp_middlename', 'invalid'),
        Output('peremp_dob', 'valid'), Output('peremp_dob', 'invalid'),
        Output('peremp_pob', 'valid'), Output('peremp_pob', 'invalid'),
        Output('peremp_empno', 'valid'), Output('peremp_empno', 'invalid'),
        Output('peremp_unit', 'valid'), Output('peremp_unit', 'invalid'),
        Output('peremp_isactive', 'valid'), Output('peremp_isactive', 'invalid'),

        Output('peremp_doblabel', 'style'),
        Output('peremp_pobislocallabel', 'style'),
        Output('peremp_pobprovincelabel', 'style'),
        Output('peremp_pobcitylabel', 'style'),
        Output('peremp_pobcountrylabel', 'style'),
        Output('peremp_unitlabel', 'style'),
        Output('peremp_isactivelabel', 'style'),

        Output('peremp_duplimodal', 'is_open')


    ],
    [
        Input('peremp_submitbtn', 'n_clicks'),
        Input('peremp_submitmodal1go', 'n_clicks'),
        Input('peremp_submitmodal1back', 'n_clicks'),
        Input('peremp_dupliclose', 'n_clicks')
    ],
    [
        State("peremp_firstname", "value"),
        State("peremp_middlename", "value"),
        State("peremp_lastname", "value"),
        State('peremp_extension', 'value'),
        State("peremp_dob", "date"),
        State("peremp_pob", "value"),
        State("peremp_empno", "value"),
        State('peremp_unit', 'value'),
        State('peremp_isactive', 'value'),
        State('current_user_id', 'data'),

        State('peremp_pobislocal', 'value'),
        State('peremp_pobprovince', 'value'),
        State('peremp_pobcity', 'value'),
        State('peremp_pobcountry', 'value'),

        State('peremp_doblabel', 'style'),
        State('peremp_pobislocallabel', 'style'),
        State('peremp_pobprovincelabel', 'style'),
        State('peremp_pobcitylabel', 'style'),
        State('peremp_pobcountrylabel', 'style'),
        State('peremp_unitlabel', 'style'),
        State('peremp_isactivelabel', 'style'),

    ]

)

def peremp_openmodal1(peremp_submitbtn, peremp_submitmodal1go, peremp_submitmodal1back, peremp_dupliclose,
                      peremp_firstname, peremp_middlename, peremp_lastname, peremp_extension,
                      peremp_dob, peremp_pob, peremp_empno, peremp_unit, peremp_isactive, current_user_id,
                      peremp_pobislocal, peremp_pobprovince, peremp_pobcity, peremp_pobcountry,
                      peremp_doblabel,
                      peremp_pobislocallabel,
                      peremp_pobprovincelabel,
                      peremp_pobcitylabel,
                      peremp_pobcountrylabel,
                      peremp_unitlabel,
                      peremp_isactivelabel
                      ):
    peremp_submitmodal1 = False
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid in ['peremp_submitbtn', 'peremp_submitmodal1go', 'peremp_submitmodal1back', 'peremp_dupliclose']:

            if str(peremp_isactive).upper() in ['NONE']:
                peremp_isactive_str = ""
            else:
                peremp_isactive_str = str(peremp_isactive)

            peremp_lastnamevalid = checkiflengthzero2(peremp_lastname)
            peremp_firstnamevalid = checkiflengthzero2(peremp_firstname)
            peremp_dobvalid = checkiflengthzero2(peremp_dob)
            peremp_empnovalid = checkiflengthx2(peremp_empno, 9)
            peremp_unitvalid = checkiflengthzero2(peremp_unit)
            peremp_isactivevalid = checkiflengthzero2(peremp_isactive_str)
            peremp_pobislocalvalid = checkiflengthzero2(peremp_pobislocal)
            peremp_pobprovincevalid = checkiflengthzero2(peremp_pobprovince)
            peremp_pobcityvalid = checkiflengthzero2(peremp_pobcity)
            peremp_pobcountryvalid = checkiflengthzero2(peremp_pobcountry)
            peremp_pobvalid = checkiflengthzero2(peremp_pob)

            if (peremp_pobislocal and peremp_pobprovince and peremp_pobcity) or (
                    peremp_pobislocal and peremp_pobcountry and peremp_pob):

                peremp_finalvalid = True

            else:
                peremp_finalvalid = False

            peremp_doblabel = checkstyle2(peremp_dobvalid)
            peremp_pobislocallabel = checkstyle2(peremp_pobislocalvalid)
            peremp_pobprovincelabel = checkstyle2(peremp_pobprovincevalid)
            peremp_pobcitylabel = checkstyle2(peremp_pobcityvalid)
            peremp_pobcountrylabel = checkstyle2(peremp_pobcountryvalid)
            peremp_unitlabel = checkstyle2(peremp_unitvalid)
            peremp_isactivelabel = checkstyle2(peremp_isactivevalid)

            if peremp_empnovalid == True:

                sql1 = '''
                    SELECT emp_number
                    FROM employees
                '''

                values1 = (False,)
                columns1 = ['emp_number']
                allempnos = securequerydatafromdatabase(sql1, values1, columns1)
                allempnos_list = allempnos["emp_number"].tolist()
                if peremp_empno in allempnos_list:
                    peremp_empnovalid = False
                else:
                    peremp_empnovalid = True

            allvalid = [peremp_lastnamevalid, peremp_firstnamevalid,
                        # peremp_middlenamevalid,
                        peremp_dobvalid, peremp_empnovalid, peremp_unitvalid,
                        peremp_finalvalid, peremp_isactivevalid]

            if all(allvalid):
                peremp_submitmodal1 = True


            has_dupli = False
            duplimodal = has_dupli
            person_id = 0
            if eventid in ['peremp_submitbtn']:

                has_dupli = False
                person_id = 0
                has_dupli, person_id = ispersonexisting(peremp_firstname, peremp_middlename, peremp_lastname,
                                                        peremp_extension, peremp_dob)

                if has_dupli == True:
                    duplimodal = True
                    peremp_submitmodal1 = False
                else:
                    duplimodal = False

            if eventid in ['peremp_dupliclose']:
                duplimodal = False
                peremp_submitmodal1 = False


            return [peremp_submitmodal1,
                    peremp_lastnamevalid, not peremp_lastnamevalid,
                    peremp_firstnamevalid, not peremp_firstnamevalid,
                    # peremp_middlenamevalid, not peremp_middlenamevalid,
                    peremp_dobvalid, not peremp_dobvalid,
                    peremp_pobvalid, not peremp_pobvalid,
                    peremp_empnovalid, not peremp_empnovalid,
                    peremp_unitvalid, not peremp_unitvalid,
                    peremp_isactivevalid, not peremp_isactivevalid,

                    peremp_doblabel,
                    peremp_pobislocallabel,
                    peremp_pobprovincelabel,
                    peremp_pobcitylabel,
                    peremp_pobcountrylabel,
                    peremp_unitlabel,
                    peremp_isactivelabel,
                    duplimodal

                    ]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate
