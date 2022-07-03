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
from dash_extensions import Keyboard

layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Maintain Unit Tags of Employees"),
    html.Hr(),
    html.Div([
        dbc.Card([
            Keyboard(id="keyboard_query"),
            dbc.CardHeader(
                html.H4("Search Employee to Manage"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Select Unit", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        options=[

                                        ],
                                        id='query_emp_units',
                                        searchable=True, clearable=True
                                    ),
                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Select Employee Class", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        options=[

                                        ],
                                        id='query_emp_units_class',
                                        searchable=True, clearable=True
                                    ),
                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Last Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="searchname_emp_unit", placeholder="Enter search name"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search First Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="searchfname_emp_unit", placeholder="Enter search name"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Employee Number", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="searchnumber_emp_unit", placeholder="Enter search number"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Select Active Employees", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Include Current Employees Only", "value": 1},

                                        ],
                                        value=[1],
                                        id="query_employee_status_emp_unit",
                                        switch=True,
                                    ),
                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                ]),
                dbc.Row([
                        dbc.Col([
                            dbc.Button("Search", id="btn_search_employees_emp_unit",
                                       color="primary", block=True),
                        ]),
                        dbc.Col([
                        
                        ]),
                        ]),
                html.Hr(),
                html.H5("Employee List"),
                html.Div([

                ], id="queryfacultydiv_emp_unit"),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        #    Output('query_employee_class', 'options'),
        Output('query_emp_units', 'options'),
        Output('query_emp_units_class','options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
    ],
)
def fillindropdowns(pathname):

    if pathname == "/settings/settings_unit_emp":
        query_employee_class = commonmodules.queryfordropdown('''
            SELECT emp_class_name as label, emp_class_id as value
           FROM emp_classes
           WHERE emp_class_delete_ind = %s
           ORDER BY emp_class_id
        ''', (False, ))

        # query_employee_class
        return [commonmodules.queryunits(), query_employee_class]
    else:
        raise PreventUpdate


