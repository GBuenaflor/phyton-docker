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

leaveflowass_emptype_dict = {0:"Any", 1: 'Faculty (Full-time)', 2: 'Administrative Personnel', 3:'Research and Extension Professional Staff (REPS)', 4:'Faculty (Administrator)'}


# bpflowass_appttype_dict = {0: 'Any', 1: 'Additional Assignment - Original', 2:'Additional Assignment - Renewal', 3: 'Additional Assignment - Temporary',  12:'Original', 13:'Permanency/Tenure', 14:'Promotion', 15: 'Promotion - Automatic', 18:'Promotion - Merit', 19: 'Reappointment - MC 11, Cat II',
#                            20:'Reclassification', 21: 'Reemployement', 22: 'Renewal', 23: 'Renewal with Promotion', 27: 'Transfer - Lateral', 28: 'Transfer - With Promotion'}

# bpflowass_numfail_dict = {0:'Any', 1:'0', 2:'At Least 1'}
#
# bpflowass_sg_dict = {0:'Any', 1:'SG 1 to 17', 2:'SG 18 to 33'}
#
# bpflowass_funding_dict = {0:'Any (Yes/No)', 1:'Yes', 2:'No'}

# leaveflowass_role_dict = {0:'Any', 1:'Professor Emeritus', 2:'Other (i.e. not Professor Emeritus)'}

leaveflowass_days_dict = {0:'Any', 1: '1 to less than 4 days', 2: '4 to less than 30 days', 3:'30 to less than 365 days', 4:'365 days and above'}
leaveflowass_ishead_dict = {0:'Any', 1:'Yes', 2:'No'}

# bpflowass_replacement_dict = {0:'Any (Yes/No)', 1:'Yes', 2:'No'}


