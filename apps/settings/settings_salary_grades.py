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
    html.H1("Salary Grades Master Data Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Salary Grades"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New SG Tranche", id="btnaddnewsg", color="primary",
                                   href='/settings/settings_salary_grades_profile?&mode=add'),  # block=True
                    ]),
                ]),

                html.Hr(),
                html.H4("Existing SG Tranches"),

                html.Div([

                ], id="sgdt"),

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
        Output('sgdt', 'children')
    ],
    [
        Input('url', 'pathname'),

    ],
    [
    ],
)
def querymodulesfordtcall(url):


    sqlcommand = """
                SELECT sg_tranche_id, sg_tranche_name, sg_tranche_year, sg_tranche_effectivity_start_date, sg_tranche_effectivity_end_date
                FROM sg_tranches
                WHERE sg_tranche_delete_ind = %s
                ORDER BY sg_tranche_year DESC
            """
    values = (False,)


    columns = ["sg_tranche_id", "sg_tranche_name", "sg_tranche_year", "sg_tranche_effectivity_start_date", "sg_tranche_effectivity_end_date"]

    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["SG Tranche ID", "Name", "Year", "Start Date", "End Date"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_salary_grades_profile?sg_tranche_id='+str(row["SG Tranche ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Name", "Year", "Start Date", "End Date", "Select"]]
    # print("HERE3456", df)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table, ]
