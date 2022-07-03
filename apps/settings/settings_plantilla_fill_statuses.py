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
    html.H1("Plantilla Fill Statuses Master Data Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Plantilla Fill Statuses"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Fill Status", id="plantilla_fill_status_add_new_btn", color="primary",
                                   href='/settings/settings_plantilla_fill_statuses_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Plantilla Fill Status", width=3,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="plantilla_fill_status_search", placeholder="Enter search string"
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
                                       className="mr-1", id="plantilla_fill_status_show_all"),
                        ])
                    ]),


                ]),

                html.Hr(),
                html.H4("Existing Plantilla Fill Statuses"),

                html.Div([

                ], id="plantilla_fill_status_edit_status_dt"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='plantilla_fill_status_submit_status', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='plantilla_fill_status_id', type='text', value="0")
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
        Output('plantilla_fill_status_edit_status_dt', 'children')
    ],
    [
        Input('plantilla_fill_status_search', 'value'),
        Input('plantilla_fill_status_submit_status', 'value'),
        Input('plantilla_fill_status_show_all', 'n_clicks'),
    ],
    [
    ],
)
def querymodulesfordtcall(plantilla_fill_status_search, plantilla_fill_status_submit_status, plantilla_fill_status_show_all):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'plantilla_fill_status_show_all':
            sqlcommand = """
                        SELECT plantilla_fill_status_id, plantilla_fill_status_name, plantilla_fill_status_description
                          FROM plantilla_fill_statuses
                         WHERE plantilla_fill_status_delete_ind = %s
                        ORDER BY plantilla_fill_status_name ASC
                         LIMIT 200
                    """
            values = (False,)
        elif plantilla_fill_status_search:
            plantilla_fill_status_search = "%"+plantilla_fill_status_search+"%"
            sqlcommand = """
                            SELECT plantilla_fill_status_id, plantilla_fill_status_name, plantilla_fill_status_description
                              FROM plantilla_fill_statuses
                             WHERE plantilla_fill_status_delete_ind = %s
                               AND plantilla_fill_status_name ILIKE %s
                            ORDER BY plantilla_fill_status_name ASC
                        """
            values = (False, plantilla_fill_status_search)
        else:
            raise PreventUpdate
    else:
        sqlcommand = """
                    SELECT plantilla_fill_status_id, plantilla_fill_status_name, plantilla_fill_status_description
                      FROM plantilla_fill_statuses
                     WHERE plantilla_fill_status_delete_ind = %s
                    ORDER BY plantilla_fill_status_id ASC
                     LIMIT 200
                """
        values = (False,)
    columns = ["plantilla_fill_status_id", "plantilla_fill_status_name", "plantilla_fill_status_description"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Plantilla Fill Status ID", "Fill Status Name", "Description"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit/View', href='/settings/settings_plantilla_fill_statuses_profile?plantilla_fill_status_id='+str(row["Plantilla Fill Status ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Plantilla Fill Status ID", "Fill Status Name", "Description", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table, ]
