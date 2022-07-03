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
    html.H1("Leave Approval Flows"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Leave Approval Flows"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Leave Approval Flow", id="leave_btnaddnewbpflow", color="primary",
                                   href='/settings/settings_leave_approval_flows_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Leave Approval Flow Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="search_leaveflow_input", placeholder="Enter search string"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                    # html.Div([
                    #
                    #     dbc.Col([
                    #         dbc.FormGroup(
                    #             [
                    #                 dbc.Label("Search Leave Flow", width=3,
                    #                           style={"text-align": "left"}),
                    #                 dbc.Col([
                    #                     dbc.Input(
                    #                         type="text", id="search_leaveflow_input", placeholder="Enter search string"
                    #                     ),
                    #
                    #                 ],
                    #                     width=9
                    #                 ),
                    #
                    #             ],
                    #             row=True
                    #         ),
                    #     ]),
                    #
                    #
                    #     dbc.Row([
                    #         dbc.Col([
                    #             dbc.Button("Show All", color="primary",
                    #                        className="mr-1", id="leaveflows_show_all"),
                    #         ])
                    #     ]),
                    #
                    # ], style = {'display': 'none'}),


                ]),

                html.Hr(),
                html.H4("Existing Leave Approval Flows"),

                html.Div([

                ], id="leaveflowsdt"),

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
        Output('leaveflowsdt', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('search_leaveflow_input', 'value'),

    ],
    [
    ],
)
def leaveappflow_querymodulesfordtcall(url, search_leaveflow_input):

    if search_leaveflow_input:
        search_leaveflow_input = "%"+search_leaveflow_input+"%"
        sqlcommand = """
                    SELECT leave_approval_flow_id, leave_approval_flow_name, leave_approval_flow_code
                    FROM leave_approval_flows
                    WHERE leave_approval_flow_delete_ind = %s
                    and leave_approval_flow_name ILIKE %s
                    ORDER BY leave_approval_flow_name ASC
                """
        values = (False, search_leaveflow_input)


        # sqlcommand = "SELECT leave_type_id, leave_type_name, leave_type_code FROM leave_types WHERE leave_type_delete_ind = %s and leave_type_name ILIKE %s ORDER By leave_type_name"
        # values = (False, sleavetypename)
    else:
        sqlcommand = """
                    SELECT leave_approval_flow_id, leave_approval_flow_name, leave_approval_flow_code
                    FROM leave_approval_flows
                    WHERE leave_approval_flow_delete_ind = %s

                    ORDER BY leave_approval_flow_name ASC
                """
        values = (False,)

        # sqlcommand = "SELECT leave_type_id, leave_type_name, leave_type_code FROM leave_types WHERE leave_type_delete_ind = %s ORDER By leave_type_name"
        # values = (False,)

    columns = ["leave_approval_flow_id", "leave_approval_flow_name", "leave_approval_flow_code"]

    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Leave Approval Flow ID", "Leave Approval Flow Name", "Leave Approval Flow Code"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_leave_approval_flows_profile?leave_approval_flow_id='+str(row["Leave Approval Flow ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Leave Approval Flow Name", "Leave Approval Flow Code", "Select"]]
    # print("HERE3456", df)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table, ]




    ###
    # sqlcommand = """
    #             SELECT leave_approval_flow_id, leave_approval_flow_name, leave_approval_flow_code
    #             FROM leave_approval_flows
    #             WHERE leave_approval_flow_delete_ind = %s
    #             ORDER BY leave_approval_flow_name ASC
    #         """
    # values = (False,)
    #
    #
    # columns = ["leave_approval_flow_id", "leave_approval_flow_name", "leave_approval_flow_code"]
    #
    # df = securequerydatafromdatabase(sqlcommand, values, columns)
    # df.columns = ["Leave Approval Flow ID", "Leave Approval Flow Name", "Leave Approval Flow Code"]
    # columns = [{"name": i, "id": i} for i in df.columns]
    # data = df.to_dict("rows")
    # linkcolumn = {}
    # for index, row in df.iterrows():
    #     linkcolumn[index] = dcc.Link(
    #         'Edit', href='/settings/settings_leave_approval_flows_profile?leave_approval_flow_id='+str(row["Leave Approval Flow ID"])+'&mode=edit')
    # data_dict = df.to_dict()
    # dictionarydata = {'Select': linkcolumn}
    # data_dict.update(dictionarydata)
    # df = pd.DataFrame.from_dict(data_dict)
    # df = df[["Leave Approval Flow Name", "Leave Approval Flow Code", "Select"]]
    # # print("HERE3456", df)
    # table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    # return [table, ]
