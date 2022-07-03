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
    # dcc.Store(id='sessionindiv', storage_type='memory', data=[]),
    # dcc.Store(id='sessionindiv_processed', storage_type='memory', data=[]),
    html.H1("Employee Management"),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dbc.Button("Create New Employee Entry", color="primary", className="mr-1",
                       id="otherbp_basic_paper", href="/settings/settings_employee_management_profile?mode=add"),
        ])
    ]),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Filters"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Filter by Last Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="empman_name_filter", placeholder="Enter search name"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Filter by Employee Number", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="empman_num_filter", placeholder="Enter Employee Number"
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
                            dbc.Button("Search", id="empman_search_button",
                                       className="mr-1", color="primary"),
                        ]),
                        ]),
                html.Hr(),
                html.H5("Employee Profiles"),
                html.Br(),
                html.Div([
                ], id="emp_man_listdiv"),


            ], style={'line-height': "1em", "display": "block"}),  # end of cardbody
        ], style={'line-height': "1em", "display": "block"}  # end of card
        )
    ]),  # end of submain div
])  # end of main div


@app.callback([ Output('emp_man_listdiv','children')
                ],
                [
                Input('url','pathname'),
                Input('empman_search_button', 'n_clicks')
                ],[

                  State('sessioncurrentunit','data'),
                  State('sessionlistofunits','data'),
                  State('empman_name_filter','value'),
                  State('empman_num_filter','value'),
                ])


def querygrsfordtcall(url,empman_search_button,sessioncurrentunit,sessionlistofunits, empman_name_filter, empman_num_filter):
    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    ctx = dash.callback_context

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'empman_search_button':

            if any([empman_name_filter, empman_num_filter]):

                sql = '''
                       SELECT e.emp_id, p.person_last_name, p.person_first_name, e.emp_number, ec.emp_class_name, u.unit_code, d.designation_name
                   FROM employees e
                   LEFT JOIN persons p ON p.person_id = e.person_id
                   LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
				  LEFT JOIN emp_units eu ON eu.emp_id = e.emp_id
                   LEFT JOIN units u ON u.unit_id = eu.unit_id
                   LEFT JOIN designations d ON d.designation_id = e.emp_primary_designation_id
                   WHERE eu.emp_unit_is_primary_home_unit = %s
                   AND eu.unit_id IN %s
               '''
                values = [True, listofallowedunits]

                if empman_name_filter:
                    sql = sql + " AND p.person_last_name ILIKE %s"
                    values.append('%'+empman_name_filter+'%')

                if empman_num_filter:
                    sql = sql + " AND e.emp_number ILIKE %s"
                    values.append('%'+empman_num_filter+'%')

                sql = sql + "ORDER BY p.person_last_name"
            else:

                sql = '''
                       SELECT e.emp_id, p.person_last_name, p.person_first_name, e.emp_number, ec.emp_class_name, u.unit_code, d.designation_name
                   FROM employees e
                   LEFT JOIN persons p ON p.person_id = e.person_id
                   LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
				  LEFT JOIN emp_units eu ON eu.emp_id = e.emp_id
                   LEFT JOIN units u ON u.unit_id = eu.unit_id
                   LEFT JOIN designations d ON d.designation_id = e.emp_primary_designation_id
                   WHERE eu.emp_unit_is_primary_home_unit = %s
                   AND eu.unit_id IN %s
                '''
                values = (listofallowedunits,)

            columns = ['Employee ID', 'Last Name', 'First Name', 'Emp Number', 'Class', "Unit", 'Primary Designation']

            print('HERE458', sql, values)
            df = securequerydatafromdatabase(sql, values, columns)

            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index]=dcc.Link('Edit', href='/settings/settings_employee_management_profile?emp_id='+str(row["Employee ID"])+'&mode=edit')
            data_dict = df.to_dict()
            dictionarydata = {'Select':linkcolumn}
            data_dict.update(dictionarydata)
            df =pd.DataFrame.from_dict(data_dict)
            df = df[['Last Name', 'First Name', 'Emp Number', 'Class', "Unit", 'Primary Designation', "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [table]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
