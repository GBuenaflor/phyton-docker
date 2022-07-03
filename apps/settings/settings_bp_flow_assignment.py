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

bpflowass_emptype_dict = {0:"Any", 1: 'Faculty', 2: 'Administrative Personnel', 3:'Research and Extension Professional Staff (REPS)'}


# bpflowass_appttype_dict = {0: 'Any', 1: 'Additional Assignment - Original', 2:'Additional Assignment - Renewal', 3: 'Additional Assignment - Temporary',  12:'Original', 13:'Permanency/Tenure', 14:'Promotion', 15: 'Promotion - Automatic', 18:'Promotion - Merit', 19: 'Reappointment - MC 11, Cat II',
#                            20:'Reclassification', 21: 'Reemployement', 22: 'Renewal', 23: 'Renewal with Promotion', 27: 'Transfer - Lateral', 28: 'Transfer - With Promotion'}

bpflowass_numfail_dict = {0:'Any', 1:'0', 2:'At Least 1'}

bpflowass_sg_dict = {0:'Any', 1:'SG 1 to 17', 2:'SG 18 to 33'}

bpflowass_funding_dict = {0:'Any (Yes/No)', 1:'Yes', 2:'No'}

bpflowass_desig_dict = {0:'Any', 1:'Professor Emeritus', 3: 'Instructor/Lecturer', 2:'Other (i.e. not Prof Emeritus/Inst/Lec)', 4: 'Head Librarian'}

bpflowass_srempclass_dict = {0:'Any', 1: 'Faculty', 2: 'Administrative Personnel', 3:'Research and Extension Professional Staff (REPS)'}

# bpflowass_replacement_dict = {0:'Any (Yes/No)', 1:'Yes', 2:'No'}


# bpflowass_sg_dict = {0:'Any', 1:'SG 1 to 17', 2:'SG 18 to 33'}

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Basic Paper Approval Flow Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("BP Approval Flow Assignments"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New BP Flow Assignment Criteria", id="bpflowass_addnewbtn", color="primary",
                                   href='/settings/settings_bp_flow_assignment_profile?&mode=add'),  # block=True
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
                        id="bpflowass_priorityfrom",
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
                            id="bpflowass_priorityto",
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
                        dbc.Button("Move Priority", color = "primary", id = 'bpflowass_moveprioritybtn')

                    )


                ], className = "w-70"),


                html.Hr(),
                html.H4("Existing BP Flow Assignment Criteria"),

                html.Div([

                ], id="bpflowass_dt"),

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


