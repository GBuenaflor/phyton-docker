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


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Designations Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Designations"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Designation", id="btnaddnewdesignation", color="primary",
                                   href='/settings/settings_designations_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        # dbc.Row([
                            dbc.FormGroup(
                            [
                                dbc.Label("Search Designation", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sdesignationname", placeholder="Enter search string"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    # ]),
                ]),
                ]),
                dbc.Row([
                    dbc.Col([

                    ]),
                    dbc.Col([
                        dbc.Checklist(
                            options=[
                                {"label": "Show inactive options", "value": 1},
                            ],
                            value=[],
                            id="sdesignationinactive",
                            switch=True,
                        ),
                    ])
                ]),
                html.Hr(),
                html.H4("Existing designations"),

                html.Div([

                ], id="editdesignationdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='designationsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='designationid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editdesignationdatatable', 'children')
               ],
              [
    Input('sdesignationname', 'value'),
    Input('designationsubmitstatus', 'value'),
    Input('sdesignationinactive','value')
],
    [

],)
def query_designations_dt(sdesignationname, designationsubmitstatus, sdesignationinactive):
    if sdesignationname:
        sdesignationname = "%"+sdesignationname+"%"
        sqlcommand = '''SELECT designation_id, designation_name, emp_class_name, designation_current_ind FROM designations d
        LEFT JOIN emp_classes ec ON ec.emp_class_id = d.designation_emp_class_id
        WHERE designation_delete_ind = %s and designation_name ILIKE %s'''
        values = [False, sdesignationname]
    else:
        raise PreventUpdate
        #sqlcommand = "SELECT designation_id, designation_name FROM designations WHERE designation_delete_ind = %s and designation_current_ind = %s ORDER By designation_name"
        #values = (False, True, )

    if 1 not in sdesignationinactive:
        sqlcommand = sqlcommand + " and designation_current_ind = %s"
        values.append(True)

    sqlcommand = sqlcommand + " ORDER By designation_name"
    columns = ["designation_id", "designation_name", "emp_class_name", "designation_current_ind"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Designation ID", "Designation Name", "Employee Class", "Is Current"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_designations_profile?designation_id='+str(row["Designation ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Designation Name","Employee Class", "Is Current", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
