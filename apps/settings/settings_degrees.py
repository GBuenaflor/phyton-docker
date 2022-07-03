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
    html.H1("Course Degrees and Degree Programs Master Data Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Course Degrees and Degree Programs"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Degree", id="btnaddnewdegree", color="primary", href='/settings/settings_degrees_profile?&mode=add'),# block=True


                    ]),
                    dbc.Col([
                        dbc.Button("Add New Degree Program", id="btnaddnewdegprog", color="primary", href='/settings/settings_degreeprograms_profile?&mode=add'),# block=True
                    ]),
                    # dbc.Col([
                    #     dbc.FormGroup(
                    #         [
                    #             dbc.Label("Search Degree Name", width=4, style={"text-align":"left"}),
                    #             dbc.Col([
                    #                 dbc.Input(
                    #                     type="text", id="sdegreename", placeholder="Enter search string"
                    #                 ),
                    #
                    #             ],
                    #             width=8
                    #             )
                    #         ],
                    #         row=True
                    #     ),
                    # ]),

                ]),
                html.Hr(),
                html.H4("Click to view Existing Degrees", id="degreetoggle", style = {'cursor':'pointer', 'text-decoration':'underline'}),

                dbc.Collapse([
                    dbc.Row(dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Degree Name", width=4, style={"text-align":"left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sdegreename", placeholder="Enter search string",
                                    ),

                                ],
                                width=8
                                )
                            ],
                            row=True
                        ),
                        ]),
                    ),
                    html.Div([

                    ],id="editdegreesdatatable")
                ], id="degreecollapse"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='degreesubmitstatus', type='text', value="0")
                        ], style={'display':'none'}),
                        html.Div([
                            dcc.Input(id='degreeid', type='text', value="0")
                        ], style={'display':'none'}),

                    ], width=2
                ),

                html.Hr(),
                html.H4("Click to view Existing Degree Programs", id="degprogtoggle", style = {'cursor':'pointer', 'text-decoration':'underline'}),


                dbc.Collapse([
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Search Degree Program Name", width=4, style={"text-align":"left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="sdegprogname", placeholder="Enter search string"
                                        ),

                                    ],
                                    width=8
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),
                    html.Div([

                    ],id="editdegprogdatatable")
                ], id="degprogcollapse"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='degprogsubmitstatus', type='text', value="0")
                        ], style={'display':'none'}),
                        html.Div([
                            dcc.Input(id='degprogid', type='text', value="0")
                        ], style={'display':'none'}),

                    ], width=2
                ),
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback([ Output('degreecollapse', 'is_open'),
                Output('editdegreesdatatable','children')
                ],
                [
                Input('degreetoggle', 'n_clicks'),
                Input('sdegreename','value'),
                Input('degreesubmitstatus', 'value'),
                ],
              [State('degreecollapse', 'is_open'),

              ],)
def querymodulesfordtcall(n1, sdegreename,degreesubmitstatus, is_open1):
    ctx = dash.callback_context
    if not ctx.triggered:
        #print('none')
        return [False, []]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]


    if button_id == 'degreetoggle' and n1:
        is_open1 = not is_open1
        if is_open1==False:
            #print('closed')
            sdegreename == ""
            return [False, []]
        else:
            sdegreename == ""
            sqlcommand = "SELECT degree_id, degree_name FROM degrees WHERE degree_delete_ind = False ORDER By degree_name"
            values = (False,)
            #print(sqlcommand)

        columns = ["degree_id", "degree_name"]
        df = securequerydatafromdatabase(sqlcommand, values,columns)
        df.columns=["Degree ID","Degree Name"]
        columns = [{"name":i, "id":i} for i in df.columns]
        data = df.to_dict("rows")
        linkcolumn = {}
        for index, row in df.iterrows():
            linkcolumn[index]=dcc.Link('Edit', href='/settings/settings_degrees_profile?degree_id='+str(row["Degree ID"])+'&mode=edit')

        data_dict = df.to_dict()
        dictionarydata = {'Select':linkcolumn}
        data_dict.update(dictionarydata)
        df =pd.DataFrame.from_dict(data_dict)
        df = df[["Degree Name", "Select"]]
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        return [is_open1, table]

    if sdegreename:
        sqlcommand = "SELECT degree_id, degree_name FROM degrees WHERE degree_delete_ind = %s and degree_name ILIKE %s ORDER By degree_name"
        values = (False, "%"+sdegreename+"%")
        #print(sqlcommand)

    else:
        sqlcommand = "SELECT degree_id, degree_name FROM degrees WHERE degree_delete_ind = False ORDER By degree_name"
        values = (False,)
        #print(sqlcommand)


    columns = ["degree_id", "degree_name"]
    df = securequerydatafromdatabase(sqlcommand, values,columns)
    df.columns=["Degree ID","Degree Name"]
    columns = [{"name":i, "id":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index]=dcc.Link('Edit', href='/settings/settings_degrees_profile?degree_id='+str(row["Degree ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    df = df[["Degree Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

    return [is_open1, table]

@app.callback([ Output('degprogcollapse', 'is_open'),
                Output('editdegprogdatatable','children')
                ],
                [
                Input('degprogtoggle', 'n_clicks'),
                Input('sdegprogname','value'),
                Input('degprogsubmitstatus', 'value'),
                ],
              [State('degprogcollapse', 'is_open')
              ],)

def querymodulesfordtcall(n1, sdegprogname,degprogsubmitstatus, is_open1):
    ctx = dash.callback_context
    if not ctx.triggered:

        return [False, []]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]


    if button_id == 'degprogtoggle' and n1:
        is_open1 = not is_open1
        if is_open1==False:

            return [False, []]
        else:
            sqlcommand = "SELECT program_id, program_name FROM programs WHERE program_delete_ind = %s ORDER By program_name"
            values = (False,)


        columns = ['program_id', 'program_name']
        df = securequerydatafromdatabase(sqlcommand, values,columns)
        df.columns=["Program ID", "Program Name"]
        columns = [{"degprogname":i, "degprogid":i} for i in df.columns]
        data = df.to_dict("rows")
        linkcolumn2 = {}
        for index, row in df.iterrows():
            linkcolumn2[index]=dcc.Link('Edit', href='/settings/settings_degreeprograms_profile?program_id='+str(row["Program ID"])+'&mode=edit')

        data_dict = df.to_dict()
        dictionarydata = {'Select':linkcolumn2}
        data_dict.update(dictionarydata)
        df =pd.DataFrame.from_dict(data_dict)
        df = df[["Program Name", "Select"]]
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        return [is_open1, table]

    if sdegprogname:
        sqlcommand = "SELECT program_id, program_name FROM programs WHERE program_delete_ind = %s and program_name ILIKE %s ORDER By program_name"
        values = (False, "%"+sdegprogname+"%")

    else:
        sqlcommand = "SELECT program_id, program_name FROM programs WHERE program_delete_ind = %s ORDER By program_name"
        values = (False,)


    columns = ['program_id', 'program_name']
    df = securequerydatafromdatabase(sqlcommand, values,columns)
    df.columns=["Program ID", "Program Name"]
    columns = [{"degprogname":i, "degprogid":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn2 = {}
    for index, row in df.iterrows():
        linkcolumn2[index]=dcc.Link('Edit', href='/settings/settings_degreeprograms_profile?program_id='+str(row["Program ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn2}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    df = df[["Program Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

    return [is_open1, table]
