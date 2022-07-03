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
    html.H1("Schools Master Data Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Schools"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New School", id="btnaddnewschool", color="primary",
                                   href='/settings/settings_schools_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search School", width=3,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="search_school_input", placeholder="Enter search string"
                                    ),

                                ],
                                    width=9
                                ),

                            ],
                            row=True
                        ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Show All", color="primary",
                                       className="mr-1", id="schools_show_all"),
                        ])
                    ]),


                ]),

                html.Hr(),
                html.H4("Existing Schools"),

                html.Div([

                ], id="edit_school_dt"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='schoolsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='schoolid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('edit_school_dt', 'children')
    ],
    [
        Input('search_school_input', 'value'),
        Input('schoolsubmitstatus', 'value'),
        Input('schools_show_all', 'n_clicks'),
    ],
    [
    ],
)
def querymodulesfordtcall(search_school_input, schoolsubmitstatus, schools_show_all):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'schools_show_all':
            sqlcommand = """
                        SELECT school_id, school_name, school_contact_person, school_contact_number, school_contact_email
                          FROM schools
                         WHERE school_delete_ind = %s
                         ORDER BY school_name
                         LIMIT 200
                    """
            values = (False,)
        elif search_school_input:
            search_school_input = "%"+search_school_input+"%"
            sqlcommand = """
                            SELECT school_id, school_name, school_contact_person, school_contact_number, school_contact_email
                              FROM schools
                             WHERE school_delete_ind = %s
                               AND school_name ILIKE %s
                             ORDER BY school_name
                             LIMIT 200
                        """
            values = (False, search_school_input)
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    columns = ["school_id", "school_name", "school_contact_person",
               "school_contact_number", "school_contact_email"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["School ID", "School Name", "Contact Person", "Contact Number", "E-mail"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit/View', href='/settings/settings_schools_profile?school_id='+str(row["School ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["School Name", "Contact Person", "Contact Number", "E-mail", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table, ]