@app.callback([Output('bpflowass_dt', 'children'),
               Output('bpflowass_priorityfrom', 'options'),
               Output('bpflowass_priorityto', 'options')
               ],
              [
    Input('url', 'search'),
    Input('bpflowass_moveprioritybtn', 'n_clicks')

],
    [
     State('bpflowass_priorityfrom', 'value'),
     State('bpflowass_priorityto', 'value')
],)
def querymodulesfordtcall(url, bpflowass_moveprioritybtn, bpflowass_priorityfrom, bpflowass_priorityto):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'bpflowass_moveprioritybtn':

            sql5 = """
                    UPDATE bp_flow_assignment
                    SET bp_flow_assignment_priority_id = %s
                    WHERE bp_flow_assignment_priority_id = %s
                """

            values5 = [0, bpflowass_priorityfrom]

            modifydatabase(sql5, values5)

            prior_list = []
            prior_list2 = []
            if bpflowass_priorityfrom < bpflowass_priorityto:
                for i in range(bpflowass_priorityfrom+1, bpflowass_priorityto+1):
                    prior_list.append(i)
                    prior_list2.append(i+500)
                sql2 = """
                        UPDATE bp_flow_assignment
                        SET bp_flow_assignment_priority_id = bp_flow_assignment_priority_id  - 1
                        WHERE bp_flow_assignment_priority_id IN %s
                    """
                values2 = (tuple(prior_list),)

                modifydatabase(sql2, values2)

            elif bpflowass_priorityfrom > bpflowass_priorityto:
                for i in range(bpflowass_priorityto, bpflowass_priorityfrom):
                    prior_list.append(i)
                    prior_list2.append(i+500)
                sql2 = """
                        UPDATE bp_flow_assignment
                        SET bp_flow_assignment_priority_id = bp_flow_assignment_priority_id + 1
                        WHERE bp_flow_assignment_priority_id IN %s
                    """
                values2 = (tuple(prior_list),)

                modifydatabase(sql2, values2)

            sql1 = """
                    UPDATE bp_flow_assignment
                    SET bp_flow_assignment_priority_id = %s
                    WHERE bp_flow_assignment_priority_id = %s
                """

            values1 = [bpflowass_priorityto, 0]

            modifydatabase(sql1, values1)



    priorityoptions = commonmodules.queryfordropdown('''
        SELECT bp_flow_assignment_priority_id as value, bp_flow_assignment_priority_id as label
       FROM bp_flow_assignment
       WHERE bp_flow_assignment_delete_ind = %s
       ORDER BY bp_flow_assignment_priority_id
    ''', (False, ))


    # sqlcommand = '''
    #             SELECT bfa.bp_flow_assignment_priority_id, bp_flow_assignment_id, bp_flow_assignment_emp_class_id, bp_flow_assignment_appt_type_id, bp_flow_assignment_numfail_id,
    #             bp_flow_assignment_sg_type_id, bfa.bp_flow_assignment_unit_id, bfa.bp_flow_assignment_is_ta_funding, bfa.bp_flow_assignment_desig_id, bfa.bp_flow_assignment_sr_emp_class_id, baf.approval_flow_name
    #             FROM bp_flow_assignment bfa
    #             INNER JOIN bp_approval_flows baf ON baf.approval_flow_id = bfa.bp_flow_assignment_flow_id
    #             WHERE bp_flow_assignment_delete_ind = %s
    #             ORDER BY bfa.bp_flow_assignment_priority_id ASC
    #              '''

    sqlcommand = '''
                SELECT bfa.bp_flow_assignment_priority_id, bp_flow_assignment_id, bp_flow_assignment_emp_class_id, bp_flow_assignment_appt_type_id, bp_flow_assignment_numfail_id,
                bp_flow_assignment_sg_type_id, bfa.bp_flow_assignment_unit_id, bfa.bp_flow_assignment_is_ta_funding, bfa.bp_flow_assignment_desig_id, bfa.bp_flow_assignment_sr_emp_class_id, baf.approval_flow_name
                FROM bp_flow_assignment bfa
                LEFT JOIN bp_approval_flows baf ON baf.approval_flow_id = bfa.bp_flow_assignment_flow_id
                WHERE bp_flow_assignment_delete_ind = %s
                ORDER BY bfa.bp_flow_assignment_priority_id ASC
                 '''


    values = [False]

    columns = ['bp_flow_assignment_priority_id', 'bp_flow_assignment_id', "bp_flow_assignment_emp_class_id", "bp_flow_assignment_appt_type_id", "bp_flow_assignment_numfail_id",
               'bp_flow_assignment_sg_type_id', 'bp_flow_assignment_unit_id', 'bp_flow_assignment_is_ta_funding', 'bp_flow_assignment_desig_id', 'bp_flow_assignment_sr_emp_class_id', 'approval_flow_name']
    df = securequerydatafromdatabase(sqlcommand, values, columns)


    empclass_labels = []
    for i in df['bp_flow_assignment_emp_class_id']:
        empclass_labels.append(bpflowass_emptype_dict[i])

    sqlappttype = '''
    SELECT appt_type_id, appt_type_name
    FROM appointment_types
    WHERE appt_type_is_active = %s
    AND appt_type_delete_ind = %s
    '''

    valuesappttype = (True, False)
    columnsappttype = ['appt_type_id', 'appt_type_name']
    df1 = securequerydatafromdatabase(sqlappttype, valuesappttype, columnsappttype)

    bpflowass_appttype_dict = dict(zip(df1.appt_type_id, df1.appt_type_name))
    bpflowass_appttype_dict[0] = 'Any'
    print('here3456', bpflowass_appttype_dict)
    appttype_labels = []
    for i in df['bp_flow_assignment_appt_type_id']:
        appttype_labels.append(bpflowass_appttype_dict[i])

    numfail_labels = []
    for i in df['bp_flow_assignment_numfail_id']:
        numfail_labels.append(bpflowass_numfail_dict[i])

    sg_labels = []
    for i in df['bp_flow_assignment_sg_type_id']:
        sg_labels.append(bpflowass_sg_dict[i])

    bpflowass_funding_dict[None] = 'Any (Yes/No)'

    funding_labels = []
    for i in df['bp_flow_assignment_is_ta_funding']:

        funding_labels.append(bpflowass_funding_dict[i])

    bpflowass_desig_dict[None] = 'Any'

    desig_labels = []
    for i in df['bp_flow_assignment_desig_id']:
        desig_labels.append(bpflowass_desig_dict[i])


    bpflowass_srempclass_dict[None] = 'Any'

    sr_emp_class_labels = []
    for i in df['bp_flow_assignment_sr_emp_class_id']:
        sr_emp_class_labels.append(bpflowass_srempclass_dict[i])

    # bpflowass_replacement_dict[None] = 'Any (Yes/No)'
    #
    # replacement_labels = []
    # for i in df['bp_flow_assignment_with_replacement']:
    #     print(df['bp_flow_assignment_with_replacement'], 'bpflowass_replacement_dict[i]')
    #     replacement_labels.append(bpflowass_replacement_dict[i])


    sql1 = '''
                    SELECT unit_id, unit_name
                    FROM units
                    WHERE unit_is_active = %s
                    AND unit_delete_ind = %s

                '''

    values1 = (True, False)
    columns1 = ['unit_id', 'unit_name']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)

    bpflowass_unit_dict = dict(df1.values)



    bpflowass_unit_dict[0] = 'Any'
    bpflowass_unit_dict[None] = 'Any'
    # bpflowass_unit_dict[nan] = 'Any'
    # unitoptions.insert(0, {'label': 'Any', 'value': 0})

    unit_labels = []
    for i in df['bp_flow_assignment_unit_id']:

        unit_labels.append(bpflowass_unit_dict[i])



    df['BP Emp Class'] = empclass_labels
    df['Appt Type'] = appttype_labels
    df['Number of Failing Marks'] = numfail_labels
    df['SG Type'] = sg_labels
    df['Unit'] = unit_labels
    df['Under TA Funding?'] = funding_labels
    df['Designation'] = desig_labels
    df['SR Emp Class'] = sr_emp_class_labels
    # df['With replacement designation?'] = replacement_labels

    # bpflowass_emptype_label = bpflowass_emptype_dict
    # bpflowass_appttype_label = bpflowass_appttype_dict
    # bpflowass_numfail_label = bpflowass_numfail_dict
    # bpflowass_sg_label = bpflowass_sg_dict



    df.columns = ["Priority", "BP Flow Assignment ID", "BP Emp Class1", "Appt Type1", "Number of Failing Marks1", 'SG Type1', 'Unit1','Under TA Funding?1','Designation1', 'SR Emp Class1', 'Approval Flow',
                  'BP Emp Class', 'Appt Type', 'Number of Failing Marks', 'SG Type', 'Unit', 'Under TA Funding?', 'Designation', 'SR Emp Class']
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_bp_flow_assignment_profile?bp_flow_assignment_id='+str(row["BP Flow Assignment ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Priority", "BP Emp Class", "Appt Type", "Number of Failing Marks", 'SG Type', 'Unit', 'Under TA Funding?', 'Designation', 'SR Emp Class', 'Approval Flow', 'Select']]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)



    return [table, priorityoptions, priorityoptions]


    # else:
    #     raise PreventUpdate
