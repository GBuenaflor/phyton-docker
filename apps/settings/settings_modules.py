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
    # commonmodules.get_settings_menu(),
    html.H1("Modules Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Modules"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Module", id="btnaddnewmodule", color="primary",
                                   href='/settings/settings_modules_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Module Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="smodulename", placeholder="Enter search string"
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
                html.H4("Existing Modules"),

                html.Div([

                ], id="editmodulesdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='modulesubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='moduleid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editmodulesdatatable', 'children')
               ],
              [
    Input('smodulename', 'value'),
    Input('modulesubmitstatus', 'value'),
],
    [
],)
def querymodulesfordtcall(smodulename, banksubmitstatus):
    if smodulename:
        smodulename = "%"+smodulename+"%"
        sqlcommand = '''SELECT module_id,
                               module_name,
                               module_link,
                               module_header,
                               module_icon
                          FROM modules WHERE module_delete_ind = %s
                           AND module_name ILIKE %s
                        ORDER By module_header, module_name
                       '''
        values = (False, smodulename)
    else:
        sqlcommand = """SELECT module_id, module_name, module_link, module_header, module_icon
                        FROM modules
                       WHERE module_delete_ind = %s
                      ORDER BY module_header, module_name"""
        values = (False,)
    columns = ["module_id", "module_name", "module_link", "module_header", "module_icon"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Module ID", "Module Name", "Module Link", "Header", "Icon"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_modules_profile?module_id='+str(row["Module ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Module Name", "Module Link", "Header", "Icon", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
