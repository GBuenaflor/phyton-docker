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
    html.H1("Performance Rating"),
    html.Hr(),
    html.Div([
        dbc.Card([
            Keyboard(id="perfrating_keyboard"),
            dbc.CardHeader(
                html.H4("Performance Rating Filters"),
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
                                        id='perfrating_query_faculty_unit',
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
                # dbc.Row([
                #     dbc.Col([
                #         dbc.FormGroup(
                #             [
                #                 dbc.Label("Select Employee Class:", width=4,
                #                           style={"text-align": "left"}),
                #                 dbc.Col([
                #                     dcc.Dropdown(
                #                         options=[
                #                             {'label': 'Faculty', 'value': '1'},
                #                             {'label': 'Admin Staff', 'value': '2'},
                #                             {'label': 'REPS', 'value': '3'}
                #                         ],
                #                         searchable=True, clearable=True,
                #                         id="query_employee_class"
                #                     ),
                #                 ],
                #                     width=8
                #                 )
                #             ],
                #             row=True
                #         ),
                #     ]),
                # ]),

                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Last Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="perfrating_searchname", placeholder="Enter search name"
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
                                        type="text", id="perfrating_searchfname", placeholder="Enter search name"
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
                                        type="text", id="perfrating_searchnumber", placeholder="Enter search number"
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
                                        id="perfrating_query_employee_status",
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
                            dbc.Button("Search", id="perfrating_btn_search_employees",
                                       color="primary", block=True),
                        ]),
                        dbc.Col([]
                        ),
                        ]),
                html.Hr(),
                html.H5("Employee List"),
                html.Div([

                ], id="perfrating_queryfacultydiv"),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        #    Output('query_employee_class', 'options'),
        Output('perfrating_query_faculty_unit', 'options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
    ],
)
def fillindropdowns(pathname):

    if pathname == "/settings/settings_perfrating_query":
        # query_employee_class = commonmodules.queryfordropdown('''
        #     SELECT emp_class_name as label, emp_class_id as value
        #    FROM emp_classes
        #    WHERE emp_class_delete_ind = %s
        #    ORDER BY emp_class_id
        # ''', (False, ))

        # query_employee_class
        return [commonmodules.queryunits()]
    else:
        raise PreventUpdate


@app.callback(
[
    Output('perfrating_queryfacultydiv', 'children')
],
[
    Input('perfrating_btn_search_employees', 'n_clicks'),
    Input("perfrating_keyboard", "keydown")
],
    [
    State('perfrating_searchname', 'value'),
    State('perfrating_query_employee_status', 'value'),
    #State('query_employee_class', 'value'),
    State('sessioncurrentunit', 'data'),
    State('sessionlistofunits', 'data'),
    State('current_user_id', 'data'),
    State('perfrating_searchnumber', 'value'),
    State('perfrating_query_faculty_unit', 'value'),
    State('perfrating_searchfname', 'value')
],)
def querylistofemployees(perfrating_btn_search_employees, keydown, searchname, query_employee_status,  sessioncurrentunit, sessionlistofunits,  # query_employee_class
                         current_user_id, searchnumber, query_faculty_unit, searchfname):

    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'perfrating_btn_search_employees':
            if any([searchname, searchnumber, query_faculty_unit, searchfname]):  # query_employee_class

                sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                INNER JOIN employees e ON e.person_id = p.person_id
                INNER JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
                INNER JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
                WHERE emp_delete_ind = %s
                AND (ec.emp_class_id = %s OR ec.emp_class_id = %s)
                '''
                values = [False, 2, 3]  # AND emp_primary_home_unit_id IN %s

                if 1 in query_employee_status:
                    sqlcommand = sqlcommand + " AND e.emp_is_active = %s "
                    values.append(True)

                # if query_employee_class:
                #     sqlcommand = sqlcommand + " AND e.emp_class_id = %s "
                #     values.append(query_employee_class)

                if searchname:
                    sqlcommand = sqlcommand + " AND person_last_name ILIKE %s "  # + \
                    values.append('%'+searchname+'%')

                if searchfname:
                    sqlcommand = sqlcommand + " AND person_first_name ILIKE %s "  # + \
                    values.append('%'+searchfname+'%')

                if searchnumber:
                    sqlcommand = sqlcommand + " AND emp_number ILIKE %s "  # + \
                    values.append('%'+searchnumber+'%')

                if query_faculty_unit:
                    sqlcommand = sqlcommand + " AND unit_id = %s "  # + \
                    values.append(query_faculty_unit)

                sqlcommand = sqlcommand + " ORDER BY person_last_name"
            else:
                raise PreventUpdate
                sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                INNER JOIN employees e ON e.person_id = p.person_id
                INNER JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                INNER JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                INNER JOIN designations d ON e.emp_primary_designation_id= d.designation_id
                INNER JOIN emp_classes ec ON ec.emp_class_id = d.designation_emp_class_id
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
                    'View', href='/settings/settings_perfrating_query_profile?eid='+str(row["emp_id"])+'&mode=view')
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

            if any([searchname, searchnumber, query_faculty_unit, searchfname]):  # query_employee_class

                sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                INNER JOIN employees e ON e.person_id = p.person_id
                INNER JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
                INNER JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
                WHERE emp_delete_ind = %s
                '''
                values = [False]  # AND emp_primary_home_unit_id IN %s

                if 1 in query_employee_status:
                    sqlcommand = sqlcommand + " AND e.emp_is_active = %s "
                    values.append(True)
                if searchfname:
                    sqlcommand = sqlcommand + " AND person_first_name ILIKE %s "  # + \
                    values.append('%'+searchfname+'%')
                # if query_employee_class:
                #     sqlcommand = sqlcommand + " AND e.emp_class_id = %s "
                #     values.append(query_employee_class)

                if searchname:
                    sqlcommand = sqlcommand + " AND person_last_name ILIKE %s "  # + \
                    values.append('%'+searchname+'%')

                if searchnumber:
                    sqlcommand = sqlcommand + " AND emp_number ILIKE %s "  # + \
                    values.append('%'+searchnumber+'%')

                if query_faculty_unit:
                    sqlcommand = sqlcommand + " AND unit_id = %s "  # + \
                    values.append(query_faculty_unit)

                sqlcommand = sqlcommand + " ORDER BY person_last_name"
            else:
                raise PreventUpdate
                sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
                    emp_status_name, designation_name
                FROM persons p
                INNER JOIN employees e ON e.person_id = p.person_id
                INNER JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
                INNER JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
                INNER JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
                INNER JOIN designations d ON e.emp_primary_designation_id= d.designation_id
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
                    'View', href='/settings/settings_perfrating_query_profile?eid='+str(row["emp_id"])+'&mode=view')
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
