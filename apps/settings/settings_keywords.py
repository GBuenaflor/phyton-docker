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
    html.H3('Keyword Classes'),
    commonmodules.get_settings_menu(),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Keyword Classes"),
                className='text-white bg-dark'
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Keyword", id="btnaddnewmainkeyword", color="primary",
                                   href='/settings/settings_keywords_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Main Keyword Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="smainkeyname", placeholder="Enter search string"
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
                html.H4("Existing Class Keywords"),

                html.Div([

                ], id="editmainkeyworddatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='mainkeywordsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='mainkeywordid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])

# #


@app.callback([Output('editmainkeyworddatatable', 'children')
               ],
              [
    Input('smainkeyname', 'value'),
    Input('mainkeywordsubmitstatus', 'value'),
],
    [
],)
def querydtcall(smainkeyname, mainkeywordsubmitstatus):
    if smainkeyname:
        sqlcommand = "SELECT keyword_class_id, keyword_class_name  FROM keyword_classes WHERE keyword_class_delete_ind = %s and keyword_class_name ILIKE %s ORDER By keyword_class_name"
        values = (False, smainkeyname)
    else:
        sqlcommand = "SELECT keyword_class_id, keyword_class_name  FROM keyword_classes WHERE keyword_class_delete_ind = %s ORDER By keyword_class_name"
        values = (False,)
    columns = ["keyword_class_id", "keyword_class_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Keyword Class ID", "Keyword Name"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")

    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_keywords_profile?keywordclass_id='+str(row["Keyword Class ID"])+'&mode=edit')
        #linkcolumn.append({index:html.A('Edit', href='/settings_users?uid='+str(row["User ID"]))})

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}

    data_dict.update(dictionarydata)

    #df['Edit'] = np.array(linkcolumn)
    df = pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
