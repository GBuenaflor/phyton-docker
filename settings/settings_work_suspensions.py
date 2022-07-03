import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from apps import commonmodules
import dash_bootstrap_components as dbc
from app import app
from dash.exceptions import PreventUpdate
import re
from dash.dependencies import Input, Output, State
from apps import commonmodules
import dash
from apps.dbconnect import securequerydatafromdatabase
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import date
from datetime import datetime
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid,bulkmodifydatabase
import pandas as pd
import json
layout = html.Div([
    dbc.Spinner([
        commonmodules.get_header(),
        commonmodules.get_menu(),
        commonmodules.get_common_variables(),
        html.H1("Work Suspensions"),
        dcc.Link('← Home', href='/home'),
        html.Div([
            dbc.Card([

                dbc.CardHeader(
                    html.H4("Select Year"),
                    style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                ),
                dcc.ConfirmDialog(
                    id='suspension_usermessage',
                ),
                dbc.Modal([
                    dbc.ModalHeader("Process work suspensions / holidays", id = "suspension_results_head"),
                    dbc.ModalBody([
                    ], id = "suspension_results_body"),
                    dbc.ModalFooter([
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Close", id="btn_suspension_head_close", color="primary", block=True),
                            ], id="suspension_results_head_close", style={'display':'none'} ),
                            dbc.Col([
                                dbc.Button("Return", id="btn_suspension_results_head_return", color="primary", block=True, href ='/settings/settings_work_suspensions'),
                            ], id="suspension_results_head_return", style={'display':'none'} ),
                        ], style={'width':'100%'}),
                    ]),
                ], id="suspension_results_modal"),
                dbc.CardBody([
                    # dbc.Row([
                    #     dbc.Col([
                    #         html.H5("Search BP to view.")
                    #     ])
                    # ]),
                    # html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Select Year:", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options=[
                                            {'value':i,'label':i} for i in range(1980,2051)
                                            ],  # value=1,
                                            searchable=True, id='work_suspension_year', clearable=False
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
                    dbc.Row([

                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Work Suspension Type:", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options=[

                                            ],
                                            searchable=True, id='work_suspension_type'
                                        ),
                                    ],
                                        width=8
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Work Suspension Date:", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.DatePickerSingle(
                                            id='work_suspension_date',
                                        ),
                                    ],
                                        width=8
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Work Start Time:", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options=[{'label':'%s:%s %s' % (h, m, ap), 'value':'%s:%s %s' % (h, m, ap)} for ap in ('AM', 'PM') for h in ([12] + list(range(1,12))) for m in ('00','15', '30','45')],
                                            searchable=True, id='work_start_time'
                                        ),
                                    ],
                                        width=8
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),

                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Work End Time:", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options=[{'label':'%s:%s %s' % (h, m, ap),
                                                      'value':'%s:%s %s' % (h, m, ap)} for ap in ('AM', 'PM') for h in ([12] + list(range(1,12))) for m in ('00','15', '30','45')],
                                            searchable=True, id='work_end_time'
                                        ),
                                    ],
                                        width=8
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Work Suspension Name:", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(id='work_suspension_name', type='text')
                                    ],
                                        width=8
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Add Work Suspension", color="primary",
                                       className="mr-1", id="add_work_suspension"),
                        ])
                    ]),
                    html.Br(),
                    html.Hr(),
                    html.Div([
                    ], id="list_year_work_suspension"),
                    # html.Div([
                    # ],id="bpmaint_listofbpsforapproval"),

                    # html.Div([
                    #     dbc.Button("Approve", color="primary", id="btnapprove",
                    #                className="mr-1", style={"float": "right"}),
                    #     html.Br(),
                    # ]),

                ], style={'line-height': "1em", "display": "block"}),
            ], style={'line-height': "1em", "display": "block"}
            )
        ]),
    ],color="danger")

])

@app.callback([
    Output('work_suspension_year', 'value'),
    Output('work_suspension_type','options')
],
    [
    Input('url', 'pathname'),
]
)
def work_suspension_year(url):
    if url=="/settings/settings_work_suspensions":
        todays_date = date.today()
        work_suspension_types = commonmodules.queryfordropdown('''
            SELECT work_suspension_type_name as label, work_suspension_type_id as value
           FROM work_suspension_types
           WHERE work_suspension_type_delete_ind = %s
           ORDER BY work_suspension_type_id
        ''', (False, ))
        return [todays_date.year,work_suspension_types]
    else:
        raise PreventUpdate


