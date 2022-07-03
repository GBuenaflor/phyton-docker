
from dash_extensions.snippets import send_bytes
from dash_extensions import Download
from urllib.parse import quote
import io
import base64

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from datetime import date as date
from dash.dependencies import Input, Output, State
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid
import hashlib
from datetime import datetime
import pandas as pd
import urllib.parse as urlparse
from urllib.parse import parse_qs
import logging

app.config.suppress_callback_exceptions = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def parse_contents(contents, filename, date):

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:

        return html.Div([
            'There was an error processing this file.'
        ])
    data=df.to_dict('records')
    columns=[{'name': i, 'id': i} for i in df.columns]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return table, data, columns

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),

    dcc.Store(id='sg_profile_sessionproxy', storage_type='session'),
    dcc.Store(id='sg_profile_dfstore', storage_type='session'),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Salary Grade Tranche", id="sg_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Salary Grades", id="sg_results_head"),
                dbc.ModalBody([
                ], id="sg_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_sg_head_close",
                                       color="primary", block=True, href="/settings/settings_salary_grades"),
                        ], id="sg_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_sg_results_head_return",
                                       color="primary", block=True, href='/settings/settings_salary_grades'),
                        ], id="sg_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="sg_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Salary Grades', href='/settings/settings_salary_grades'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("SG Tranche Name*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="sg_name", placeholder="Enter SG Tranche Name"
                             ),
                             dbc.FormFeedback("Please enter a valid SG tranche name", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("SG Tranche Year*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="number", id="sg_year", placeholder="Enter SG Tranche Year"
                             ),
                             dbc.FormFeedback("Please enter a valid year", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("SG Tranche Start Date*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.DatePickerSingle(id='sg_startdate', placeholder="mm/dd/yyyy",
                                                  date=date.today(), display_format='MMM DD, YYYY'
                                                  ),
                             dbc.FormFeedback("Please enter valid start date.", valid=False),
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("SG Tranche End Date", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.DatePickerSingle(id='sg_enddate', placeholder="mm/dd/yyyy",
                                                  date=date.today(), display_format='MMM DD, YYYY'
                                                  ),
                             # dbc.FormFeedback("Please enter end date.", valid=False),
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.Label("Upload Salary Values", width=2, style={"text-align": "left"}),


                    dcc.Upload(
                                id='salary_data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=False
                            ),

                    dbc.Spinner([
                        html.Div([

                        ], id="sgprofiledt"),
                    ]),

                    html.Br(),


                    dbc.Row([
                        html.Div([


                            dbc.Button("Download Table As CSV", color='info',
                                       className='mr-1',
                                       n_clicks=0,
                                       id='download_btn',
                                       style={"background-color": "rgb(123,20,24)",
                                              'color': 'white'},
                                       block=True),
                            html.A(
                                id="download_link",
                                href="",
                                download="salaries.csv",
                                target="_blank"
                            ),
                            # dbc.Button("Download Results", id="download", block=True,
                            #            style={"background-color": "rgb(123,20,24)", 'color': 'white'}),
                        ], id = "sg_profile_downloadtable", style = {'display': 'none'}),
                        Download(id='downloadtranche')

                    ]),
                    html.Br(),

                    dbc.Row([
                        html.Div([

                            dbc.Button("Download Blank Table", color='info',
                                       className='mr-1',
                                       n_clicks=0,
                                       id='download_btn2',
                                       style={"background-color": "rgb(123,20,24)",
                                              'color': 'white'},
                                       block=True),



                            Download(id = 'downloadblank')



                            # dbc.Button("Download Results", id="download", block=True,
                            #            style={"background-color": "rgb(123,20,24)", 'color': 'white'}),
                        ])

                    ]),

                    html.Br(),


                    # html.A(
                    #
                    #     id="download_link2",
                    #     href="",
                    #     download="salaries.csv",
                    #     target="_blank"
                    # ),

                    html.Br(),

                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Mark Entire SG Tranche for Deletion?', 'value': '1'},
                            ], id='sg_chkmarkfordeletion', value=[]
                        ),
                    ], id='div_sg_delete', style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New SG Tranche", id="sg_submit_btn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="sg_cancel",
                                   href='/settings/settings_salary_grades', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),

                dbc.Row([
                    dbc.Label("Note: Uploading a new batch of SGs may take up to a few minutes.", width=8, style={"text-align": "left"}, color = "danger")

                ], style={'width': '100%'}, ),
                # dbc.Col([
                #
                #     html.Div([
                #         dcc.Input(id='sg_submit_status', type='text', value="0")
                #     ], style={'display': 'none'}),
                #     html.Div([
                #         dcc.Input(id='sg_id', type='text', value="0")
                #     ], style={'display': 'none'}),
                #     dcc.ConfirmDialog(
                #         id='sg_message',
                #     ), ], width=2
                # )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])
