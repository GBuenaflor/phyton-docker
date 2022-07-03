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
    html.H1("Document Type Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Document Types"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Document Type", id="btnaddnewdocument", color="primary",
                                   href='/settings/settings_documents_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.Row([
                            dbc.FormGroup(
                            [
                                dbc.Label("Search Document Type", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sdocumentname", placeholder="Enter search string"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                        ]),

                        dbc.Row([

                            dbc.Checklist(
                                options=[
                                    {"label": "Show active documents only", "value": 1},

                                ],
                                value=[1],
                                id="sdocumentinactive",
                                switch=True,
                            ),
                        ])
                    ]),

                ]),
                html.Hr(),
                html.H4("Existing Documents"),

                html.Div([

                ], id="editdocumentdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='documentsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='documentid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editdocumentdatatable', 'children')
               ],
              [
    Input('sdocumentname', 'value'),
    Input('documentsubmitstatus', 'value'),
    Input('sdocumentinactive','value')
],
    [

],)
def query_documents_dt(sdocumentname, documentsubmitstatus, sdocumentinactive):
    if sdocumentname:
        sdocumentname = "%"+sdocumentname+"%"
        sqlcommand = '''SELECT doc_id, doc_name FROM documents
        WHERE doc_name ILIKE %s'''
        values = [sdocumentname]
    else:

        sqlcommand = "SELECT doc_id, doc_name FROM documents WHERE doc_id >= %s"
        values = [1]

    if 1 in sdocumentinactive:
        sqlcommand = sqlcommand + " and doc_delete_ind = %s"
        values.append(False)
    else:
        sqlcommand = sqlcommand + " and doc_delete_ind = %s"
        values.append(True)

    sqlcommand = sqlcommand + " ORDER By doc_name"
    columns = ["document id", "document_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    #print(sqlcommand)
    df.columns = ["Document ID", "Document Name"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_documents_profile?doc_id='+str(row["Document ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Document Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
