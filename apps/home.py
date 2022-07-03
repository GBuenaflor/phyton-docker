import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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


layout = html.Div([
    dbc.Spinner([
        commonmodules.get_header(),
        commonmodules.get_menu(),
        commonmodules.get_common_variables(),
        html.H1("Welcome!"),
        html.Hr(),
        html.Div([
            dbc.Card([
                dbc.CardHeader(
                    html.H4("Announcements"),
                    style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                ),
                dbc.CardBody([
                    html.Div([
                        dbc.Row([
                            dbc.Col([

                                html.Div([
                                    html.Div([html.H5("You can now apply for monetization today, October 11, 2021, 1PM", style={'color': 'rgb(123,20,24)'})]),
                                ]),
                                html.Div([
                                    dcc.Markdown('''Login as Faculty/Admin/REPS and just go to Leave/Monetization Application module > Apply for Monetization'''),
                                ]),

                            ])
                        ]),
                    ],id = 'announcement_mone'),

                    html.Br(),
                    html.Div([
                        dbc.Row([
                            dbc.Col([

                                html.Div([
                                    html.Div([html.H5("Reporting Bugs and Desired Enhancements", style={'color': 'rgb(123,20,24)'})]),
                                ]),
                                html.Div([
                                    dcc.Markdown('''Welcome to the **HRDO PUSO (Personnel Unified Systems Outlook)** System. This system is a home-grown information system developed by the **Information Systems Group** of the *Department of Industrial Engineering and Operations Research.*
                                    For comments and suggestions, please contact us via this:'''), html.A(["Feedback link"], href="https://forms.gle/HEzPaayeVdjD1Xbp9")
                                ]),

                            ])
                        ])
                    ])

                ])
            ]),
            dbc.Card([
                dbc.CardHeader(
                    html.H4("Leave Credits information"),
                    style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P(id="home_leave_credits_description")
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div(id="home_leave_credits")
                        ])
                    ]),
                    html.Hr(),

                ])
            ], style = {'display':'none'}, id = 'home_leavesdashboardcard'),
            dbc.Card([
                dbc.CardHeader(
                    html.H4("Basic Paper Dashboard"),
                    style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Alert("This is a success alert! Well done!", color="success", id="totalinprocessbp"),
                        ]),
                        dbc.Col([
                            dbc.Alert("This is a danger alert. Scary!", color="danger", id="totalreturnedbp"),
                        ]),
                    ]),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([

                            html.Div([
                                html.Div([html.H5("Pending Basic Papers", style={'color': 'rgb(123,20,24)'})]),
                            ]),
                            html.Div([
                                dcc.Markdown('''The following are the current basic papers and their current status in the processing pipeline.
                                Please make sure that the basic papers are approved by the unit head by the deadline stated by HRDO such that there would be enough processing lead time.'''),

                            ]),
                            html.Div([
                                html.Div(id="t_bp_statuses")
                            ])


                        ])
                    ]),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([

                            # html.Div([
                            #     html.Div([html.H5("Pending Basic Papers", style={'color': 'rgb(123,20,24)'})]),
                            # ]),
                            html.Div([
                                dcc.Markdown('''These are the following pending basic papers and their appointment types.'''),

                            ]),
                            html.Div([
                                html.Div(id="t_bp_statuses_appt")
                            ])


                        ])
                    ]),

                ])
            ], style = {'display':'none'}, id = 'home_bpdashboardcard')


        ])
    ],color="danger")

])






