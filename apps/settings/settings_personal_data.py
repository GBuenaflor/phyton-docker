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
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid
import hashlib
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
from datetime import datetime as dt
from dash_extensions import Keyboard
# columns=[{"name": "Transaction No.", "id": "trans_no"}, {"name": "Request Date", "id": "req_date"},
#                                  {"name": "Last Name", "id": "last_name"},{"name": "First Name", "id": "first_name"},
#                                  {"name": "Employee Type", "id": "emp_type"},{"name": "BP Type", "id": "bp_type"},
#                                  {"name": "Approval Decision", "id": "approval"}],
# data=[{"trans_no":"5", "req_date":"09/12/2020",
#                               "last_name":"Lagria", "first_name":"Freth",
#                               "emp_type":"Faculty", "bp_type":"Original",
#                               "approval":""},
#                               {"trans_no":"7", "req_date":"09/18/2020",
#                               "last_name":"Lorenzo", "first_name":"Anthony",
#                               "emp_type":"Faculty", "bp_type":"Promotion",
#                               "approval":""},
#                               {"trans_no":"10", "req_date":"09/18/2020",
#                               "last_name":"Tejada", "first_name":"Regine",
#                               "emp_type":"Administrative Personnel", "bp_type":"Original",
#                               "approval":""},
#                               ],
# datadf = pd.DataFrame(columns =columns, data=data )


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Personal Data"),
    html.Hr(),
    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Button("Create Personal Data Entry", color="primary", className="mr-1",  # style={"display": "none"},
                           id="add_pds", href="/settings/settings_personal_data_profile?mode=add"),
            ])
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H5(
                    """NOTE: Employee data is updated up to October 2021. Any new employee beyond October 2021 must have a personal data created.
                       Please DO NOT create NEW PERSONAL data if the employee is already connected to UP Diliman before October 2021.
                       If an existing employee under your unit does not exist in the dropdown options, PLEASE CONTACT HRDO.
                     """, style={'font-style': 'italic'})
            ])
        ]),
        html.Hr(),
        dbc.Card([
            Keyboard(id="keyboard"),
            dbc.CardHeader(
                html.H4("Filter Personal Data Entries"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([

                # dbc.Row([
                #     dbc.Col([
                #         dbc.FormGroup(
                #             [
                #                 dbc.Label("Filter by Last Name:", width=4,
                #                           style={"text-align": "left"}),
                #                 dbc.Col([
                #                     dbc.Input(
                #                         type="text", placeholder="Enter last name", id='pds_lastnamefilter'
                #                     ),
                #
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
                                dbc.Label("Select Unit", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        options=[

                                        ],
                                        id='pds_unitfilter',
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
                                dbc.Label("Select Employee Class", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        options=[

                                        ],
                                        id='pds_empclassfilter',
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
                                        type="text", id="pds_lastnamefilter", placeholder="Enter search name"
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
                                        type="text", id="pds_firstnamefilter", placeholder="Enter search name"
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
                                        type="text", id="pds_empnumfilter", placeholder="Enter search number"
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
                                        id="pds_empactivefilter",
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
                        dbc.Button("Search", color="primary",
                                   className="mr-1", id="search_pds"),
                    ])
                ]),
                html.Br(),
                html.H5("*You can only edit the data of persons with home unit under the scope of your assigned unit."),
                html.Hr(),
                html.Br(),
                html.H5("Existing Personal Data Entries"),
                html.Div([
                ], id="listofpds"),
                # html.Div([
                # ],id="listofbpsforapproval"),

                # html.Div([
                #     dbc.Button("Approve", color="primary", id="btnapprove",
                #                className="mr-1", style={"float": "right"}),
                #     html.Br(),
                # ]),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('listofpds', 'children')
               ],
              [

    Input('search_pds', 'n_clicks'),
    Input("keyboard", "keydown")
], [
    State('url', 'pathname'),
    State('sessioncurrentunit', 'data'),
    State('sessionlistofunits', 'data'),
    State('pds_unitfilter', 'value'),
    State('pds_empclassfilter', 'value'),
    State('pds_lastnamefilter', 'value'),
    State('pds_firstnamefilter', 'value'),
    State('pds_empnumfilter', 'value'),
    State('pds_empactivefilter', 'value'),

])
def query_persons(search_pds, keydown, url, sessioncurrentunit, sessionlistofunits,
                      pds_unitfilter, pds_empclassfilter, pds_lastnamefilter, pds_firstnamefilter, pds_empnumfilter, pds_empactivefilter):

    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'search_pds':

            sqlcommand = '''

                            SELECT p.person_id, p.person_last_name, p.person_first_name, p.person_middle_name
                            FROM persons p
                            LEFT JOIN employees e ON p.person_id = e.person_id
                            WHERE p.person_delete_ind = %s
                            AND (e.emp_primary_home_unit_id IN %s OR p.person_temp_unit_id IN %s)


                        '''
            values = [False, listofallowedunits, listofallowedunits]

            if pds_unitfilter:
                sqlcommand = sqlcommand + \
                    " AND (e.emp_primary_home_unit_id = %s OR p.person_temp_unit_id = %s)"
                values.append(pds_unitfilter)
                values.append(pds_unitfilter)

            if pds_empclassfilter:
                sqlcommand = sqlcommand + " AND e.emp_class_id = %s"
                values.append(pds_empclassfilter)

            if pds_lastnamefilter:
                sqlcommand = sqlcommand + " AND p.person_last_name ILIKE %s"
                values.append('%' + pds_lastnamefilter + '%')

            if pds_firstnamefilter:
                sqlcommand = sqlcommand + " AND p.person_first_name ILIKE %s"
                values.append('%' + pds_firstnamefilter + '%')

            if pds_empnumfilter:
                sqlcommand = sqlcommand + " AND e.emp_number ILIKE %s"
                values.append(pds_empnumfilter + '%')

            if 1 in pds_empactivefilter:
                sqlcommand = sqlcommand + " AND e.emp_is_active = %s"
                values.append(True)

            sqlcommand = sqlcommand + " ORDER BY p.person_last_name "

            columns = ['person_id', 'person_last_name', 'person_first_name', 'person_middle_name']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["Person ID", "Last Name", "First Name", "Middle Name"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_personal_data_profile?uid='+str(row["Person ID"])+'&mode=edit')
            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            df = df[["Last Name", "First Name", "Middle Name", "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [table]
        elif not keydown:
            raise PreventUpdate
        elif keydown['key'] == 'Enter':
            sqlcommand = '''

                            SELECT p.person_id, p.person_last_name, p.person_first_name, p.person_middle_name
                            FROM persons p
                            LEFT JOIN employees e ON p.person_id = e.person_id
                            WHERE p.person_delete_ind = %s
                            AND (e.emp_primary_home_unit_id IN %s OR p.person_temp_unit_id IN %s)


                        '''
            values = [False, listofallowedunits, listofallowedunits]

            if pds_unitfilter:
                sqlcommand = sqlcommand + \
                    " AND (e.emp_primary_home_unit_id = %s OR p.person_temp_unit_id = %s)"
                values.append(pds_unitfilter)
                values.append(pds_unitfilter)

            if pds_empclassfilter:
                sqlcommand = sqlcommand + " AND e.emp_class_id = %s"
                values.append(pds_empclassfilter)

            if pds_lastnamefilter:
                sqlcommand = sqlcommand + " AND p.person_last_name ILIKE %s"
                values.append('%' + pds_lastnamefilter + '%')

            if pds_firstnamefilter:
                sqlcommand = sqlcommand + " AND p.person_first_name ILIKE %s"
                values.append('%' + pds_firstnamefilter + '%')

            if pds_empnumfilter:
                sqlcommand = sqlcommand + " AND e.emp_number ILIKE %s"
                values.append(pds_empnumfilter + '%')

            if 1 in pds_empactivefilter:
                sqlcommand = sqlcommand + " AND e.emp_is_active = %s"
                values.append(True)

            sqlcommand = sqlcommand + " ORDER BY p.person_last_name "

            columns = ['person_id', 'person_last_name', 'person_first_name', 'person_middle_name']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["Person ID", "Last Name", "First Name", "Middle Name"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_personal_data_profile?uid='+str(row["Person ID"])+'&mode=edit')
            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            df = df[["Last Name", "First Name", "Middle Name", "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [table]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [
        #    Output('query_employee_class', 'options'),
        Output('pds_unitfilter', 'options'),
        Output('pds_empclassfilter', 'options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('sessioncurrentunit', 'data'),
        State('sessionlistofunits', 'data'),
    ],
)
def fillindds(pathname, sessioncurrentunit, sessionlistofunits):
    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    if pathname == "/settings/settings_personal_data":
        query_employee_class = commonmodules.queryfordropdown('''
            SELECT emp_class_name as label, emp_class_id as value
           FROM emp_classes
           WHERE emp_class_delete_ind = %s
           ORDER BY emp_class_id
        ''', (False, ))

        unitoptions = commonmodules.queryfordropdown('''
                    SELECT unit_name as label, unit_id as value
                    FROM units
                    WHERE unit_delete_ind = %s
                    AND unit_id in %s
                    ORDER BY unit_name

               ''', (False, listofallowedunits))

        # query_employee_class
        return [unitoptions, query_employee_class]
    else:
        raise PreventUpdate
