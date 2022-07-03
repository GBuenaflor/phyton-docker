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
import urllib.parse as urlparse
from urllib.parse import parse_qs


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Performance Rating"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Performance Rating", id="btnaddnewperfrating", color="primary",
                                   href='/settings/settings_performancerating_profile?&mode=add'),  # block=True
                    ]),

                    # dbc.Col([
                    #     dbc.FormGroup(
                    #         [
                    #             dbc.Label("Search Designation", width=4,
                    #                       style={"text-align": "left"}),
                    #             dbc.Col([
                    #                 dbc.Input(
                    #                     type="text", id="sdesignationname", placeholder="Enter search string"
                    #                 ),
                    #
                    #             ],
                    #                 width=8
                    #             )
                    #         ],
                    #         row=True
                    #     ),
                    # ]),

                ]),
                html.Br(),
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Search by", width=2, style={"text-align": "left"}),
                                        dbc.Col([
                                            dbc.RadioItems(
                                                id = "perf_rating_searchby",
                                                options=[
                                                    {"label": "Employee Number", "value": 1},
                                                    {"label": "Name", "value": 2},
                                                ]
                                            )
                                            #dbc.FormFeedback("Too short or already taken", valid = False)
                                        ],
                                            width=8
                                        ),

                                        ],
                                    row=True
                                ),
                            ])
                        ])
                    ])
                ], className="border-dark", style={"background-color": "#cfcfcf"}),
                html.Br(),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Employee #", width=2, style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="perf_rating_empnosearch", placeholder="Enter employee number"
                                        ),
                                        #dbc.FormFeedback("Too short or already taken", valid = False)
                                    ],
                                        width=8
                                    ),
                                    dbc.Col([
                                        dbc.Button("Search", color="primary", id="btn_perf_rating_empnosearch")
                                    ])],
                                row=True
                            ),
                        ])
                    ]),
                ], id="perf_rating_divempnosearch", style={'display':'none'}),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Employee", width=2, style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id="perf_rating_emp",
                                            options=[
                                            ],
                                            # value="",
                                            searchable=True,
                                            clearable=True
                                        )
                                        #dbc.FormFeedback("Too short or already taken", valid = False)
                                    ],
                                        width=8
                                    )],
                                row=True
                            ),
                        ])
                    ]),
                ], id="perf_rating_divempsearch", style={'display':'none'}),

                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Employee #", width=2, style={"text-align": "left"}),
                                dbc.Col([
                                    html.P(" ", id="perf_rating_empno", style={"font-weight":"bold"}),
                                ], width=8)

                                ],
                            row=True
                        ),
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Designation", width=2, style={"text-align": "left"}),
                                dbc.Col([
                                    html.P(" ", id="perf_rating_desig", style={"font-weight":"bold"}),
                                ], width=8)

                                ],
                            row=True
                        ),
                    ])
                ]),

                html.Hr(),
                html.H4("Existing performance ratings"),

                html.Div([

                ], id="editperfratingdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='perfratingsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='perfratingid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editperfratingdatatable', 'children')
               ],
              [
    Input('perf_rating_emp', 'value'),
    Input('perfratingsubmitstatus', 'value'),
],
    [
],)
def querymodulesfordtcall(perf_rating_emp, perfratingsubmitstatus):
    # if sdesignationname:
    #     sdesignationname = "%"+sdesignationname+"%"
    #     sqlcommand = "SELECT designation_id, designation_name FROM designations WHERE designation_delete_ind = %s and designation_current_ind = %s and designation_name ILIKE %s ORDER By designation_name"
    #     values = (False, True, sdesignationname)
    # else:

    if perf_rating_emp:
        sqlcommand = '''SELECT perf_rating_id, perf_rating_start_period, perf_rating_end_period, perf_rating FROM performance_ratings
        WHERE emp_id = %s and perf_rating_delete_ind = %s'''
        values = (perf_rating_emp, False, )

        columns = ["perf_rating_id", "perf_rating_start_period", "perf_rating_end_period", "perf_rating"]
        df = securequerydatafromdatabase(sqlcommand, values, columns)
        df.columns = ["Rating ID", "Start Period", "End Period", "Performance Rating"]
        columns = [{"name": i, "id": i} for i in df.columns]
        data = df.to_dict("rows")
        linkcolumn = {}
        for index, row in df.iterrows():
            linkcolumn[index] = dcc.Link(
                'Edit', href='/settings/settings_performancerating_profile?perf_rating_id='+str(row["Rating ID"])+'&mode=edit')

        data_dict = df.to_dict()
        dictionarydata = {'Select': linkcolumn}
        data_dict.update(dictionarydata)
        df = pd.DataFrame.from_dict(data_dict)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        return [table]
    else:
        raise PreventUpdate