@app.callback(
    [
        Output('t_bp_statuses', 'children'),
        Output('t_bp_statuses_appt','children'),
        Output('totalreturnedbp','children'),
        Output('totalinprocessbp','children'),
        Output('home_bpdashboardcard', 'style'),
        Output('home_leavesdashboardcard', 'style'),
        Output('home_leave_credits_description', 'children'),
        Output('home_leave_credits', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('sessioncurrentunit', 'modified_timestamp'),
    ],
    [
        State('sessioncurrentrole', 'data'),
        State('current_user_id', 'data'),
        State('sessionroleunits', 'data'),
        State('sessiondefaultrole', 'data'),
        State('sessionlistofunits', 'data'),
        State('sessioncurrentunit', 'data'),
        State('sessioncurrentuserroleid', 'data')
    ]
)
def g_bp_statuses(url, sessioncurrentunit_time,sessioncurrentrole, currentuserid, sessionroleunits, sessiondefaultrole,
                     sessionlistofunits, sessioncurrentunit, sessioncurrentuserroleid):
    try:
        listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    except:
        listofallowedunits = (2,)

    # print('test printing sessioncurrentuserroleid, ', sessioncurrentuserroleid)

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    # print('printing sessioncurrentrole from home, ', sessioncurrentrole)
    # print('printing sessioncurrentunit from home, ', sessioncurrentunit)

    if url =='/home':
        if (sessioncurrentrole in [26, 28, 36]) or (sessioncurrentrole is None):
            home_bpdashboardcard = {'display': 'none'}
            home_leavesdashboardcard = {'display': 'inline'}
            # print('printing from leave credits path')
        else:
            home_bpdashboardcard = {'display': 'inline'}
            home_leavesdashboardcard = {'display': 'none'}
            # print('printing from bp path')


        sqlcommand = '''
            select bs.bp_status_id, bp_status_name as "Status", COUNT(bp.bp_id) as "Count of BP"
            FROM basic_papers bp LEFT join bp_status_changes bsc ON bsc.bp_id = bp.bp_id
            INNER JOIN bp_statuses bs ON bs.bp_status_id = bsc.bp_status_id
            WHERE bp_delete_ind = %s and bp_status_change_current_ind = %s and bp_designation_unit_id in %s
            GROUP BY bs.bp_status_id,bp_status_name
            ORDER BY COUNT(bp.bp_id) DESC'''
        columns = ["bp_status_id","Status", "Count of BP"]
        df = securequerydatafromdatabase(sqlcommand, [False, True,listofallowedunits], columns)
        country_list = [1,22,21,2,3,4,5,32,33,38,42,43,44,45,46,47]

        filtered_df = df[df['bp_status_id'].isin(country_list)]
        if not filtered_df.empty:
            countofbackbp= filtered_df['Count of BP'].sum()
            totalbp = df['Count of BP'].sum()
            countofinprocessbp = int(totalbp) - int(countofbackbp)
            countofbackbp = 'Count of BPs Requiring Unit Intervention: '+ str(countofbackbp)
            countofinprocessbp = 'Count of BPs Under Processing: '+ str(countofinprocessbp)
        else:
            countofbackbp = 'Count of BPs Requiring Unit Intervention: '
            countofinprocessbp = 'Count of BPs Under Processing: '
        dfcopy = df[["Status", "Count of BP"]].copy()
        table = dbc.Table.from_dataframe(dfcopy, striped=True, bordered=True, hover=True)



        sqlcommand2 = '''
            select appt_type_name as "Appointment Type", emp_class_name as "Type of Employee", COUNT(bp.bp_id) as "Count of BP"
            FROM basic_papers bp inner join appointment_types atp ON atp.appt_type_id = bp_appt_type_id
            INNER JOIN emp_classes ec ON ec.emp_class_id = bp.bp_emp_class_id
            WHERE bp_delete_ind = %s and bp_designation_unit_id in %s
            GROUP BY appt_type_name, emp_class_name
            ORDER BY COUNT(bp.bp_id) DESC
            '''

        columns2 = ["Appointment Type","Type of Employee", "Count of BP"]
        df2 = securequerydatafromdatabase(sqlcommand2, [False,listofallowedunits], columns2)
        table2 = dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True)


        #leave credits section
        sqlemp = '''SELECT emp_id
                      FROM employees e
                    LEFT JOIN users u ON u.person_id = e.person_id
                     WHERE user_id = %s '''
        valuesemp = (currentuserid, )
        columnsemp = ['emp_id']
        dfemp = securequerydatafromdatabase(sqlemp, valuesemp, columnsemp)

        vlcount = 0
        if dfemp.empty or dfemp["emp_id"][0] == None:
            table3 = None
            description = "This account does not have an employee id."
        else:
            emp_id = str(dfemp["emp_id"][0])
            # print(emp_id, 'emp_id')
            sqlcommand = '''SELECT CASE WHEN lt.leave_type_class_id = %s THEN 'Sick Leave Credit Earned'
                WHEN lt.leave_type_class_id = %s THEN 'Vacation Leave Credit Earned'
                ELSE '' END AS LeaveType,
				leave_credits_balance,
                CASE WHEN leave_credits_balance_as_of IS NULL THEN leave_emp_modified_on
                WHEN (leave_emp_modified_on IS NULL AND leave_credits_balance_as_of IS NULL) THEN leave_emp_inserted_on
                ELSE leave_credits_balance_as_of END AS Date
                FROM leave_employees le
                LEFT JOIN leave_types lt ON lt.leave_type_id = le.leave_type_id
                WHERE leave_credits_current_bal_ind = %s
                AND lt.leave_type_class_id IN (%s, %s)
                AND leave_emp_delete_ind = %s
                AND emp_id = %s
                ORDER BY leave_type_name

                '''
            values = [2, 1, True, 1, 2, False, emp_id]
            columns = ['leave_type_name', 'leave_credits_balance', 'Date']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            if not df.empty:
                df = df[['leave_type_name', 'leave_credits_balance', 'Date']]
                df['Date'] = df['Date'].dt.strftime('%m/%d/%Y %H:%M')
                df.columns = ["Leave Type", "Balance", "As of"]
                table3 = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
                description = "Here are your sick/vacation leave credits. These are subject to adjustment due to various concerns."
                vlcount = int(df["Balance"][1])
            else:
                table3 = None
                description = "You do not have any sick or vacation leave credits as of today. If this is incorrect, please contact HRDO."

        return [table,table2,countofbackbp,countofinprocessbp, home_bpdashboardcard, home_leavesdashboardcard, description, table3]
    else:
        raise PreventUpdate
