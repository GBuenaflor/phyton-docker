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

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Documentary Requirements"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Document Requirement", id="btnaddnewdocreq", color="primary",
                                   href='/settings/settings_doc_requirements_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Document Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sdocreqname", placeholder="Enter search string"
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
                html.H4("Existing Documents"),

                html.Div([

                ], id="editdocumentsdatatable"),

                dbc.Col([

                        # html.Div([
                        #     dcc.Input(id='rolesubmitstatus', type='text', value="0")
                        # ], style={'display':'none'}),
                        # html.Div([
                        #     dcc.Input(id='roleid', type='text', value="0")
                        # ], style={'display':'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editdocumentsdatatable', 'children')
               ],
              [
    Input('sdocreqname', 'value'),

],
    [
],)
def query_doc_requirement_dt(sdocreqname):
    if sdocreqname:
        sdocreqname = "%"+sdocreqname+"%"
        sqlcommand = """
                        SELECT doc_requirement_id, doc_requirement_name, doc_requirement_description
                          FROM document_requirements
                         WHERE doc_requirement_delete_ind = %s
                           AND doc_requirement_name ILIKE %s
                      ORDER BY doc_requirement_name
                     """
        values = (False, sdocreqname)
    else:
        sqlcommand = """
                    SELECT doc_requirement_id, doc_requirement_name, doc_requirement_description
                      FROM document_requirements
                     WHERE doc_requirement_delete_ind = False
                  ORDER BY doc_requirement_name
                    """
        values = (False,)
    columns = ["doc_requirement_id", "doc_requirement_name", "doc_requirement_description"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Document ID", "Doc Requirement Name", "Doc Description"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_doc_requirements_profile?document_id='+str(row["Document ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