@app.callback([Output('perf_rating_empno', 'children'),
            Output('perf_rating_desig', 'children')
               ],
              [
    Input('perf_rating_emp', 'value'),
    Input('perfratingsubmitstatus', 'value'),
],
    [
],)
def querymodulesfordtcall(perf_rating_emp, perfratingsubmitstatus):
    # if sdesignationname:
    #     sdesignationname = "%"+sdesignationname+"%"
    #     sqlcommand = "SELECT designation_id, designation_name FROM designations WHERE designation_delete_ind = %s and designation_current_ind = %s and designation_name ILIKE %s ORDER By designation_name"
    #     values = (False, True, sdesignationname)
    # else:

    if perf_rating_emp:
        sqlcommand = '''SELECT emp_number, designation_name from employees e
            LEFT JOIN designations d ON d.designation_id = e.emp_primary_designation_id
            where emp_id = %s'''
        values = (perf_rating_emp,)

        columns = ["emp_id", "designation_name"]
        df = securequerydatafromdatabase(sqlcommand, values, columns)
        perf_rating_empno = df['emp_id'][0]
        perf_rating_desig = df['designation_name'][0]


        return [perf_rating_empno, perf_rating_desig]
    else:
        raise PreventUpdate

@app.callback([
    Output('perf_rating_emp', 'options'),

],
    [
    Input('url', 'pathname'),
],
    [
    State('url', 'search'),
    State('sessioncurrentunit', 'data'),
    State('sessionlistofunits', 'data'),
    # State('admin_pos_id', 'data')

],)
def degree_level_fillindropdowns(path, url, sessioncurrentunit,sessionlistofunits):
    parsed = urlparse.urlparse(url)
    if path == "/settings/settings_performancerating":
        # mode = str(parse_qs(parsed.query)['mode'][0])
        # if mode == "edit":
        #     admin_pos_load_data = 1
        # else:
        #     admin_pos_load_data = 2
        # listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

        listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

        employees = commonmodules.queryfordropdown('''
            SELECT person_last_name || ', ' || person_first_name as label, emp_id as value
           FROM employees e INNER JOIN persons p ON p.person_id = e.person_id
           WHERE emp_delete_ind = %s AND (emp_class_id = %s OR emp_class_id = %s) AND emp_primary_home_unit_id IN %s
           ORDER BY person_last_name
        ''', (False, 2, 3, listofallowedunits ))

        # degreelevel = commonmodules.queryfordropdown('''
        #     SELECT degree_level as label, degree_level_id as value
        #       FROM degree_levels dl
        #      WHERE dl.degree_level_delete_int = %s
        #    ORDER BY degree_level
        # ''', (False, ))



        return [employees]
    else:
        raise PreventUpdate


@app.callback(


    #for sabbatical only
    [Output('perf_rating_divempnosearch', 'style'),
    Output('perf_rating_divempsearch', 'style'),
    ],


    [Input('perf_rating_searchby', 'value')]

    # Input('url', 'pathname'),

    # [
    # State('url', 'search'),
    # ]
)
def toggle_divforeigncit(perf_rating_searchby):
    ctx = dash.callback_context
    # parsed = urlparse.urlparse(url)
    # if path == "/leaves/leavesentry_profile":


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]


        if eventid == 'perf_rating_searchby':
            if perf_rating_searchby == 1:

                return [{'display': 'inline'}, {'display': 'none'}]
            else:
                return [{'display': 'none'}, {'display': 'inline'}]
            # if 1 in sabbatical_first_time:
            #     return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'inline'}, {'display': 'inline'}, {'display': 'inline'}]
            # else:
            #     return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'inline'}, {'display': 'inline'}, {'display': 'none'}]


        else:
            raise PreventUpdate
    # elif (path == "/leaves/leavesentry_profile" and lwops_lwop_type_dd in [3, 5, 8, 9]):
    #     return [{'display': 'inline'}, {'display': 'inline'}, {'display': 'inline'}, {'display': 'inline'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]
    else:
        raise PreventUpdate