@app.callback([Output('queryfacultydiv_emp_unit', 'children')
               ],
              [

    Input('btn_search_employees_emp_unit', 'n_clicks'),
    Input("keyboard_query", "keydown")
],
    [
    State('searchname_emp_unit', 'value'),
    State('query_employee_status_emp_unit', 'value'),
    #State('query_employee_class', 'value'),
    State('sessioncurrentunit', 'data'),
    State('sessionlistofunits', 'data'),
    State('current_user_id', 'data'),
    State('searchnumber_emp_unit', 'value'),
    State('query_emp_units', 'value'),
    State('searchfname_emp_unit', 'value'),
    State('url','pathname'),
    State('query_emp_units_class','value')
],)
def querylistofemployees(btn_search_employees_emp_unit, keydown, searchname_emp_unit, query_employee_status_emp_unit,  sessioncurrentunit, sessionlistofunits,  # query_employee_class
                         current_user_id, searchnumber_emp_unit, query_emp_units, searchfname_emp_unit, pathname, query_emp_units_class):

    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    ctx = dash.callback_context

    mode="view"
    url='/settings/settings_unit_emp_profile'
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'btn_search_employees_emp_unit':

            if any([searchname_emp_unit, searchnumber_emp_unit, query_emp_units, searchfname_emp_unit]):  # query_employee_class
            #concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name)
                sqlcommand = '''SELECT emp_id, emp_number,

                coalesce(person_first_name, '') || ' ' || coalesce(person_middle_name, '') || ' ' || coalesce(person_last_name, '') || ' ' || coalesce(person_name_extension, '') AS name,


                unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                LEFT JOIN employees e ON e.person_id = p.person_id
                LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
                LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
                WHERE emp_delete_ind = %s
                '''
                values = [False]  # AND emp_primary_home_unit_id IN %s

                if 1 in query_employee_status_emp_unit:
                    sqlcommand = sqlcommand + " AND e.emp_is_active = %s "
                    values.append(True)

                if query_emp_units_class:
                    sqlcommand = sqlcommand + " AND e.emp_class_id = %s "
                    values.append(query_emp_units_class)

                if searchname_emp_unit:
                    sqlcommand = sqlcommand + " AND person_last_name ILIKE %s "  # + \
                    values.append(searchname_emp_unit+'%')

                if searchfname_emp_unit:
                    sqlcommand = sqlcommand + " AND person_first_name ILIKE %s "  # + \
                    values.append('%'+searchfname_emp_unit+'%')

                if searchnumber_emp_unit:
                    sqlcommand = sqlcommand + " AND emp_number ILIKE %s "  # + \
                    values.append('%'+searchnumber_emp_unit+'%')

                if query_emp_units:
                    sqlcommand = sqlcommand + " AND unit_id = %s "  # + \
                    values.append(query_emp_units)

                sqlcommand = sqlcommand + " ORDER BY person_last_name"
            else:
                raise PreventUpdate
                sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                LEFT JOIN employees e ON e.person_id = p.person_id
                LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
                LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
                WHERE emp_delete_ind = %s
                AND emp_is_active = %s
                ORDER BY person_last_name'''
                values = (False, True)  # AND emp_primary_home_unit_id IN %s

            columns = ['emp_id', 'emp_number', 'name', 'unit_name',
                       'emp_class', 'emp_status_name', 'designation_name']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["emp_id", "Emp Number", "Name", "Unit Name",
                          "Employee Class", "Status Name", "Designation Name"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'View', href=url+'?eid='+str(row["emp_id"])+'&mode='+mode)
            df = df[["Emp Number", "Name", "Unit Name",
                     "Employee Class", "Status Name", "Designation Name"]]
            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            if df.empty == True:
                table = "No entries found. Please check your search criteria."
            return [table]
        elif not keydown:
            raise PreventUpdate
        elif keydown['key'] == 'Enter':

            if any([searchname_emp_unit, searchnumber_emp_unit, query_emp_units, searchfname_emp_unit]):  # query_employee_class

                sqlcommand = '''SELECT emp_id, emp_number,

                coalesce(person_first_name, '') || ' ' || coalesce(person_middle_name, '') || ' ' || coalesce(person_last_name, '') || ' ' || coalesce(person_name_extension, '') AS name,


                unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                LEFT JOIN employees e ON e.person_id = p.person_id
                LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
                LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
                WHERE emp_delete_ind = %s
                '''
                values = [False]  # AND emp_primary_home_unit_id IN %s

                if 1 in query_employee_status_emp_unit:
                    sqlcommand = sqlcommand + " AND e.emp_is_active = %s "
                    values.append(True)
                if searchfname_emp_unit:
                    sqlcommand = sqlcommand + " AND person_first_name ILIKE %s "  # + \
                    values.append('%'+searchfname_emp_unit+'%')
                if query_emp_units_class:
                    sqlcommand = sqlcommand + " AND e.emp_class_id = %s "
                    values.append(query_emp_units_class)

                if searchname_emp_unit:
                    sqlcommand = sqlcommand + " AND person_last_name ILIKE %s "  # + \
                    values.append(searchname_emp_unit+'%')

                if searchnumber_emp_unit:
                    sqlcommand = sqlcommand + " AND emp_number ILIKE %s "  # + \
                    values.append('%'+searchnumber_emp_unit+'%')

                if query_emp_units:
                    sqlcommand = sqlcommand + " AND unit_id = %s "  # + \
                    values.append(query_emp_units)

                sqlcommand = sqlcommand + " ORDER BY person_last_name"
            else:
                raise PreventUpdate
                sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                LEFT JOIN employees e ON e.person_id = p.person_id
                LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
                LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
                WHERE emp_delete_ind = %s
                AND emp_is_active = %s
                ORDER BY person_last_name'''
                values = (False, True)  # AND emp_primary_home_unit_id IN %s

            columns = ['emp_id', 'emp_number', 'name', 'unit_name',
                       'emp_class', 'emp_status_name', 'designation_name']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["emp_id", "Emp Number", "Name", "Unit Name",
                          "Employee Class", "Status Name", "Designation Name"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'View', href=url+'?eid='+str(row["emp_id"])+'&mode='+mode)
            df = df[["Emp Number", "Name", "Unit Name",
                     "Employee Class", "Status Name", "Designation Name"]]
            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            if df.empty == True:
                table = "No entries found. Please check your search criteria."
            return [table]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
# @app.callback([
#                ],
#               [
#     Input('searchname_emp_unit', 'value'),
#     # Input('usersubmitstatus', 'value'),
# ],
#     [
# ],)
# def querylistofemployees(searchname_emp_unit):
#     return []
