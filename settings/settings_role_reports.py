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
    html.H1("Report-Roles Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Report-Roles"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    # dbc.Col([
                    #     dbc.Button("Add New School", id="rolereports_", color="primary",
                    #                href='/settings/settings_schools_profile?&mode=add'),  # block=True
                    # ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Role", width=3,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="rolereports_rolefilter", placeholder="Enter search string"
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
                            dbc.Button("Show All Roles", color="primary",
                                       className="mr-1", id="rolereports_showall"),
                        ])
                    ]),


                ]),

                html.Hr(),
                html.H4("Roles"),

                html.Div([

                ], id="rolereports_rolesdt"),

                # dbc.Col([
                #
                #         html.Div([
                #             dcc.Input(id='schoolsubmitstatus', type='text', value="0")
                #         ], style={'display': 'none'}),
                #         html.Div([
                #             dcc.Input(id='schoolid', type='text', value="0")
                #         ], style={'display': 'none'}),
                #
                #         ], width=2
                #         )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('rolereports_rolesdt', 'children')
    ],
    [
        Input('rolereports_rolefilter', 'value'),
        # Input('schoolsubmitstatus', 'value'),
        Input('rolereports_showall', 'n_clicks'),
    ],
    [
    ],
)
def querymodulesfordtcall(rolereports_rolefilter, rolereports_showall):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'rolereports_showall':
            sqlcommand = """
                        SELECT role_id, role_name
                          FROM roles
                         WHERE role_delete_ind = %s
                         ORDER BY role_name
                    """
            values = (False,)

        elif rolereports_rolefilter:
            rolereports_rolefilter = "%"+rolereports_rolefilter+"%"
            sqlcommand = """
                        SELECT role_id, role_name
                          FROM roles
                         WHERE role_delete_ind = %s
                               AND role_name ILIKE %s
                             ORDER BY role_name
                        """
            values = (False, rolereports_rolefilter)
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    columns = ["role_id", "role_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Role ID", "Role"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Add Reports to Role', href='/settings/settings_role_reports_profile?role_id='+str(row["Role ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Role", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table, ]