@app.callback([
    Output('list_year_work_suspension','children'),
    Output('suspension_results_modal',"is_open"),
    Output('suspension_results_body',"children"),
    Output('suspension_results_head_close',"style"),
    Output('suspension_results_head_return',"style"),
],
    [
    Input('work_suspension_year', 'value'),
    Input('add_work_suspension', 'n_clicks'),
    Input({'type': 'dynamic_work_sus_delete', 'index': ALL}, 'n_clicks'),
    Input('btn_suspension_head_close', 'n_clicks'),
    Input('btn_suspension_results_head_return', 'n_clicks'),
],[
    State('work_suspension_type','value'),
    State('work_suspension_date','date'),
    State('work_start_time','value'),
    State('work_end_time','value'),
    State('work_suspension_name','value'),
    State('current_user_id','data'),
    State({'type': 'dynamic_work_sus_delete', 'index': ALL}, 'children')
]
)
def list_year_work_suspension(work_suspension_year,add_work_suspension,dynamic_work_sus_delete,
    btn_suspension_head_close, btn_suspension_results_head_return, work_suspension_type,
    work_suspension_date,work_start_time,work_end_time,work_suspension_name,current_user_id,dynamic_work_sus_delete_children):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'work_suspension_year':
            table = queryworksuspensions(work_suspension_year)
            return [table, False, "", {'display':'none'}, {'display':'none'}]
        elif eventid =='add_work_suspension':
            values = [work_suspension_type,work_suspension_date,work_start_time,work_end_time,work_suspension_name,current_user_id,False]
            insertintoworksuspensions(values)
            table = queryworksuspensions(work_suspension_year)
            return [table, True, "Successfully added new work suspension/holiday", {'display':'inline'}, {'display':'none'}]
        elif eventid =='btn_suspension_head_close':
            table = queryworksuspensions(work_suspension_year)
            return [table, False, "", {'display':'inline'}, {'display':'none'}]
        else:
            index = json.loads(eventid)["index"]

            sqlwork_suspensions = """
                 UPDATE work_suspensions SET
                     work_suspension_delete_ind=%s
                    WHERE work_suspension_day_id = %s

            """
            modifydatabase(sqlwork_suspensions, [True,index])
            table = queryworksuspensions(work_suspension_year)
            return [table, False, "", {'display':'inline'}, {'display':'none'}]
    else:
        raise PreventUpdate


def insertintoworksuspensions(values):
    sqlwork_suspensions = """
        INSERT INTO work_suspensions(work_suspension_type_id, work_suspension_day,
            work_suspension_start_hour, work_suspension_end_hour,  work_suspension_name,work_suspension_inserted_by, work_suspension_delete_ind)
        VALUES (%s, %s, %s, %s, %s, %s, %s)

    """
    modifydatabase(sqlwork_suspensions, values)
    pass

def queryworksuspensions(work_suspension_year):
    sqlcommand = '''SELECT work_suspension_day_id, work_suspension_type_name, work_suspension_day, work_suspension_name, work_suspension_start_hour, work_suspension_end_hour
        FROM work_suspensions ws INNER JOIN work_suspension_types wst ON ws.work_suspension_type_id = wst.work_suspension_type_id
        WHERE date_part('year', work_suspension_day)=%s and work_suspension_delete_ind = %s ORDER BY work_suspension_day DESC'''
    values = (work_suspension_year, False)
    columns = ['work_suspension_id', 'Suspension Type', 'Date', 'Name', 'Start Hour', 'End Hour']
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    data_dict = df.to_dict()
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dbc.Button("Delete", id={'index': str(
            row["work_suspension_id"]), 'type': 'dynamic_work_sus_delete'}, color="primary", className="mr-1", block=True)
    dictionarydata = {'Options': linkcolumn}
    data_dict.update(dictionarydata)

    df = pd.DataFrame.from_dict(data_dict)
    df2 = df[['Suspension Type', 'Date', 'Name', 'Start Hour', 'End Hour','Options']].copy()
    table = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True)
    return table
