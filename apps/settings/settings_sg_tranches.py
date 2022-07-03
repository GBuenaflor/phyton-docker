
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from apps import commonmodules
import re
from dash.dependencies import Input, Output, State
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid, querydatafromdatabase, modifydatabase
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
                html.H4("Salary Grades"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        # dbc.FormGroup([
                        #     dbc.Label("Current Active Tranche:", style={"text-align":"left"}),
                        #     dbc.Col([
                        #         dbc.Label("1", width=4, style={"text-align":"left"})
                        #     ]),
                        # ],row=True),

                        # dbc.FormGroup([
                        #     dbc.Label("Set New Active Tranche:", style={"text-align":"left"}),
                        #     dbc.Col([
                        #         dcc.Dropdown(id="new_tranche_input",     options=[
                        #             {'label': '1', 'value': '1'},
                        #             {'label': '2', 'value': '2'},
                        #             {'label': '3', 'value': '3'},
                        #             {'label': '4', 'value': '4'}
                        #         ],)
                        #     ], width = 1),
                        # ],row=True),

                        dbc.FormGroup([
                            dbc.Label("Current Active Tranche:", width=2,
                                      style={"text-align": "left"}),
                            dbc.Col([

                                dbc.Label(width=2, style={
                                          "text-align": "left"}, id="active_tranche")
                            ], width=8)
                        ], row=True),
                        dbc.FormGroup([
                            dbc.Label("Set New Active Tranche:", width=2,
                                      style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(id="new_tranche_input",     options=[
                                    {'label': '1', 'value': '1'},
                                    {'label': '2', 'value': '2'},
                                    {'label': '3', 'value': '3'},
                                    {'label': '4', 'value': '4'}
                                ],)
                            ], width=1)
                        ], row=True),

                        dbc.Button("Set as Active", id="btnsetactivetranche",
                                   color="primary"),  # block=True
                    ]),
                ]),
                html.Hr(),
                html.H4("Active SG Tranche Amounts"),

                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label("Tranche:", width=2),

                            dbc.Col([
                                dbc.Label(id='tranche_text'),
                                dbc.FormFeedback(
                                    "Please enter last name", valid=False)
                            ], width=8)
                        ], row=True),
                    ]),
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label("Year of Effectivity:"),
                            dbc.Col([
                                dbc.Label(id='year_text'),

                            ], width=8)
                        ], row=True),
                    ]),
                ]),

                html.Div([

                ], id="editsgdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='sgsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='sgid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([
    Output('new_tranche_input', 'options'),
],
    [
    Input('url', 'pathname'),

],
)
def filldd(path):
    trancheoptions = commonmodules.queryfordropdown('''
        SELECT ssl_tranche_id as label, ssl_tranche_id as value
       FROM ssl_tranches
       WHERE ssl_tranche_delete_ind = %s
       ORDER BY ssl_tranche_id
    ''', (False, ))


# ORIGINAL START
@app.callback([Output('active_tranche', 'children'),
               Output('editsgdatatable', 'children'),
               Output('tranche_text', 'children'),
               Output('year_text', 'children'),
               ],
              [
    Input('btnsetactivetranche', 'n_clicks'),
],
    [State('new_tranche_input', 'value')]
)
def populatemonitoringtable(btnsetactivetranche, new_tranche_input):

    sqlcommand3 = "SELECT ssl_tranche_id FROM ssl_tranches WHERE ssl_tranche_is_active = true"
    df3 = querydatafromdatabase(sqlcommand3)
    current_active_tranche = df3.loc[0][0]

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'btnsetactivetranche':
            if current_active_tranche:
                sqlcommand = '''
                UPDATE ssl_tranches SET ssl_tranche_is_active = false WHERE ssl_tranche_id = %s
                '''
                values = (int(current_active_tranche),)
                modifydatabase(sqlcommand, values)

            if new_tranche_input:
                sqlcommand2 = '''
                UPDATE ssl_tranches SET ssl_tranche_is_active = true WHERE ssl_tranche_id = %s
                '''
                values2 = (int(new_tranche_input),)
                modifydatabase(sqlcommand2, values2)

    sqlcommand = '''
    SELECT sgs.sg_number_step, sg.salary_grade_amount
    FROM sg_number_steps sgs
	INNER JOIN salary_grades sg ON sgs.sg_number_step_id = sg.salary_grade_number_step_id
    INNER JOIN ssl_tranches tr ON sg.salary_grade_ssl_tranche_id = tr.ssl_tranche_id
    WHERE sg.salary_grade_delete_ind = false and tr.ssl_tranche_is_active = true
    ORDER By sgs.sg_number_step, sg.salary_grade_ssl_tranche_id
    '''
    values = (False,)
    columns = ["salary_grade", "salary_grade_amount"]

    df = securequerydatafromdatabase(sqlcommand, values, columns)

    df.columns = ["Salary Grade", "Amount"]

    columns = [{"name": i, "id": i} for i in df.columns]

    table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                     hover=True, style={"text-align": "left"})

    # active tranche
    sqlcommand2 = """
    SELECT ssl_tranche_id, ssl_tranche, ssl_tranche_year
    FROM ssl_tranches
    WHERE ssl_tranche_is_active = true
    """

    df2 = querydatafromdatabase(sqlcommand2)
    active_tranche = df2.iloc[0][0]
    tranche_text = df2.iloc[0][1]
    year_text = df2.iloc[0][2]

    return [active_tranche, table, tranche_text, year_text]