#
#
@app.callback(
    [
        Output('sg_name', 'value'),
        Output('sg_year', 'value'),
        Output('sg_startdate', 'date'),
        Output('sg_enddate', 'date'),
        # Output('sgprofiledt', 'children'),
        Output("sg_process_editmodalhead", "children"),
        Output("sg_submit_btn", "children"),
        Output("sg_chkmarkfordeletion", "value"),
        Output("div_sg_delete", "style"),


        # Output('sg_city', 'options'),
    ],
    [
        # Input('sg_submit_status', 'value'),
        # Input('btn_sg_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('sg_name', 'value'),
        State('sg_year', 'value'),
        State('sg_startdate', 'date'),
        State('sg_enddate', 'date'),
        State('sgprofiledt', 'children'),
        State('sg_process_editmodalhead', "children"),
        State("sg_submit_btn", "children"),
        State("sg_chkmarkfordeletion", "value"),

    ]

)
def returnsgdata(
        url,
        sg_name, sg_year, sg_startdate, sg_enddate, sgprofiledt,
        sg_process_editmodalhead, sg_submit_btn,
        sg_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            sg_tranche_id = str(parse_qs(parsed.query)['sg_tranche_id'][0])
            sql = '''
            SELECT sg_tranche_name, sg_tranche_year, sg_tranche_effectivity_start_date,  sg_tranche_effectivity_end_date
            FROM sg_tranches
            WHERE sg_tranche_id = %s
            AND sg_tranche_delete_ind = %s
                  '''
            values = (sg_tranche_id, False)
            columns = ['sg_tranche_name', 'sg_tranche_year', 'sg_tranche_effectivity_start_date', 'sg_tranche_effectivity_end_date']
            df = securequerydatafromdatabase(sql, values, columns)
            sg_name = df["sg_tranche_name"][0]
            sg_year = df["sg_tranche_year"][0]
            sg_startdate = df["sg_tranche_effectivity_start_date"][0]
            sg_enddate = df["sg_tranche_effectivity_end_date"][0]

            sql2 = '''
            SELECT sg_number_step, sg_version_salary_rate
            FROM salary_grades sg
            INNER JOIN salary_grade_versions sgv ON sg.sg_id = sgv.sg_id
            INNER JOIN sg_tranches sgt ON sgv.sg_tranche_id = sgt.sg_tranche_id
            WHERE sgt.sg_tranche_id = %s
            AND sg_tranche_delete_ind = %s
            AND sg_delete_ind = %s
            ORDER BY sgv.sg_id ASC
              '''

            values2 = (sg_tranche_id, False, False)
            columns2 = ['Salary Grade', 'Salary']
            df2 = securequerydatafromdatabase(sql2, values2, columns2)
            sgprofiledt = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True)

            dfstore = df2.to_dict('records')

            values = [sg_name, sg_year, sg_startdate, sg_enddate,
                      "Edit Existing SG Tranche:",
                      "Save Changes", [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":

            values = ["", "", date.today(), date.today(), sg_process_editmodalhead,
                      sg_submit_btn, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate

@app.callback([
                Output('sgprofiledt','children'),
                Output('sg_profile_dfstore', 'data')


                ],
              [Input('salary_data', 'contents'),
               Input("url", "search")],
                [State('salary_data', 'filename'),
                 State('salary_data', 'last_modified')]
)
def updatesupplydemandmodel(list_of_contents, url, list_of_names, list_of_dates):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    # if parsed.query:
    #     if parse_qs(parsed.query)['mode'][0] == "edit":
    # sg_tranche_id = str(parse_qs(parsed.query)['sg_tranche_id'][0])


    if list_of_contents is not None:

        children, data, columns= parse_contents(list_of_contents, list_of_names, list_of_dates)
        tempval = 5

        df = pd.DataFrame.from_dict(data)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        return [table, df.to_dict('records')]

    if parsed.query:

        if parse_qs(parsed.query)['mode'][0] == "edit":

            sg_tranche_id = str(parse_qs(parsed.query)['sg_tranche_id'][0])

            sql2 = '''
            SELECT sg_number_step, sg_version_salary_rate
            FROM salary_grades sg
            INNER JOIN salary_grade_versions sgv ON sg.sg_id = sgv.sg_id
            INNER JOIN sg_tranches sgt ON sgv.sg_tranche_id = sgt.sg_tranche_id
            WHERE sgt.sg_tranche_id = %s
            AND sg_tranche_delete_ind = %s
            AND sg_delete_ind = %s
            ORDER BY sgv.sg_id ASC
              '''

            values2 = (sg_tranche_id, False, False)
            columns2 = ['Salary Grade', 'Salary']
            df2 = securequerydatafromdatabase(sql2, values2, columns2)
            sgprofiledt = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True)

            dfstore = df2.to_dict('records')


            values = [sgprofiledt, dfstore]
            return values

        elif parse_qs(parsed.query)['mode'][0] == "add":

            values = [[],[]]
            return values

        else:

            raise PreventUpdate
    else:

        raise PreventUpdate

@app.callback(

    [Output('download_link', "href")],
    [Input("download_btn", "n_clicks")],

    [State("sg_profile_dfstore", "data")]
    # [State("inst_collapse", "is_open")]

)

def downloaddataexcel(download_btn, sg_profile_dfstore):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'download_btn':

            df = pd.DataFrame(sg_profile_dfstore)


            csv_str = df.to_csv(index=False, encoding='utf-8')
            csv_str = "data:text/csv;charset=utf-8," + quote(csv_str)

            return [csv_str]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output("downloadtranche", "data")],
    [Input("download_btn2", "n_clicks")]

)
def generate_csv(download_btn2):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'download_btn2':

            df = pd.DataFrame({'Salary Grade': ['1-1',	'1-2',	'1-3',	'1-4',	'1-5',	'1-6',	'1-7',	'1-8',	'2-1',	'2-2',	'2-3',	'2-4',	'2-5',	'2-6',	'2-7',	'2-8',	'3-1',	'3-2',	'3-3',	'3-4',	'3-5',	'3-6',	'3-7',	'3-8',	'4-1',	'4-2',	'4-3',	'4-4',	'4-5',	'4-6',	'4-7',	'4-8',	'5-1',	'5-2',	'5-3',	'5-4',	'5-5',	'5-6',	'5-7',	'5-8',	'6-1',	'6-2',	'6-3',	'6-4',	'6-5',	'6-6',	'6-7',	'6-8',	'7-1',	'7-2',	'7-3',	'7-4',	'7-5',	'7-6',	'7-7',	'7-8',	'8-1',	'8-2',	'8-3',	'8-4',	'8-5',	'8-6',	'8-7',	'8-8',	'9-1',	'9-2',	'9-3',	'9-4',	'9-5',	'9-6',	'9-7',	'9-8',	'10-1',	'10-2',	'10-3',	'10-4',	'10-5',	'10-6',	'10-7',	'10-8',	'11-1',	'11-2',	'11-3',	'11-4',	'11-5',	'11-6',	'11-7',	'11-8',	'12-1',	'12-2',	'12-3',	'12-4',	'12-5',	'12-6',	'12-7',	'12-8',	'13-1',	'13-2',	'13-3',	'13-4',	'13-5',	'13-6',	'13-7',	'13-8',	'14-1',	'14-2',	'14-3',	'14-4',	'14-5',	'14-6',	'14-7',	'14-8',	'15-1',	'15-2',	'15-3',	'15-4',	'15-5',	'15-6',	'15-7',	'15-8',	'16-1',	'16-2',	'16-3',	'16-4',	'16-5',	'16-6',	'16-7',	'16-8',	'17-1',	'17-2',	'17-3',	'17-4',	'17-5',	'17-6',	'17-7',	'17-8',	'18-1',	'18-2',	'18-3',	'18-4',	'18-5',	'18-6',	'18-7',	'18-8',	'19-1',	'19-2',	'19-3',	'19-4',	'19-5',	'19-6',	'19-7',	'19-8',	'20-1',	'20-2',	'20-3',	'20-4',	'20-5',	'20-6',	'20-7',	'20-8',	'21-1',	'21-2',	'21-3',	'21-4',	'21-5',	'21-6',	'21-7',	'21-8',	'22-1',	'22-2',	'22-3',	'22-4',	'22-5',	'22-6',	'22-7',	'22-8',	'23-1',	'23-2',	'23-3',	'23-4',	'23-5',	'23-6',	'23-7',	'23-8',	'24-1',	'24-2',	'24-3',	'24-4',	'24-5',	'24-6',	'24-7',	'24-8',	'25-1',	'25-2',	'25-3',	'25-4',	'25-5',	'25-6',	'25-7',	'25-8',	'26-1',	'26-2',	'26-3',	'26-4',	'26-5',	'26-6',	'26-7',	'26-8',	'27-1',	'27-2',	'27-3',	'27-4',	'27-5',	'27-6',	'27-7',	'27-8',	'28-1',	'28-2',	'28-3',	'28-4',	'28-5',	'28-6',	'28-7',	'28-8',	'29-1',	'29-2',	'29-3',	'29-4',	'29-5',	'29-6',	'29-7',	'29-8',	'30-1',	'30-2',	'30-3',	'30-4',	'30-5',	'30-6',	'30-7',	'30-8',	'31-1',	'31-2',	'31-3',	'31-4',
                                                '31-5',	'31-6',	'31-7',	'31-8',	'32-1',	'32-2',	'32-3',	'32-4',	'32-5',	'32-6',	'32-7',	'32-8',	'33-1',	'33-2'],
                               'Salary': ['',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',
                                          '',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'',	'']})

            def to_xlsx(bytes_io):
                xslx_writer = pd.ExcelWriter(bytes_io)
                df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
                xslx_writer.save()

            return [send_bytes(to_xlsx, "sg_template.xlsx")]
            # return [send_data_frame(df.to_csv, filename="salaries.csv")]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [Output("downloadblank", "data")],
    [Input("download_btn", "n_clicks")],
    [State("sg_profile_dfstore", "data")]

)
def generate_csv2(download_btn, sg_profile_dfstore):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'download_btn':

            df = pd.DataFrame(sg_profile_dfstore)

            def to_xlsx(bytes_io):
                xslx_writer = pd.ExcelWriter(bytes_io)
                df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
                xslx_writer.save()

            return [send_bytes(to_xlsx, "salary_amounts.xlsx")]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("sg_name", "valid"),
        Output("sg_name", "invalid"),
        # Output("sg_city", "valid"),
        # Output("sg_city", "invalid"),
        Output("sg_year", "valid"),
        Output("sg_year", "invalid"),
        Output("sg_startdate", "valid"),
        Output("sg_startdate", "invalid"),
        # Output("sg_enddate", "valid"),
        # Output("sg_enddate", "invalid"),

        Output('sg_results_modal', "is_open"),
        Output('sg_results_body', "children"),
        Output('sg_results_head_close', "style"),
        Output('sg_results_head_return', "style"),
    ],
    [
        Input('sg_submit_btn', 'n_clicks'),
        Input('btn_sg_head_close', 'n_clicks'),
        Input('btn_sg_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('sg_name', 'value'),
        State("sg_year", "value"),
        State("sg_startdate", "date"),
        State("sg_enddate", "date"),

        State("sg_submit_btn", "children"),
        State("sg_chkmarkfordeletion", "value"),
        State("url", "search"),
        State("sg_profile_dfstore", "data")

    ]

)
def processdata(sg_submit_btn, btn_sg_head_close, btn_sg_results_head_return,
                current_user_id, sg_name, sg_year, sg_startdate, sg_enddate,
                mode, sg_chkmarkfordeletion, url, sg_profile_dfstore):

    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False, False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'sg_submit_btn':
            if sg_name:
                is_valid_sg_name = True
            else:
                is_valid_sg_name = False

            if sg_year:
                is_valid_sg_year = True
            else:
                is_valid_sg_year = False

            if sg_startdate:
                is_valid_sg_startdate = True
            else:
                is_valid_sg_startdate = False

            if sg_enddate:
                is_valid_sg_enddate = True
            else:
                is_valid_sg_enddate = False

            validity = [
                is_valid_sg_name, not is_valid_sg_name,
                is_valid_sg_year, not is_valid_sg_year,
                is_valid_sg_startdate, not is_valid_sg_startdate,
                # is_valid_sg_enddate, not is_valid_sg_enddate,
            ]
            allvalid = [is_valid_sg_name,
                        is_valid_sg_year,
                        is_valid_sg_startdate,
                        # is_valid_sg_enddate
                        ]

            if all(allvalid):

                if mode == "Save New SG Tranche":
                    #add mode
                    sql = """
                        INSERT INTO sg_tranches (sg_tranche_name, sg_tranche_year, sg_tranche_effectivity_start_date, sg_tranche_effectivity_end_date,
                        sg_tranche_inserted_by, sg_tranche_inserted_on, sg_tranche_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING sg_tranche_id

                    """
                    values = (sg_name, sg_year, sg_startdate, sg_enddate,
                              current_user_id, datetime.now(), False)

                    sg_tranche_id = modifydatabasereturnid(sql, values)

                    for i in range(len(sg_profile_dfstore)):

                        # print("I6", i, sg_profile_dfstore[i])
                        # print("HEREEE", sg_profile_dfstore[i]['Salary'],
                        #       sg_tranche_id,
                        #       i + 1,
                        #       False)
                        sql2 = """
                                    INSERT INTO salary_grade_versions (sg_tranche_id, sg_id, sg_version_salary_rate, sg_version_delete_ind)
                                    VALUES (%s, %s, %s, %s)
                                """

                        values2 = (sg_tranche_id, i+1, sg_profile_dfstore[i]['Salary'], False)

                        modifydatabase(sql2, values2)

                    displayed = True
                    message = "Successfully added salary grades"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}

                elif mode == "Save Changes":
                    #edit mode

                    sg_tranche_id = int(parse_qs(parsed.query)['sg_tranche_id'][0])

                    if parse_qs(parsed.query):
                        parsed = urlparse.urlparse(url)


                        sql = """
                            UPDATE sg_tranches SET sg_tranche_name = %s, sg_tranche_year = %s, sg_tranche_effectivity_start_date = %s, sg_tranche_effectivity_end_date = %s,
                        sg_tranche_inserted_by = %s, sg_tranche_inserted_on = %s, sg_tranche_delete_ind  = %s
                                 WHERE sg_tranche_id = %s
                        """

                        if '1' in sg_chkmarkfordeletion:
                            fordelete = True
                        else:
                            fordelete = False
                        values = (sg_name, sg_year, sg_startdate, sg_enddate,
                                  current_user_id, datetime.now(), fordelete, sg_tranche_id)
                        modifydatabase(sql, values)