# bpflowass_sg_dict = {0:'Any', 1:'SG 1 to 17', 2:'SG 18 to 33'}

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Leave Approval Flow Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Leave Approval Flow Assignments"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Leave Flow Assignment Criteria", id="leave_flowass_addnewbtn", color="primary",
                                   href='/settings/settings_leave_flow_assignment_profile?&mode=add'),  # block=True
                    ]),
                    # dbc.Col([
                    #     dbc.FormGroup(
                    #         [
                    #             dbc.Label("Search BP Approval Status", width=4,
                    #                       style={"text-align": "left"}),
                    #             dbc.Col([
                    #                 dbc.Input(
                    #                     type="text", id="bpflowass_searchinput", placeholder="Enter search string"
                    #                 ),
                    #
                    #             ],
                    #                 width=8
                    #             )
                    #         ],
                    #         row=True
                    #     ),
                    # ]),
                    #
                    # dbc.Row([
                    #     dbc.Col([
                    #         dbc.Button("Show All", color="primary",
                    #                    className="mr-1", id="bpflowass_showallbtn"),
                    #     ])
                    # ]),

                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.H4("Move priority from")),
                    dbc.Col(
                        dcc.Dropdown(
                        id="leave_flowass_priorityfrom",
                        options=[
                            # {'label': 'Any', 'value': '0'},
                            # {'label': 'Faculty', 'value': '1'},
                            # {'label': 'Administrative Personnel', 'value': '2'},
                            # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                            {'label': 0, 'value': 0},
                            {'label': 1, 'value': 1}

                        ],
                        value=0,
                        searchable=True
                        ),
                    ),
                    dbc.Col(html.H4("to")),
                    dbc.Col(
                        dcc.Dropdown(
                            id="leave_flowass_priorityto",
                            options=[
                                # {'label': 'Any', 'value': '0'},
                                # {'label': 'Faculty', 'value': '1'},
                                # {'label': 'Administrative Personnel', 'value': '2'},
                                # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                {'label': 0, 'value': 0},
                                {'label': 1, 'value': 1}

                            ],
                            value=0,
                            searchable=True
                        ),
                    ),
                    dbc.Col(
                        dbc.Button("Move Priority", color = "primary", id = 'leave_flowass_moveprioritybtn')

                    )


                ], className = "w-70"),


                html.Hr(),
                html.H4("Existing Leave Flow Assignment Criteria"),

                html.Div([

                ], id="leave_flowass_dt"),

                # dbc.Col([
                #
                #         html.Div([
                #             dcc.Input(id='unitsubmitstatus', type='text', value="0")
                #         ], style={'display': 'none'}),
                #         html.Div([
                #             dcc.Input(id='unitid', type='text', value="0")
                #         ], style={'display': 'none'}),
                #
                #         ], width=2
                #         )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('leave_flowass_dt', 'children'),
               Output('leave_flowass_priorityfrom', 'options'),
               Output('leave_flowass_priorityto', 'options')
               ],
              [
    Input('url', 'search'),
    Input('leave_flowass_moveprioritybtn', 'n_clicks')

],
    [
     State('leave_flowass_priorityfrom', 'value'),
     State('leave_flowass_priorityto', 'value')
],)
def leaveflowassignment_querymodulesfordtcall(url, leave_flowass_moveprioritybtn, leave_flowass_priorityfrom, leave_flowass_priorityto):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'leave_flowass_moveprioritybtn':

            sql5 = """
                    UPDATE leave_flow_assignment
                    SET leave_flow_assignment_priority_id = %s
                    WHERE leave_flow_assignment_priority_id = %s
                """

            values5 = [0, leave_flowass_priorityfrom]

            modifydatabase(sql5, values5)

            prior_list = []
            prior_list2 = []
            if leave_flowass_priorityfrom < leave_flowass_priorityto:
                for i in range(leave_flowass_priorityfrom+1, leave_flowass_priorityto+1):
                    prior_list.append(i)
                    prior_list2.append(i+500)
                sql2 = """
                        UPDATE leave_flow_assignment
                        SET leave_flow_assignment_priority_id = leave_flow_assignment_priority_id  - 1
                        WHERE leave_flow_assignment_priority_id IN %s
                    """
                values2 = (tuple(prior_list),)

                modifydatabase(sql2, values2)

            elif leave_flowass_priorityfrom > leave_flowass_priorityto:
                for i in range(leave_flowass_priorityto, leave_flowass_priorityfrom):
                    prior_list.append(i)
                    prior_list2.append(i+500)
                sql2 = """
                        UPDATE leave_flow_assignment
                        SET leave_flow_assignment_priority_id = leave_flow_assignment_priority_id + 1
                        WHERE leave_flow_assignment_priority_id IN %s
                    """
                values2 = (tuple(prior_list),)

                modifydatabase(sql2, values2)

            sql1 = """
                    UPDATE leave_flow_assignment
                    SET leave_flow_assignment_priority_id = %s
                    WHERE leave_flow_assignment_priority_id = %s
                """

            values1 = [leave_flowass_priorityto, 0]

            modifydatabase(sql1, values1)



    priorityoptions = commonmodules.queryfordropdown('''
        SELECT leave_flow_assignment_priority_id as value, leave_flow_assignment_priority_id as label
       FROM leave_flow_assignment
       WHERE leave_flow_assignment_delete_ind = %s
       ORDER BY leave_flow_assignment_priority_id
    ''', (False, ))


    sqlcommand = '''
                SELECT bfa.leave_flow_assignment_priority_id, leave_flow_assignment_id, leave_flow_assignment_leavetype_id, leave_flow_assignment_designation_id, leave_flow_assignment_emp_class_id, leave_flow_assignment_numdays, leave_flow_assignment_ishead_id,
                leave_flow_assignment_unit_id, leave_approval_flow_name
                FROM leave_flow_assignment bfa
                INNER JOIN leave_approval_flows baf ON baf.leave_approval_flow_id = bfa.leave_flow_assignment_flow_id
                WHERE leave_flow_assignment_delete_ind = %s
                ORDER BY bfa.leave_flow_assignment_priority_id ASC
                 '''


    values = [False]

    columns = ['bfa.leave_flow_assignment_priority_id', 'leave_flow_assignment_id', 'leave_flow_assignment_leavetype_id', 'leave_flow_assignment_designation_id', 'leave_flow_assignment_emp_class_id', 'leave_flow_assignment_numdays', 'leave_flow_assignment_ishead_id',
        'leave_flow_assignment_unit_id', 'leave_approval_flow_name']
    df = securequerydatafromdatabase(sqlcommand, values, columns)

    #leaveflowass_emptype_dict[None] = 'Any'
    empclass_labels = []
    for i in df['leave_flow_assignment_emp_class_id']:
        empclass_labels.append(leaveflowass_emptype_dict[i])
    # print('leave_empclass_labels', empclass_labels)

    #leaveflowass_days_dict[None] = 'Any'

    numdays_labels = []
    for i in df['leave_flow_assignment_numdays']:
        numdays_labels.append(leaveflowass_days_dict[i])

    leaveflowass_ishead_dict[0] = 'Any'
    leaveflowass_ishead_dict[None] = 'Any'
    ishead_labels = []
    for i in df['leave_flow_assignment_ishead_id']:
        ishead_labels.append(leaveflowass_ishead_dict[i])

    # print('leave_numdays_labels', numdays_labels)

    # appttype_labels = []
    # for i in df['bp_flow_assignment_appt_type_id']:
    #     appttype_labels.append(bpflowass_appttype_dict[i])
    #
    # numfail_labels = []
    # for i in df['bp_flow_assignment_numfail_id']:
    #     numfail_labels.append(bpflowass_numfail_dict[i])
    #
    # sg_labels = []
    # for i in df['bp_flow_assignment_sg_type_id']:
    #     sg_labels.append(bpflowass_sg_dict[i])

    # bpflowass_funding_dict[None] = 'Any (Yes/No)'

    # funding_labels = []
    # for i in df['bp_flow_assignment_is_ta_funding']:
    #     print(df['bp_flow_assignment_is_ta_funding'], 'bpflowass_funding_dict[i]')
    #     funding_labels.append(bpflowass_funding_dict[i])
    #
    # bpflowass_desig_dict[None] = 'Any'
    #
    # desig_labels = []
    # for i in df['bp_flow_assignment_desig_id']:
    #     desig_labels.append(bpflowass_desig_dict[i])
    #
    #
    # bpflowass_srempclass_dict[None] = 'Any'
    #
    # sr_emp_class_labels = []
    # for i in df['bp_flow_assignment_sr_emp_class_id']:
    #     sr_emp_class_labels.append(bpflowass_srempclass_dict[i])

    # bpflowass_replacement_dict[None] = 'Any (Yes/No)'
    #
    # replacement_labels = []
    # for i in df['bp_flow_assignment_with_replacement']:
    #     print(df['bp_flow_assignment_with_replacement'], 'bpflowass_replacement_dict[i]')
    #     replacement_labels.append(bpflowass_replacement_dict[i])


    sql1 = '''
                    SELECT unit_id, unit_name || ' (' || unit_code || ')'
                    FROM units
                    WHERE unit_is_active = %s
                    AND unit_delete_ind = %s

                '''

    values1 = (True, False)
    columns1 = ['unit_id', 'unit_name']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)

    leaveflowass_unit_dict = dict(df1.values)


    leaveflowass_unit_dict[0] = 'Any'
    leaveflowass_unit_dict[None] = 'Any'
    # bpflowass_unit_dict[nan] = 'Any'
    # unitoptions.insert(0, {'label': 'Any', 'value': 0})

    unit_labels = []
    for i in df['leave_flow_assignment_unit_id']:

        unit_labels.append(leaveflowass_unit_dict[i])



    ##
    sql2 = '''
                    SELECT designation_id, designation_name
                    FROM designations
                    WHERE designation_delete_ind = %s

                '''

    values2 = (False,)
    columns2 = ['designation_id', 'designation_name']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)

    leaveflowass_desig_dict = dict(df2.values)



    leaveflowass_desig_dict[0] = 'Any'
    leaveflowass_desig_dict[None] = 'Any'
    # bpflowass_unit_dict[nan] = 'Any'
    # unitoptions.insert(0, {'label': 'Any', 'value': 0})

    desig_labels = []
    for i in df['leave_flow_assignment_designation_id']:

        desig_labels.append(leaveflowass_desig_dict[i])



    ##
    sql3 = '''
                    SELECT leave_type_id, leave_type_name
                    FROM leave_types
                    WHERE leave_type_delete_ind = %s

                '''

    values3 = (False,)
    columns3 = ['leave_type_id', 'leave_type_name']
    df3 = securequerydatafromdatabase(sql3, values3, columns3)

    leaveflowass_leavetype_dict = dict(df3.values)



    leaveflowass_leavetype_dict[0] = 'Any'
    leaveflowass_leavetype_dict[None] = 'Any'
    # bpflowass_unit_dict[nan] = 'Any'
    # unitoptions.insert(0, {'label': 'Any', 'value': 0})

    leavetype_labels = []
    for i in df['leave_flow_assignment_leavetype_id']:

        leavetype_labels.append(leaveflowass_leavetype_dict[i])



    df['Leave Type'] = leavetype_labels
    df['Designation'] = desig_labels
    df['Leave Emp Class'] = empclass_labels
    df['Head of Unit/Sub-unit?'] = ishead_labels
    df['# of Days'] = numdays_labels


    # bpflowass_emptype_label = leaveflowass_emptype_dict
    # bpflowass_emptype_label = leaveflowass_days_dict
    #
    # # df['Appt Type'] = appttype_labels
    # # df['Number of Failing Marks'] = numfail_labels
    # # df['SG Type'] = sg_labels
    df['Unit'] = unit_labels


    # df['Under TA Funding?'] = funding_labels
    # df['Designation'] = desig_labels
    # df['SR Emp Class'] = sr_emp_class_labels
    # df['With replacement designation?'] = replacement_labels

    # bpflowass_emptype_label = bpflowass_emptype_dict
    # bpflowass_appttype_label = bpflowass_appttype_dict
    # bpflowass_numfail_label = bpflowass_numfail_dict
    # bpflowass_sg_label = bpflowass_sg_dict



    df.columns = ["Priority", "Leave Flow Assignment ID", "Leave Type1", "Designation1", "Leave Emp Class1", "Head of Unit/Sub-unit?1", "# of Days1", "Unit1", 'Approval Flow',
                  'Leave Type', 'Designation', 'Leave Emp Class', "Head of Unit/Sub-unit?", '# of Days', 'Unit']
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_leave_flow_assignment_profile?leave_flow_assignment_id='+str(row["Leave Flow Assignment ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)

    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Priority", "Leave Type", "Designation", "Leave Emp Class", "Head of Unit/Sub-unit?", "# of Days", "Unit", 'Approval Flow', 'Select']]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)




    return [table, priorityoptions, priorityoptions]


    # else:
    #     raise PreventUpdate
