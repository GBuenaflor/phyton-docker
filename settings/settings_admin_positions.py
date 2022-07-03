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
    html.H1("Administrative Positions Entry"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Administrative Positions"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Admin Position", id="btnaddnewadminposition", color="primary",
                                   href='/settings/settings_admin_positions_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Administrative Position", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sadminpositionname", placeholder="Enter search string"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),

                ]),
                html.Hr(),
                html.H4("Existing Administrative Positions"),

                html.Div([

                ], id="editadminpositiondatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='adminpositionsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='adminpositionid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editadminpositiondatatable', 'children')
               ],
              [
    Input('sadminpositionname', 'value'),
    Input('adminpositionsubmitstatus', 'value'),
],
    [
],)
def query_admin_positions_dt(sadminpositionname, adminpositionsubmitstatus):
    if sadminpositionname:
        sadminpositionname = "%"+sadminpositionname+"%"
        sqlcommand = """SELECT admin_pos_id, designation_name, unit_name, role_name
                          FROM admin_positions ap
                        INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                        INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                        INNER JOIN roles r ON r.role_id = ap.admin_role_Id
                         WHERE admin_pos_delete_ind = %s
                           AND admin_pos_description ILIKE %s
                        ORDER BY admin_pos_description
                     """
        values = (False, sadminpositionname)
    else:
        sqlcommand = """SELECT admin_pos_id, designation_name, unit_name, role_name
                          FROM admin_positions ap
                        INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                        INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                        INNER JOIN roles r ON r.role_id = ap.admin_role_Id
                         WHERE admin_pos_delete_ind = False
                        ORDER BY designation_name
                     """
        values = (False,)
    columns = ["admin_pos_id", "admin_pos_description", "unit_name", "role_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Admin Position ID", "Admin Position Name", "Unit", "Attached User Role"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_admin_positions_profile?admin_pos_id='+str(row["Admin Position ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