###

                        sql1 = '''
                                    SELECT sg_version_id
                                    FROM salary_grade_versions
                                    WHERE sg_tranche_id = %s
                                    AND sg_version_delete_ind = %s

                                '''

                        values1 = (sg_tranche_id, False)
                        columns1 = ['sg_version_id']
                        df1 = securequerydatafromdatabase(sql1, values1, columns1)

                        if not df1.empty:

                            for i in range(len(sg_profile_dfstore)):

                                sql2 = """
                                            UPDATE salary_grade_versions SET sg_version_salary_rate = %s
                                            WHERE sg_tranche_id = %s
                                            AND sg_id = %s
                                            AND sg_version_delete_ind = %s
                                        """

                                values2 = (sg_profile_dfstore[i]['Salary'], sg_tranche_id, i+1, False)

                                modifydatabase(sql2, values2)

                        else:
                            for i in range(len(sg_profile_dfstore)):

                                sql2 = """
                                                   INSERT INTO salary_grade_versions (sg_tranche_id, sg_id, sg_version_salary_rate, sg_version_delete_ind)
                                                   VALUES (%s, %s, %s, %s)
                                               """

                                values2 = (sg_tranche_id, i + 1, sg_profile_dfstore[i]['Salary'], False)

                                modifydatabase(sql2, values2)


                        validity = [
                            False, False, False, False, False, False
                        ]
                        stylehead_close = {'display': 'none'}
                        stylehead_return = {'display': 'inline'}
                        displayed = True
                        message = "Successfully edited salary grades"
                        status = "1"
                else:
                    raise PreventUpdate
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display': 'inline'}
                stylehead_return = {'display': 'none'}
            out = [displayed, message, stylehead_close, stylehead_return]
            out = validity + out
            return out
        elif eventid == 'btn_sg_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display': 'inline'}
            stylehead_return = {'display': 'none'}
            out = [displayed, message, stylehead_close, stylehead_return]
            out = validity + out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [Output('sg_profile_downloadtable', 'style')],
    [Input('url', 'search')]
)

def stylesg_profile_downloadtable(url):
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            return [{'display':'inline'}]
        elif parse_qs(parsed.query)['mode'][0] == "add":
            return [{'display': 'none'}]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate