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


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Personal Data Viewing"),

    html.Div([

        # dbc.Row([
        #     dbc.Col([
        #         dbc.Button("Create Personal Data Entry", color="primary", className="mr-1",
        #                    id="add_pdsv", href="/settings/settings_personal_data_viewing_profile?mode=add"),
        #     ])
        # ]),
        html.Hr(),
        dbc.Card([
            dbc.CardHeader(
                html.H4("Filter Personal Data Entries"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([


                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Select Unit:", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        options=[

                                        ],
                                        id='pdsv_unitfilter',
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
                                dbc.Label("Select Employee Class:", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        options=[

                                        ],
                                        id='pdsv_empclassfilter',
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
                                dbc.Label("Search Last Name:", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="pdsv_lastnamefilter", placeholder="Enter search name"
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
                                dbc.Label("Search First Name:", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="pdsv_firstnamefilter", placeholder="Enter search name"
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
                                dbc.Label("Search Employee Number:", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="pdsv_empnumfilter", placeholder="Enter search number"
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
                                dbc.Label("Select Active Employees:", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Include Current Employees Only", "value": 1},

                                        ],
                                        value=[1],
                                        id="pdsv_empactivefilter",
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
                                   className="mr-1", id="search_pdsv"),
                    ])
                ]),
                html.Hr(),
                html.Br(),
                html.H5("Existing Personal Data Entries"),
                html.Div([
                ], id="listofpdsv"),
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

@app.callback([Output('listofpdsv', 'children')
               ],
              [

            Input('search_pdsv', 'n_clicks'),
], [
          State('url', 'pathname'),
          State('sessioncurrentunit', 'data'),
          State('sessionlistofunits', 'data'),
          State('pdsv_unitfilter', 'value'),
          State('pdsv_empclassfilter', 'value'),
          State('pdsv_lastnamefilter', 'value'),
          State('pdsv_firstnamefilter', 'value'),
          State('pdsv_empnumfilter', 'value'),
          State('pdsv_empactivefilter', 'value'),


])

def querygrsfordtcall(search_pdsv, url, sessioncurrentunit, sessionlistofunits,
                      pdsv_unitfilter, pdsv_empclassfilter, pdsv_lastnamefilter, pdsv_firstnamefilter, pdsv_empnumfilter, pdsv_empactivefilter):

    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'search_pdsv':
            print('printing sessionlistofunits', sessionlistofunits)
            print('printing sessioncurrentunits', sessioncurrentunit)
            print('printing search person')
            sqlcommand = '''

                             SELECT p.person_id, p.person_last_name, p.person_first_name, p.person_middle_name
                             FROM persons p
                             LEFT JOIN employees e ON p.person_id = e.person_id
                             WHERE p.person_delete_ind = %s
                             AND (e.emp_primary_home_unit_id IN %s OR p.person_temp_unit_id IN %s)


                         '''
            values = [False, listofallowedunits, listofallowedunits]
            print(listofallowedunits)
            if pdsv_unitfilter:
                sqlcommand = sqlcommand + " AND (e.emp_primary_home_unit_id = %s OR p.person_temp_unit_id = %s)"
                values.append(pdsv_unitfilter)
                values.append(pdsv_unitfilter)

            if pdsv_empclassfilter:
                sqlcommand = sqlcommand + " AND e.emp_class_id = %s"
                values.append(pdsv_empclassfilter)

            if pdsv_lastnamefilter:
                sqlcommand = sqlcommand + " AND p.person_last_name ILIKE %s"
                values.append('%' + pdsv_lastnamefilter + '%')

            if pdsv_firstnamefilter:
                sqlcommand = sqlcommand + " AND p.person_first_name ILIKE %s"
                values.append('%' + pdsv_firstnamefilter + '%')

            if pdsv_empnumfilter:
                sqlcommand = sqlcommand + " AND e.emp_number ILIKE %s"
                values.append(pdsv_empnumfilter + '%')

            # if pdsv_empactivefilter == 1:
            #     sqlcommand = sqlcommand + " AND e.emp_is_active = %s"
            #     values.append(True)

            sqlcommand = sqlcommand + " ORDER BY p.person_last_name "



            columns = ['person_id', 'person_last_name', 'person_first_name', 'person_middle_name']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["Person ID", "Last Name", "First Name", "Middle Name"]
            print(df)
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'View', href='/settings/settings_personal_data_viewing_profile?uid='+str(row["Person ID"])+'&mode=view')
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
        Output('pdsv_unitfilter', 'options'),
        Output('pdsv_empclassfilter','options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
    ],
)
def fillindds(pathname):

    if pathname == "/settings/settings_personal_data_viewing":
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
