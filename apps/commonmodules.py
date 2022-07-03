import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import math
import dash
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate
from apps.dbconnect import querydatafromdatabase, modifydatabase, modifydatabasereturnid
from apps.dbconnect import securequerydatafromdatabase
from dash.dependencies import Input, Output, State
from app import app
import base64
from datetime import datetime
import calendar
# import dash_admin_components as dac

image_filename = 'static/HRDO2.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    # "width":"20%",
    "padding": "2rem 1rem",
    "background-color": "#f3f3f3ff",
    "fontSize": "14px",
    "overflow": "auto"  # add
}

SIDEBAR_STYLE_Hidden = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "0",
    "display": "none"
}

bgstyle = {"background-color": "rgb(123,20,24)"}


# def returns3key():
#     return 'AKIA53RCOHU6U63EUUXG'
def returns3key():
    return 'AKIAYKNOPUIDFKNL57ER'

def returns3keyleaves():
    return 'AKIA2BNRE2NLOQ5BHLHV'

# def returns3secretkey():
#     return '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'

def returns3secretkey():
    return 'EyE5CS5+SrwnTVKm0Ki39jfB8iYBnOkywkCCN3IF'

def returns3secretkeyleaves():
    return '4hVMspnUWWjKw7TwweVxSzo9xnAm85dv2GOEB85X'

def getfirstflowstatus(bp_flow_id):
    sql1 = '''
            SELECT bp_status_id
            FROM bp_approval_flow_steps
            WHERE approval_flow_id = %s
            AND approval_flow_step_number = 1
            AND approval_flow_step_delete_ind = %s
        '''
    values1 = (bp_flow_id, False,)
    columns1 = ['bp_status_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    bp_status_id = int(df1["bp_status_id"][0])
    return bp_status_id

def leavegetfirstflowstatus(leave_approval_flow_id):
    sql1 = '''
                    SELECT leave_status_id
                    FROM leave_approval_flow_steps
                    WHERE leave_approval_flow_id = %s
                    AND leave_approval_flow_step_number = 1
                    AND leave_approval_flow_step_delete_ind = %s

                '''

    values1 = (leave_approval_flow_id, False,)
    columns1 = ['leave_status_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    leave_status_id = int(df1["leave_status_id"][0])

    return leave_status_id

def getbpflowid(bp_id):
    sql2 = ''' SELECT bp_approval_flow_id
                FROM basic_papers bp
                WHERE bp_id = %s
            '''
    values2 = (bp_id,)
    columns2 = ['bp_approval_flow_id']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)
    bp_approval_flow_id = int(df2["bp_approval_flow_id"][0])
    return bp_approval_flow_id

def getbpflowidnew1(bp_id):
    sql2 = ''' SELECT bp_approval_flow_new1_id
                FROM basic_papers bp
                WHERE bp_id = %s
            '''
    values2 = (bp_id,)
    columns2 = ['bp_approval_flow_new1_id']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)
    bp_approval_flow_id = int(df2["bp_approval_flow_new1_id"][0])

    return bp_approval_flow_id

def isflowsysmtemlevel(bp_flow_id):
    list_of_system_statuses = [18, 19]#put all system bp approval statuses here
    sql2 = '''
        SELECT bp_status_id
        FROM bp_approval_flow_steps
        WHERE approval_flow_id = %s
        AND approval_flow_step_delete_ind = %s
            '''
    values2 = (bp_flow_id, False)
    columns2 = ['bp_status_id']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)
    bp_status_id_list = df2['bp_status_id'].tolist()

    is_system = False
    for i in list_of_system_statuses:
        if i in bp_status_id_list:
            is_system = True
            break

    return is_system

def isflowdelegated(bp_flow_id):
    list_of_system_statuses = [32, 33]#put all delegated statuses here
    sql2 = '''
        SELECT bp_status_id
        FROM bp_approval_flow_steps
        WHERE approval_flow_id = %s
        AND approval_flow_step_delete_ind = %s
            '''
    values2 = (bp_flow_id, False)
    columns2 = ['bp_status_id']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)
    bp_status_id_list = df2['bp_status_id'].tolist()

    is_system = False
    for i in list_of_system_statuses:
        if i in bp_status_id_list:
            is_system = True
            break

    return is_system


def getbpflowidnew2(bp_id):
    sql2 = ''' SELECT bp_approval_flow_new2_id
                FROM basic_papers bp
                WHERE bp_id = %s
            '''
    values2 = (bp_id,)
    columns2 = ['bp_approval_flow_new2_id']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)
    bp_approval_flow_id = int(df2["bp_approval_flow_new2_id"][0])
    return bp_approval_flow_id

# def getrolestatuses(role_id):
#     sql0 = '''
#         SELECT bp_status_id
#         FROM bp_status_roles
#         WHERE role_id = %s
#         AND bp_status_role_delete_ind = %s
#
#     '''
#     columns0 = ['bp_status_id']
#     values0 = (user_role, False)
#     df0 = securequerydatafromdatabase(sql0, values0, columns0)

def lessthanequaltounit(listofunitids):
    overallunitlist = []
    for unit_id in listofunitids:

        sql = '''
                WITH RECURSIVE subordinates AS (
                    SELECT unit_id,	unit_parent_id,	unit_name
                    FROM units
                    WHERE unit_id = %s
                    UNION
                        SELECT e.unit_id,e.unit_parent_id,e.unit_name
                        FROM units e
                        INNER JOIN subordinates s ON s.unit_id = e.unit_parent_id
                ) SELECT * FROM subordinates
                '''
        values = (unit_id,)
        columns = ["unit_id", "unit_parent_id", "unit_name"]
        dfquery = securequerydatafromdatabase(sql, values, columns)

        x = dfquery['unit_id'].to_list()
        for i in x:
            overallunitlist.append(i)

    return overallunitlist

def ispersonexisting(firstname, middlename, lastname, extension, dob):
    has_dupli = False
    dupli_personid = 0
    duplisql = '''
                            SELECT person_last_name, person_first_name, person_middle_name, person_name_extension, person_dob, person_id
                            FROM persons
                            WHERE person_last_name = UPPER(%s)
                            AND person_delete_ind = %s
                        '''

    duplivalues = (lastname, False)
    duplicolumns = ['person_last_name', 'person_first_name', 'person_middle_name', 'person_name_extension',
                    'person_dob', 'person_id']

    duplidf = securequerydatafromdatabase(duplisql, duplivalues, duplicolumns)

    if duplidf.shape[0] > 0:
        duplidf['person_dob'] = duplidf['person_dob'].astype(str)
        # lastname_list = duplidf['person_last_name'].tolist()
        firstname_list = duplidf['person_first_name'].tolist()
        middlename_list = duplidf['person_middle_name'].tolist()
        suffix_list = duplidf['person_name_extension'].tolist()
        dob_list = duplidf['person_dob'].tolist()
        personid_list = duplidf['person_id'].tolist()

        for i in range(len(firstname_list)):
            if (str(firstname_list[i]).upper() == str(firstname).upper() and
                    str(middlename_list[i]).upper() == str(middlename).upper() and
                    str(suffix_list[i]).upper() == str(extension).upper() and
                    dob_list[i] == dob):
                dupli_personid = personid_list[i]

                has_dupli = True
                break

    return has_dupli, dupli_personid

def isleaveentryexisting(emp_id, leave_type_id, leave_start_date, leave_end_date):
    has_dupli_leave_emp_entry = False
    dupli_emp_id = 0
    duplisql = '''
                        SELECT emp_id, leave_type_id, leave_start_date, leave_end_date
                          FROM leave_employees
                         WHERE emp_id = %s
                           AND leave_type_id = %s
                           AND leave_start_date = %s
                           AND leave_end_date = %s
                           AND leave_emp_delete_ind = %s
                        '''

    duplivalues = (emp_id, leave_type_id, leave_start_date, leave_end_date, False)
    duplicolumns = ['emp_id', 'leave_type_id', 'leave_start_date', 'leave_end_date']
    duplidf = securequerydatafromdatabase(duplisql, duplivalues, duplicolumns)

    if duplidf.shape[0] > 0:
        duplidf['leave_end_date'] = duplidf['leave_start_date'].astype(str)
        duplidf['leave_end_date'] = duplidf['leave_end_date'].astype(str)
        emp_id_list = duplidf['emp_id'].tolist()
        leave_type_id_list = duplidf['leave_type_id'].tolist()
        leave_start_date_list = duplidf['leave_start_date'].tolist()
        leave_end_date_list = duplidf['leave_end_date'].tolist()

        # for i in range(len(firstname_list)):
        #     if (str(firstname_list[i]).upper() == str(firstname).upper() and
        #             str(middlename_list[i]).upper() == str(middlename).upper() and
        #             str(suffix_list[i]).upper() == str(extension).upper() and
        #             dob_list[i] == dob):
        #         dupli_emp_id = emp_id_list[i]
        #         has_dupli_leave_emp_entry = True
        #         break

    return has_dupli_leave_emp_entry, dupli_emp_id



def getcurrentbpstatus(bp_id):
    sql1 = '''
                SELECT bp_status_id
                  FROM bp_status_changes
                 WHERE bp_id = %s
                   AND bp_status_change_current_ind = %s
            '''

    values1 = (bp_id, True)
    columns1 = ['bp_status_id', 'bp_status_change_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    bp_status_id = int(df1["bp_status_id"][0])

    return bp_status_id

def setallstatuschangestofalse(bp_id):
    sql5 = """
                UPDATE bp_status_changes
                SET bp_status_change_current_ind = %s
                WHERE bp_id = %s
                """
    values5 = (False, bp_id)
    modifydatabase(sql5, values5)

def leavesetallstatuschangestofalse(leave_emp_id):
    sql5 = """
                UPDATE leave_status_changes
                SET leave_status_change_current_ind = %s
                WHERE leave_emp_id = %s
                """
    values5 = (False, leave_emp_id)
    modifydatabase(sql5, values5)

def getrolestatusesasdf(role_id):
    sql0 = '''
        SELECT bp_status_id
        FROM bp_status_roles
        WHERE role_id = %s
        AND bp_status_role_delete_ind = %s
    '''
    columns0 = ['bp_status_id']
    values0 = (role_id, False)
    df0 = securequerydatafromdatabase(sql0, values0, columns0)

    return df0

def getbpstatusofstepnumber(bp_approval_flow_id, approval_flow_step_number):
    sql4 = '''
                SELECT bp_status_id
                FROM bp_approval_flow_steps
                WHERE approval_flow_id = %s
                AND approval_flow_step_number = %s
                AND approval_flow_step_delete_ind = %s
            '''

    values4 = (bp_approval_flow_id, approval_flow_step_number, False)
    columns4 = ['bp_status_id']

    df4 = securequerydatafromdatabase(sql4, values4, columns4)
    bp_status_id_new = int(df4["bp_status_id"][0])

    return bp_status_id_new

def getflowstepnumber(bp_id):

    current_status = getcurrentbpstatus(bp_id)
    flowtype = getbpflowtype(bp_id)
    if flowtype == 1:
        flowid = getbpflowidnew1(bp_id)
    elif flowtype == 2:
        flowid = getbpflowidnew2(bp_id)
    else:
        flowid = getbpflowid(bp_id)

    sql4 = '''
            SELECT approval_flow_step_number
            FROM bp_approval_flow_steps
            WHERE approval_flow_id = %s
            AND bp_status_id = %s
            AND approval_flow_step_delete_ind = %s
            '''

    values4 = (flowid, current_status, False)
    columns4 = ['approval_flow_step_number']

    df4 = securequerydatafromdatabase(sql4, values4, columns4)
    step_no = int(df4["approval_flow_step_number"][0])

    return step_no


def fillinapproverofcurrentstatus(role_id, user_id, bp_id):
    sqlcommand12 = '''
                SELECT user_role_id
                FROM user_roles
                WHERE user_id = %s
                AND role_id = %s

                AND user_role_delete_ind = %s
    '''
    values12 = (user_id, role_id, False)
    columns12 = ['user_role_id']

    df12 = securequerydatafromdatabase(sqlcommand12, values12, columns12)
    user_role_id = int(df12["user_role_id"][0])


    sql55 = """
                UPDATE bp_status_changes
                SET bp_status_change_role_id = %s, bp_status_change_by = %s,
                bp_status_change_on = %s, bp_status_change_user_role_id = %s
                WHERE bp_id = %s
                AND bp_status_change_current_ind = %s
                """
    values55 = (role_id, user_id, datetime.now(), user_role_id, bp_id, True)
    modifydatabase(sql55, values55)

def getcurrentbpflowstepnumber(bp_approval_flow_id, bp_status_id):
    sql3 = '''
                SELECT approval_flow_step_number
                FROM bp_approval_flow_steps
                WHERE approval_flow_id = %s
                AND bp_status_id = %s
                AND approval_flow_step_delete_ind = %s
            '''
    values3 = (bp_approval_flow_id, bp_status_id, False)
    columns3 = ['approval_flow_step_number']


    df3 = securequerydatafromdatabase(sql3, values3, columns3)


    approval_flow_step_number = int(df3["approval_flow_step_number"][0])

    return approval_flow_step_number

def insertnewbpstatuschange(bp_id, bp_status_id):

    sql6 = """
            INSERT INTO bp_status_changes(bp_id, bp_status_id, bp_status_change_current_ind,
               bp_status_change_delete_ind)
            VALUES (%s, %s, %s, %s)
        """
    values6 = [bp_id, bp_status_id, True, False]
    modifydatabase(sql6, values6)

def getbpflowtype(bp_id):

    if bphasnewflow(bp_id):

        sql4 = '''
                SELECT bp_status_id
                FROM bp_approval_flow_steps
                WHERE approval_flow_id = %s
                AND approval_flow_step_delete_ind = %s
                '''
        values4 = (getbpflowidnew1(bp_id), False)
        columns4 = ['bp_status_id']
        df4 = securequerydatafromdatabase(sql4, values4, columns4)

        listofflow1statuses = df4['bp_status_id'].tolist()

        if getcurrentbpstatus(bp_id) in listofflow1statuses:
            flowtype = 1
        else:
            flowtype = 0

    else:
        flowtype = 0

    return flowtype


def bphasnewflow(bp_id):
    sql3 = '''
                SELECT bp_approval_flow_new1_id
                FROM basic_papers
                WHERE bp_id = %s
                AND bp_delete_ind = %s
                '''
    values3 = (bp_id, False)
    columns3 = ['bp_approval_flow_new1_id']
    df3 = securequerydatafromdatabase(sql3, values3, columns3)

    if not df3.empty and df3['bp_approval_flow_new1_id'][0] is not None:  # old flow is existing
        has_new_flow = True
    else:
        has_new_flow = False

    return has_new_flow

def approvebp(bp_id, user_id, user_role):
    currentflow = getbpflowtype(bp_id)

    if currentflow == 1:
        bp_approval_flow_id = getbpflowidnew1(bp_id)#Retrieve approval_flow_id of given bp
    elif currentflow == 2:
        bp_approval_flow_id = getbpflowidnew2(bp_id)#Retrieve approval_flow_id of given bp
    else:
        bp_approval_flow_id = getbpflowid(bp_id)  # Retrieve approval_flow_id of given bp
    df0 = getrolestatusesasdf(user_role)#Retrieve allowed bp_status approvals of current role
    bp_status_id = int(getcurrentbpstatus(bp_id))#Retrieve current bp_status of given bp
    if bp_status_id in df0["bp_status_id"].tolist():#if current bp status matches the status in bp_status roles, proceed. Otherwise, do not proceed with approval.
        # print('bp_status_id', bp_status_id, 'isbpinlaststep', isbpinlaststep)
        if bp_status_id in [27]: #In process
            bp_status_id_new = 6 #HRDO appt
        elif bp_status_id in [26, 32, 33] and isbpinlaststep(bp_id):#For BP/Appointment Paper Printing
            if isflowsysmtemlevel(bp_approval_flow_id):#if there is system level status in flow
                bp_status_id_new = 68 #For System Processing
            else:
                bp_status_id_new = 34 #For SR Entry Creation
        elif bp_status_id in [68]:#For System Processing
            bp_status_id_new = 34#For SR Entry Creation
        elif bp_status_id in [34]:#For System Processing
            bp_status_id_new = 69#For SR Entry Creation
        elif bp_status_id in [69]:#For Appt paper signing
            bp_status_id_new = 20#Processed
        elif bp_status_id in [21, '21'] or bp_status_id == 21:#For Requirement Fulfillment
            bp_status_id_new = getpreviousbpstatus(bp_id)
            setallstatuschangestofalse(bp_id)
            insertnewbpstatuschange(bp_id, 1)
        elif bp_status_id in [1]:#Draft
            bp_status_id_new = getfirstflowstatus(bp_approval_flow_id)
        elif bp_status_id in [22]:#For Reprocessing
            bp_status_id_new = getfirstflowstatus(bp_approval_flow_id)
            setallstatuschangestofalse(bp_id)
            insertnewbpstatuschange(bp_id, 1)
        elif isbpinlaststep(bp_id) and doesbphavenonterminalprinting(bp_id):
            bp_status_id_new = 34#For SR Entry Creation
        else:
            if isbpinlaststep(bp_id) and bphasnewflow(bp_id):
                bp_status_id_new = getfirstflowstatus(getbpflowidnew1(bp_id))
            elif (isbpinlaststep(bp_id) and getbpflowtype(bp_id) == 1) or (isbpinlaststep(bp_id) and not bphasnewflow(bp_id)):
                bp_status_id_new = 34#for SR entry creation
            else:# getbpflowtype(bp_id) == 0:
                flowtype = getbpflowtype(bp_id)
                if flowtype == 1:
                    flowid = getbpflowidnew1(bp_id)
                elif flowtype == 2:
                    flowid = getbpflowidnew2(bp_id)
                else:
                    flowid = getbpflowid(bp_id)
                approval_flow_step_number = getcurrentbpflowstepnumber(flowid, bp_status_id)# Retreive current flow step number of bp_status of given bp
                approval_flow_step_number_new = approval_flow_step_number + 1# Increment flow step number by 1, moving to the next step
                bp_status_id_new = getbpstatusofstepnumber(bp_approval_flow_id, approval_flow_step_number_new)# Retreive NEW bp_status_id of incremented step number


        fillinapproverofcurrentstatus(user_role, user_id, bp_id)# Set approver of previous step
        setallstatuschangestofalse(bp_id)# Set all other bp_statuses in bp_status_change table to FALSE
        insertnewbpstatuschange(bp_id, bp_status_id_new)# Insert new bp_status to bp_status_changes


def getcurrentbpstatus(bp_id):
    sql1 = '''
                    SELECT bp_status_id
                    FROM bp_status_changes
                    WHERE bp_id = %s
                    AND bp_status_change_current_ind = %s
                    AND bp_status_change_delete_ind = %s

                '''

    values1 = (bp_id, True, False)
    columns1 = ['bp_status_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    bp_status_id = int(df1["bp_status_id"][0])

    return bp_status_id

def getpreviousbpstatus(bp_id):
    sql1 = '''
            SELECT bp_status_id
            FROM bp_status_changes
            WHERE bp_id = %s
            AND bp_status_change_delete_ind = %s
            ORDER BY bp_status_change_id DESC

                '''

    values1 = (bp_id, False)
    columns1 = ['bp_status_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    bp_status_id = int(df1["bp_status_id"][1])
    if bp_status_id == 48:
        bp_status_id = int(df1["bp_status_id"][2])
    return bp_status_id

def getpreviousleavestatus(leave_emp_id):
    sql1 = '''
            SELECT leave_status_id
            FROM leave_status_changes
            WHERE leave_emp_id = %s
            AND leave_status_change_delete_ind = %s
            ORDER BY leave_status_change_id DESC

                '''

    values1 = (leave_emp_id, False)
    columns1 = ['leave_status_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    leave_status_id = int(df1["leave_status_id"][1])
    if leave_status_id == 21:
        leave_status_id = int(df1["leave_status_id"][2])
    return leave_status_id

def return_initial_bp_status(unit_approval_type, bp_approval_flow_id):
    initial_bp_status = 4
    if unit_approval_type == 1:
        dpc_to_cpc_dict = {
            1: 8,
            2: 9,
            3: 10,
            4: 11,
            5: 12,
            6: 13,
            7: 14,
            46:47,
            42:54,
            43:53,
            45:52,
            48:50,
            56:57,
            58: 59
        }
        if dpc_to_cpc_dict.get(bp_approval_flow_id) is not None:
            bp_approval_flow_id = dpc_to_cpc_dict[bp_approval_flow_id]

    initial_bp_status = getfirstflowstatus(bp_approval_flow_id)
    return initial_bp_status, bp_approval_flow_id


def checkiflengthzero(stringvar):
    isvalid = False
    isinvalid = False

    if stringvar:
        isvalid = True
        isinvalid = False
    else:
        isvalid = False
        isinvalid = True
    return isvalid, isinvalid


def checkiflengthx(stringvar, x):
    isvalid = False
    isinvalid = False

    if len(str(stringvar)) == x:
        isvalid = True
        isinvalid = False
    else:
        isvalid = False
        isinvalid = True
    return isvalid, isinvalid


def checkiflengthzero2(stringvar):
    isvalid = False

    if stringvar:
        isvalid = True

    else:
        isvalid = False

    return isvalid


def checkiflengthx2(stringvar, x):
    isvalid = False

    if len(str(stringvar)) == x:
        isvalid = True

    else:
        isvalid = False

    return isvalid


def safeupper(x):
    if type(x) == str:
        x = x.upper()

    return x


def checkstyle(isvalidcomponent):
    if isvalidcomponent:
        style = {"text-align": "left", 'color': 'red'}
    else:
        style = {"text-align": "left", 'color': 'black'}
    return style


def checkstyle2(isvalidcomponent):
    if isvalidcomponent:
        style = {"text-align": "left", 'color': 'black'}
    else:
        style = {"text-align": "left", 'color': 'red'}
    return style


def sendbackbp(bp_id, sendbackremarks, user_id, user_role):

    # Set all other bp_statuses in bp_status_change table to FALSE
    sql5 = """
                UPDATE bp_status_changes
                SET bp_status_change_current_ind = %s
                WHERE bp_id = %s
                """
    values5 = (False, bp_id)
    modifydatabase(sql5, values5)

    # Insert new bp_status to bp_status_changes

    sql6 = """
            INSERT INTO bp_status_changes(bp_id, bp_status_id, bp_status_change_current_ind, bp_status_change_by, bp_status_change_role_id,
                bp_status_change_on, bp_status_change_delete_ind, bp_status_change_remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

        """

    values6 = [bp_id, 21, True, user_id, user_role, datetime.now(), False, sendbackremarks]

    modifydatabase(sql6, values6)


def changebpstatuswremarks(bp_id, newbpstatus, sendbackremarks, user_id, user_role):
    sqlcommand12 = '''
                SELECT user_role_id
                FROM user_roles
                WHERE user_id = %s
                AND role_id = %s

                AND user_role_delete_ind = %s
    '''
    values12 = (user_id, user_role, False)
    columns12 = ['user_role_id']

    df12 = securequerydatafromdatabase(sqlcommand12, values12, columns12)
    user_role_id = int(df12["user_role_id"][0])


    # Set all other bp_statuses in bp_status_change table to FALSE
    sql5 = """
                UPDATE bp_status_changes
                SET bp_status_change_current_ind = %s
                WHERE bp_id = %s
                """
    values5 = (False, bp_id)
    modifydatabase(sql5, values5)

    # Insert new bp_status to bp_status_changes

    sql6 = """
            INSERT INTO bp_status_changes(bp_id, bp_status_id, bp_status_change_current_ind, bp_status_change_by, bp_status_change_role_id,
                bp_status_change_on, bp_status_change_delete_ind, bp_status_change_remarks, bp_status_change_user_role_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

        """

    values6 = [bp_id, newbpstatus, True, user_id, user_role, datetime.now(), False, sendbackremarks, user_role_id]

    modifydatabase(sql6, values6)


def changebpstatus(bp_id, newbpstatus, user_id, user_role):
    # Set all other bp_statuses in bp_status_change table to FALSE
    sql5 = """
                UPDATE bp_status_changes
                SET bp_status_change_current_ind = %s
                WHERE bp_id = %s
                """
    values5 = (False, bp_id)
    modifydatabase(sql5, values5)

    # Insert new bp_status to bp_status_changes

    sql6 = """
            INSERT INTO bp_status_changes(bp_id, bp_status_id, bp_status_change_current_ind, bp_status_change_by, bp_status_change_role_id,
                bp_status_change_on, bp_status_change_delete_ind)
            VALUES (%s, %s, %s, %s, %s, %s, %s)

        """

    values6 = [bp_id, newbpstatus, True, user_id, user_role, datetime.now(), False]

    modifydatabase(sql6, values6)

def changeleavestatus(leave_emp_id, newleavestatus, current_user_id, sessioncurrentrole, sessioncurrentunit):
    # Set all other bp_statuses in bp_status_change table to FALSE
    sql5 = """
                UPDATE leave_status_changes
                SET leave_status_change_current_ind = %s
                WHERE leave_emp_id = %s
                """
    values5 = (False, leave_emp_id)
    modifydatabase(sql5, values5)

    # Insert new bp_status to bp_status_changes

    sqluserrole = '''SELECT user_role_id from user_roles
        WHERE user_id = %s
        AND role_id = %s
        AND user_role_unit_id = %s
        AND user_role_delete_ind = %s'''

    valuesuserrole = [current_user_id, sessioncurrentrole,sessioncurrentunit, False]
    columnsuserrole = ['user_role_id']
    dfuserrole = securequerydatafromdatabase(sqluserrole, valuesuserrole, columnsuserrole)
    leaves_user_role_id = str(dfuserrole["user_role_id"][0])

    sql6 = """
            INSERT INTO leave_status_changes(leave_emp_id, leave_status_id, leave_status_change_current_ind, leave_status_change_by, leave_status_change_user_role_id,
                leave_status_change_on, leave_status_change_delete_ind)
            VALUES (%s, %s, %s, %s, %s, %s, %s)

        """

    values6 = [leave_emp_id, newleavestatus, True, current_user_id, leaves_user_role_id, datetime.now(), False]

    modifydatabase(sql6, values6)

def get_header():
    header = html.Div([])
    # header = html.Div(["test"], style={"width": "100%", "height": "10rem", "background-color": "#f3f3f3ff",    "top": 0,"left": 0,"right": 0,  })

    #     html.Div([
    #
    #     ], className="twelve columns padded"),
    #
    # ], className="row gs-header gs-text-header", style={'margin':"10px"})
    return header


def get_menu():
    menu = html.Div([

        html.Div(  # sidebar
            [
                dbc.Row(
                    [
                        html.Img(
                            src='data:image/png;base64,{}'.format(encoded_image.decode()), height="160px", width="230px"),
                        html.Br(),
                        # dbc.FormGroup(dbc.FormText("version 1.1"), style={
                        #     "textAlign": "center", "vertical-align": "bottom"}),
                    ], justify="center", align="center",
                    # className="mb-4"
                ),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='ddroledropdown',

                            searchable=False,
                            clearable=False,
                            optionHeight=40,
                            # style={'white-space': 'nowrap'}
                        ),
                    ],
                        style={'display': 'inline-block', 'width': '100%'},
                        id='divdroledropdown'
                    ),
                ]),
                # html.Div([
                #     html.Div([],
                #              style={'display': 'inline-block', 'width': '100%'},
                #              id='divcurrentrole'
                #              ),
                # ]),
                html.Div([
                    html.Div([
                    ], id="current_role_name", style={'display': 'inline-block', 'width': '100%'}),  # , 'font-size': '.75vw'
                ],
                    style={'display': 'inline-block', 'width': '100%'},
                    id='divrolename'
                ),
                html.Div([
                    html.Div([
                    ], id="current_unit_name", style={'display': 'inline-block', 'width': '100%'}),  # , 'font-size': '.75vw'
                ]),
                html.Hr(),
                html.Div([
                    html.Div([
                       dbc.DropdownMenu(
                            [


                                dbc.DropdownMenuItem(
                                    "BULSA", href="https://bulsa.upd.edu.ph"
                                ),

                            ],
                            label="Switch System",
                        ),
                        ],
                        style={'display': 'inline-block', 'width': '100%'},
                        id=''
                    ),
                ]),

                # html.I(className='fas fa-home'),
                #
                # html.Div([
                #     dbc.Nav(
                #         [
                #             dbc.NavItem(dbc.NavLink(html.Div([html.I(className='fas fa-home'), " Active" ]), href="#")),
                #             dbc.NavItem(dbc.NavLink(html.Div(["A link ",html.I(className='fas fa-home')]), href="#")),
                #
                #         ], id="test2"
                #     ),
                # ], id="test"),
                #
                # dbc.Button("Add Service Record Entry", color="primary", className="mr-1",
                #         id="test3"),
                html.Div([


                    html.Hr(),
                    html.Div([
                        dbc.Input(
                            type="text", id="module_search", placeholder="Search Module Name", value="",
                            # style={'font-size': '.85vw'}
                        ),
                    ], style={'display': 'inline-block', 'width': '100%'}),
                    html.Hr(),
                    html.Div([
                    ], id="menudiv", style={'width': '100%'}),  # 'textalign': 'left', 'color': 'black',
                    html.Div([
                        dcc.Input(id='menuload', type='text', value="0")
                    ], style={'display': 'none'}),

                    html.Hr(),
                ], id="usermenu", style={'display': 'inline'}),
            ],
            id="sidebar", style=SIDEBAR_STYLE,
        ),
        # dac.Navbar(color = "white",
        # 			text="I can write text in the navbar!",
        # 			),
        # dac.Sidebar(
        # 	dac.SidebarMenu(
        # 		[
        # 			dac.SidebarHeader(children="Cards"),
        # 			dac.SidebarMenuItem(id='tab_cards', label='Basic cards', icon='box'),
        # 			dac.SidebarMenuItem(id='tab_social_cards', label='Social cards', icon='id-card'),
        # 			dac.SidebarMenuItem(id='tab_tab_cards', label='Tab cards', icon='image'),
        # 			dac.SidebarHeader(children="Boxes"),
        # 			dac.SidebarMenuItem(id='tab_basic_boxes', label='Basic boxes', icon='desktop'),
        # 			dac.SidebarMenuItem(id='tab_value_boxes', label='Value/Info boxes', icon='suitcase')
        # 		]
        # 	),
        # 	title='Dash Admin',
        # 	skin="light",
        # 	color="primary",
        # 	brand_color="primary",
        # 	url="https://quantee.ai",
        # 	src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
        # 	elevation=3,
        # 	opacity=0.8
        # )
    ],)

    return menu


def get_common_variables():
    menu = html.Div([

        dcc.Store(id='current_page',  storage_type='session'),
        dcc.Store(id='store1', storage_type='session'),

        dcc.Store(id='menudict', storage_type='session'),
        dcc.Store(id='user_id', storage_type='session'),
        dcc.Store(id='sessionddroledropdown', storage_type='session'),

        dcc.Store(id='sessionroleunits', storage_type='session'),
        dcc.Store(id='sessioncurrentunit', storage_type='session'),
        dcc.Store(id='sessionroleaccessunits', storage_type='session'),

        dcc.Store(id='sessioncurrentuserroleid', storage_type='session'),


    ], style={'display': 'none'})
    return menu


def get_settings_menu():
    menu = html.Div(html.Div([
        # dcc.Link('Home   ', href='/', className="p-2 text-dark"),
        dcc.Link('Users   ', href='/settings/settings_users', className="p-2 text-dark"),
        dcc.Link('Banks    ', href='/settings/settings_banks', className="p-2 text-dark"),
        dcc.Link('Keywords    ', href='/settings/settings_keywords', className="p-2 text-dark"),
    ], className="d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom shadow-sm"),)

    return menu


@app.callback(
    [
        Output('ddroledropdown', 'options'),
        Output('ddroledropdown', 'value'),
        Output('sessionupdaterole', 'data'),
        # Output('divcurrentrole', 'children'),
    ],
    [
        # Input('sessiondefaultrole', 'modified_timestamp'),
        # Input('sessioncurrentrole', 'modified_timestamp'),
        Input('sessionlogout', 'modified_timestamp'),
    ],
    [

        State('sessiondefaultrole', 'data'),
        State('sessioncurrentrole', 'data'),
        State('sessionddroledropdown', 'data'),
        State('ddroledropdown', 'options'),
        State('ddroledropdown', 'value'),
    ],)
def updaterole(sessionlogout, current, selected, sessionddroledropdown, ddroledropdown, currentlyselected):  # pathname
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == "sessionlogout":
            return [[], [], [], ]
    if current and not selected and not currentlyselected:
        return [sessionddroledropdown, current, current, ]
    else:
        return [sessionddroledropdown, selected, current, ]


# for hiding HOME
@app.callback(
    [
        Output('divdroledropdown', 'style'),
        Output('divrolename', 'style'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
    ],)
def hidehome(pathname):
    if pathname == "/home":
        return [{'display': 'inline-block', 'width': '100%'}, {'display': 'none'}]
    else:
        return [{'display': 'none'}, {'display': 'inline-block', 'width': '100%'}]


@app.callback([Output('menudiv', 'children'),

               Output('sessioncurrentrole', 'data'),
               Output('current_unit_name', 'children'),
               Output('sessioncurrentunit', 'data'),
               Output('current_role_name', 'children'),
               Output('sessioncurrentuserroleid', 'data')
               # Output('listofallowedunits', 'data') #added
               ],
              [
    Input('ddroledropdown', 'value'),
    Input('module_search', 'value')
],
    [
    State('menudiv', 'children'),
    State('current_user_id', 'data'),
    State('sessionmenudict', 'data'),
    State('sessionddroledropdown', 'data'),
    State('sessiondefaultrole', 'data'),
    State('sessioncurrentrole', 'data'),
    State('sessionroleunits', 'data'),
    State('current_unit_name', 'children'),
    State('current_role_name', 'children'),
    State('sessioncurrentunit', 'data'),
    State('url', 'pathname'),
    State('sessionlistofunits', 'data'),
    State('current_module', 'data'),
    State('sessionroleaccessunits', 'data'),
    State('sessioncurrentuserroleid', 'data')
],)
def menuprocesses(ddroledropdown, module_search, menubtns, current_user_id, menudict, sessionddroledropdown,
                  sessiondefaultrole, sessioncurrentrole, sessionroleunits, current_unit_name, current_role_name,
                  sessioncurrentunit, url, sessionlistofunits, current_module, sessionroleaccessunits,
                  sessioncurrentuserroleid):
    menudiv = []
    ctx = dash.callback_context

    sessioncurrentrolename = ''
    # if sessioncurrentrole is not None:

    # try:
    #     sessioncurrentrolename = df['role_name'][0]
    # except:
    #     sessioncurrentrolename = ''

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'ddroledropdown':
            listofunits = list(
                filter(lambda sessionroleaccessunits: sessionroleaccessunits['role_id'] == ddroledropdown, sessionroleaccessunits))
            listofunits_home = list(
                filter(lambda sessionroleunits: sessionroleunits['role_id'] == ddroledropdown, sessionroleunits))
            if listofunits:
                unitrole = listofunits[0]
                unitrole_home = listofunits_home[0]
            else:
                unitrole = list(filter(
                    lambda sessionroleaccessunits: sessionroleaccessunits['role_id'] == sessiondefaultrole, sessionroleaccessunits))[0]
                unitrole_home = list(filter(
                    lambda sessionroleunits: sessionroleunits['role_id'] == sessiondefaultrole, sessionroleunits))[0]

            if current_user_id != -1:
                menudict = pd.DataFrame.from_dict(menudict)
                menudict = menudict[['role_id', 'module_name',
                                     'module_header', 'module_link', 'module_is_report', 'module_icon']]
                menuitems = convertdftomenu(menudict, ddroledropdown, url, current_module)
                unitrolename = unitrole_home['unit_name']
                current_role_id = unitrole_home['role_id']
                sql = '''
                    SELECT role_id, role_name
                      FROM roles
                     WHERE role_delete_ind = %s
                       AND role_id = %s
                '''
                values = (False, current_role_id)
                columns = ['role_id', 'role_name']
                df = securequerydatafromdatabase(sql, values, columns)
                rolename = df['role_name'][0]
                # rolename = list(filter(
                #     lambda sessionroleunits: sessionroleunits['role_id'] == sessiondefaultrole, sessionroleunits))[0]
                unit_id = unitrole['unit_id']

                #for storing sessioncurrentuserroleid
                sqluserrole = '''
                    SELECT user_role_id
                      FROM user_roles
                     WHERE user_role_delete_ind = %s
                        AND user_role_active_ind = %s
                        AND user_id = %s
                        AND role_id = %s
                '''
                valuesuserrole = (False, True, current_user_id, current_role_id)
                columnsuserrole = ['user_role_id']
                dfuserrole = securequerydatafromdatabase(sqluserrole, valuesuserrole, columnsuserrole)

                current_user_role_id = dfuserrole['user_role_id'][0]
                # print('printing current_user_role_id, ', current_user_role_id)


                return [menuitems, ddroledropdown, unitrolename, unit_id, rolename, current_user_role_id]
            else:
                raise PreventUpdate
        # elif eventid == 'module_search':
        elif module_search:
            # print('printing module_search, ', module_search)
            # raise PreventUpdate
            module_search_input = "%"+module_search+"%"
            sqlcommand = '''SELECT user_id, r.role_id, role_name, module_name, module_header, module_link, ur.user_role_default, u.unit_name, u.unit_id,
                            m.module_is_report, m.module_icon, m.module_is_open, un.unit_name, un.unit_id
            FROM user_roles ur INNER JOIN roles r on r.role_id = ur.role_id
            INNER JOIN module_roles mr ON r.role_id = mr.role_id
            INNER JOIN modules m on m.module_id= mr.module_id
            INNER JOIN units u on u.unit_id = ur.user_role_access_level_unit_id
            INNER JOIN units un on un.unit_id = ur.user_role_unit_id
            WHERE module_delete_ind = %s
            AND module_name ILIKE %s
            AND user_id=%s
            AND user_role_delete_ind = %s
            AND user_role_active_ind = %s
            ORDER BY role_name, m.module_header, m.module_name

            '''
            values = (False, module_search_input, str(current_user_id), False, True)
            columns = ["user_id", "role_id", "role_name", "module_name", "module_header",
                       "module_link", "user_role_default", "unit_name", "unit_id", 'module_is_report',
                       'module_icon', 'module_is_open', 'home_unit_name', 'home_unit_id']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            dfdict = df.copy()
            dfdict = dfdict.to_dict('list')

            listofunits = list(
                filter(lambda sessionroleaccessunits: sessionroleaccessunits['role_id'] == ddroledropdown, sessionroleaccessunits))
            listofunits_home = list(
                filter(lambda sessionroleunits: sessionroleunits['role_id'] == ddroledropdown, sessionroleunits))
            if listofunits:
                unitrole = listofunits[0]
                unitrole_home = listofunits_home[0]
            else:
                unitrole = list(filter(
                    lambda sessionroleaccessunits: sessionroleaccessunits['role_id'] == sessiondefaultrole, sessionroleaccessunits))[0]
                unitrole_home = list(filter(
                    lambda sessionroleunits: sessionroleunits['role_id'] == sessiondefaultrole, sessionroleunits))[0]

            menudict = dfdict
            menudict = pd.DataFrame.from_dict(menudict)
            menudict = menudict[['role_id', 'module_name',
                                 'module_header', 'module_link', 'module_is_report', 'module_icon']]
            menuitems = convertdftomenu(menudict, ddroledropdown, url, current_module)
            unitrolename = unitrole_home['unit_name']
            current_role_id = unitrole_home['role_id']
            sql = '''
                SELECT role_id, role_name
                  FROM roles
                 WHERE role_delete_ind = %s
                   AND role_id = %s
            '''
            values = (False, current_role_id)
            columns = ['role_id', 'role_name']
            df = securequerydatafromdatabase(sql, values, columns)
            rolename = df['role_name'][0]
            unit_id = unitrole['unit_id']
            #for storing sessioncurrentuserroleid
            sqluserrole = '''
                SELECT user_role_id
                  FROM user_roles
                 WHERE user_role_delete_ind = %s
                    AND user_role_active_ind = %s
                    AND user_id = %s
                    AND role_id = %s
            '''
            valuesuserrole = (False, True, current_user_id, current_role_id)
            columnsuserrole = ['user_role_id']
            dfuserrole = securequerydatafromdatabase(sqluserrole, valuesuserrole, columnsuserrole)
            current_user_role_id = dfuserrole['user_role_id'][0]

            # if not module_search:
            #     if current_user_id != -1:
            #         menudict = pd.DataFrame.from_dict(menudict)
            #         menudict = menudict[['role_id', 'module_name',
            #                              'module_header', 'module_link', 'module_is_report', 'module_icon']]
            #         # menudict=menudict[['module_name','module_header','module_link']]
            #         menuitems = convertdftomenu(menudict, ddroledropdown, url, current_module)
            #         # sessioncurrentunit
            #         # + ", " + sessioncurrentrole
            #         return [menuitems, ddroledropdown, current_unit_name, sessioncurrentunit, current_role_name, current_user_role_id]
            #     else:
            #         raise PreventUpdate
            # elif module_search:
            #     if current_user_id != -1:
            #
            #         menudict = pd.DataFrame.from_dict(menudict)  # ,ddroledropdown)
            #         menudict = menudict[['role_id', 'module_name',
            #                              'module_header', 'module_link', 'module_is_report', 'module_icon']]
            #         # menudict['module_name_low'] = menudict['module_name'].str.lower()
            #         # menudict = menudict[menudict['module_name_low'].str.contains(module_search.lower())].copy()
            #         menuitems = convertdftomenu(menudict, ddroledropdown, url, current_module)
            #
            #         # sessioncurrentunit
            #         # + ", " + sessioncurrentrole
            #         return [menuitems, ddroledropdown, current_unit_name, sessioncurrentunit, current_role_name, current_user_role_id]
            #     else:
            #         raise PreventUpdate
            return [menuitems, ddroledropdown, current_unit_name, sessioncurrentunit, current_role_name, current_user_role_id]
        else:
            # raise PreventUpdate
            listofunits = list(
                filter(lambda sessionroleaccessunits: sessionroleaccessunits['role_id'] == ddroledropdown, sessionroleaccessunits))
            listofunits_home = list(
                filter(lambda sessionroleunits: sessionroleunits['role_id'] == ddroledropdown, sessionroleunits))
            if listofunits:
                unitrole = listofunits[0]
                unitrole_home = listofunits_home[0]
            else:
                unitrole = list(filter(
                    lambda sessionroleaccessunits: sessionroleaccessunits['role_id'] == sessiondefaultrole, sessionroleaccessunits))[0]
                unitrole_home = list(filter(
                    lambda sessionroleunits: sessionroleunits['role_id'] == sessiondefaultrole, sessionroleunits))[0]

            menudict = pd.DataFrame.from_dict(menudict)
            menudict = menudict[['role_id', 'module_name',
                                 'module_header', 'module_link', 'module_is_report', 'module_icon']]
            menuitems = convertdftomenu(menudict, ddroledropdown, url, current_module)
            unitrolename = unitrole_home['unit_name']
            current_role_id = unitrole_home['role_id']
            sql = '''
                SELECT role_id, role_name
                  FROM roles
                 WHERE role_delete_ind = %s
                   AND role_id = %s
            '''
            values = (False, current_role_id)
            columns = ['role_id', 'role_name']
            df = securequerydatafromdatabase(sql, values, columns)
            rolename = df['role_name'][0]
            unit_id = unitrole['unit_id']
            #for storing sessioncurrentuserroleid
            sqluserrole = '''
                SELECT user_role_id
                  FROM user_roles
                 WHERE user_role_delete_ind = %s
                    AND user_role_active_ind = %s
                    AND user_id = %s
                    AND role_id = %s
            '''
            valuesuserrole = (False, True, current_user_id, current_role_id)
            columnsuserrole = ['user_role_id']
            dfuserrole = securequerydatafromdatabase(sqluserrole, valuesuserrole, columnsuserrole)
            current_user_role_id = dfuserrole['user_role_id'][0]

            if current_user_id != -1:

                menudict = pd.DataFrame.from_dict(menudict)  # ,ddroledropdown)
                menudict = menudict[['role_id', 'module_name',
                                     'module_header', 'module_link', 'module_is_report', 'module_icon']]
                menudict['module_name_low'] = menudict['module_name'].str.lower()
                menudict = menudict[menudict['module_name_low'].str.contains(module_search.lower())].copy()
                menuitems = convertdftomenu(menudict, ddroledropdown, url, current_module)

                # sessioncurrentunit
                # + ", " + sessioncurrentrole
                return [menuitems, ddroledropdown, current_unit_name, sessioncurrentunit, current_role_name, current_user_role_id]
            else:
                raise PreventUpdate
    else:
        raise PreventUpdate

#
# def convertdftomenu(df, selectedrole, url, current_module):
#     menudiv = []
#
#     df = df[df["role_id"] == selectedrole]
#     currentmodule = "Home"
#     dffiltered = df[df["role_id"] == selectedrole]
#     dffiltered = dffiltered[dffiltered["module_header"] == currentmodule]
#     menudiv.append({'props': {'children': currentmodule},
#                     'type': 'H5', 'namespace': 'dash_html_components'})
#     currentmenu = []
#     for index, row in dffiltered.iterrows():
#         if current_module == row["module_name"]:
#             tempmenu = {'props':
#                         {'children':
#                             {'props':
#                                 {'children': row["module_name"] , 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px', 'backgroundColor': 'rgb(128,0,0)', 'color': 'white'}},  # 'backgroundcolor':'red'
#                              'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
#                          }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
#         else:
#             tempmenu = {'props':
#                         {'children':
#                             {'props': {'children': row["module_name"], 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px'}},
#                              'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
#                          }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
#         currentmenu.append(tempmenu)
#         menudiv.append({'props':
#                         {'children': currentmenu,
#                          'vertical': 'xs', 'pills': True, 'style': {'margin': '0px', 'padding': '0px', 'display': 'inline', 'font-size': '14px'}},
#                         'type': 'Nav',
#                         'namespace': 'dash_bootstrap_components'})
#         currentmenu = []
#     #
#     for currentmodule in df.module_header.unique():
#         if currentmodule != "Home":
#             dffiltered = df[df["role_id"] == selectedrole]
#             dffiltered = dffiltered[dffiltered["module_header"] == currentmodule]
#             menudiv.append({'props': {'children': currentmodule},
#                             'type': 'H5', 'namespace': 'dash_html_components'})
#             currentmenu = []
#             for index, row in dffiltered.iterrows():
#                 if current_module == row["module_name"]:
#                     tempmenu = {'props':
#                                 {'children':
#                                     {'props': {'children': row["module_name"], 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px', 'backgroundColor': 'rgb(128,0,0)', 'color': 'white'}},  # 'backgroundcolor':'red'
#                                      'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
#                                  }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
#                 else:
#                     tempmenu = {'props':
#                                 {'children':
#                                     {'props': {'children': row["module_name"], 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px'}},
#                                      'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
#                                  }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
#                 if not row["module_is_report"]:
#                     currentmenu.append(tempmenu)
#             menudiv.append({'props':
#                             {'children': currentmenu,
#                              'vertical': 'xs', 'pills': True, 'style': {'margin': '0px', 'padding': '0px', 'display': 'inline', 'font-size': '14px'}},
#                             'type': 'Nav',
#                             'namespace': 'dash_bootstrap_components'})
#             currentmenu = []
#     return menudiv


def convertdftomenu(df, selectedrole, url, current_module):
    menudiv = []

    df = df[df["role_id"] == selectedrole]
    currentmodule = "Home"
    dffiltered = df[df["role_id"] == selectedrole]
    dffiltered = dffiltered[dffiltered["module_header"] == currentmodule]
    menudiv.append({'props': {'children': currentmodule},
                    'type': 'H5', 'namespace': 'dash_html_components'})
    currentmenu = []
    for index, row in dffiltered.iterrows():
        if current_module == row["module_name"]:
            if row["module_icon"]:
                module_icon = row["module_icon"]
            else:
                module_icon = 'fas fa-briefcase'
            tempmenu = {'props': {'children':
                                  {'props': {'children':
                                             {'props': {'children':
                                                        [{'props': {'children': None, 'className': module_icon}, 'type': 'I', 'namespace': 'dash_html_components'}, ' '+row["module_name"]]},
                                              'type': 'Div', 'namespace': 'dash_html_components'}, 'href': row["module_link"], 'style': {'margin': '5px', 'padding': '5px', 'backgroundColor': 'rgb(128,0,0)', 'color': 'white'}},
                                   'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}},
                        'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}

            #
            # {'props':
            #             {'children':
            #                 {'props':
            #                     {'children': row["module_name"] , 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px', 'backgroundColor': 'rgb(128,0,0)', 'color': 'white'}},  # 'backgroundcolor':'red'
            #                  'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
            #              }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
        else:
            if row["module_icon"]:
                module_icon = row["module_icon"]
            else:
                module_icon = 'fas fa-briefcase'
            tempmenu = {'props': {'children':
                                  {'props': {'children':
                                             {'props': {'children':
                                                        [{'props': {'children': None, 'className': module_icon}, 'type': 'I', 'namespace': 'dash_html_components'}, ' '+row["module_name"]]},
                                              'type': 'Div', 'namespace': 'dash_html_components'}, 'href': row["module_link"], 'style': {'margin': '5px', 'padding': '5px'}},
                                   'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}},
                        'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
            # {'props':
            #             {'children':
            #                 {'props': {'children': row["module_name"], 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px'}},
            #                  'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
            #              }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
        currentmenu.append(tempmenu)
        menudiv.append({'props':
                        {'children': currentmenu,
                         'vertical': 'xs', 'pills': True, 'style': {'margin': '0px', 'padding': '0px', 'display': 'inline', 'font-size': '14px'}},
                        'type': 'Nav',
                        'namespace': 'dash_bootstrap_components'})
        currentmenu = []
    #
    for currentmodule in df.module_header.unique():
        if currentmodule != "Home":
            dffiltered = df[df["role_id"] == selectedrole]
            dffiltered = dffiltered[dffiltered["module_header"] == currentmodule]
            if "Home" in df.module_header.unique():
                menudiv.append({'props': {'children': currentmodule},
                                'type': 'H5', 'namespace': 'dash_html_components'})
            currentmenu = []
            for index, row in dffiltered.iterrows():
                if current_module == row["module_name"]:
                    if row["module_icon"]:
                        module_icon = row["module_icon"]
                    else:
                        module_icon = 'fas fa-briefcase'
                    tempmenu = {'props': {'children':
                                          {'props': {'children':
                                                     {'props': {'children':
                                                                [{'props': {'children': None, 'className': module_icon}, 'type': 'I', 'namespace': 'dash_html_components'}, ' '+row["module_name"]]},
                                                      'type': 'Div', 'namespace': 'dash_html_components'}, 'href': row["module_link"], 'style': {'margin': '5px', 'padding': '5px', 'backgroundColor': 'rgb(128,0,0)', 'color': 'white'}},
                                           'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}},
                                'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
                    # {'props':
                    #            {'children':
                    #                {'props': {'children': row["module_name"], 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px', 'backgroundColor': 'rgb(128,0,0)', 'color': 'white'}},  # 'backgroundcolor':'red'
                    #                 'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
                    #             }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
                else:
                    if row["module_icon"]:
                        module_icon = row["module_icon"]
                    else:
                        module_icon = 'fas fa-briefcase'
                    tempmenu = {'props': {'children':
                                          {'props': {'children':
                                                     {'props': {'children':
                                                                [{'props': {'children': None, 'className': module_icon}, 'type': 'I', 'namespace': 'dash_html_components'}, ' '+row["module_name"]]},
                                                      'type': 'Div', 'namespace': 'dash_html_components'}, 'href': row["module_link"], 'style': {'margin': '5px', 'padding': '5px'}},
                                           'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}},
                                'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
                    # {'props':
                    #            {'children':
                    #                {'props': {'children': row["module_name"], 'href': row["module_link"], 'disabled': False, 'style': {'margin': '5px', 'padding': '5px'}},
                    #                 'type': 'NavLink', 'namespace': 'dash_bootstrap_components'}
                    #             }, 'type': 'NavItem', 'namespace': 'dash_bootstrap_components'}
                if not row["module_is_report"]:
                    currentmenu.append(tempmenu)
            menudiv.append({'props':
                            {'children': currentmenu,
                             'vertical': 'xs', 'pills': True, 'style': {'margin': '0px', 'padding': '0px', 'display': 'inline', 'font-size': '14px'}},
                            'type': 'Nav',
                            'namespace': 'dash_bootstrap_components'})
            currentmenu = []
    return menudiv


def convertdateseriestoformat(df, column):
    df[column] = np.where(df[column].isna(), "1970-01-01", df[column])
    df[column] = df[column].astype(str).apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%m/%d/%Y'))
    df[column] = np.where(df[column] == "01/01/1970", "", df[column])
    return df[column]


def convertsalaryseriestoformat(df, column):
    df[column] = np.where(df[column].isna(), -1, df[column])
    df[column] = df[column].apply(lambda x: "{:,.2f}".format(x))
    df[column] = np.where(df[column] == "-1.00", "", df[column])
    return df[column]


def queryunits():
    sql = '''SELECT CONCAT(unit_name,' (',unit_code,') ')  as label, unit_id as value
    FROM units
    WHERE unit_delete_ind = %s
    ORDER BY unit_name'''
    values = (False,)
    columns = ['label', 'value']
    dfsql = securequerydatafromdatabase(sql, values, columns)
    return dfsql.to_dict('records')


def queryplantillaitems():
    sql = '''SELECT plantilla_number as label, plantilla_id as value
               FROM plantilla_items
              WHERE plantilla_delete_ind = %s
                AND plantilla_is_active = %s
             ORDER BY plantilla_number'''
    values = (False, True)
    columns = ['label', 'value']
    dfsql = securequerydatafromdatabase(sql, values, columns)
    return dfsql.to_dict('records')


def queryfordropdown(sql, values):
    columns = ['label', 'value']
    dfsql = securequerydatafromdatabase(sql, values, columns)
    return dfsql.to_dict('records')


def returnbpstatuses(bp_id):
    flow_type = getbpflowtype(bp_id)
    hassnewflow = bphasnewflow(bp_id)

    if hassnewflow == False:
    # if flow_type == 0:
        sqlstatus='''select approval_flow_step_number, bp_status_name
            FROM basic_papers bp
            INNER JOIN bp_approval_flows baf ON bp.bp_approval_flow_id = baf.approval_flow_id
            INNER JOIN bp_approval_flow_steps bafs ON bafs.approval_flow_id =bp.bp_approval_flow_id
            INNER JOIN bp_statuses bs ON bs.bp_status_id = bafs.bp_status_id
            WHERE bp.bp_id=%s and approval_flow_step_delete_ind = %s
            ORDER BY approval_flow_step_number '''
        valuesstatus = (bp_id,False)
        columnsstatus = ['approval_flow_step_number', 'bp_status_name']
        dfstatus = securequerydatafromdatabase(sqlstatus, valuesstatus, columnsstatus)

        dfstatus = dfstatus.append({'approval_flow_step_number': 0, 'bp_status_name':'Draft'}, ignore_index=True)
        dfstatus = dfstatus.append({'approval_flow_step_number': 100, 'bp_status_name':'Processed'}, ignore_index=True)

        dfstatus.sort_values("approval_flow_step_number", inplace=True)

        sqlcurrstatus='''select bp_status_name
            FROM basic_papers bp
            LEFT JOIN bp_status_changes bsc ON bsc.bp_id = bp.bp_id
            INNER JOIN bp_statuses bs ON bs.bp_status_id = bsc.bp_status_id
            WHERE bp.bp_id=%s
            '''
        valuescurrstatus = (bp_id,)
        columnscurrstatus = ['bp_status_name']
        dfcurrstatus = securequerydatafromdatabase(sqlcurrstatus, valuescurrstatus, columnscurrstatus)


        dlist = []
        colorsuccess=True
        dfcurrstatuslist = dfcurrstatus['bp_status_name'].tolist()
        for index, row in dfstatus.iterrows():

            if not dfcurrstatus.empty:
                if row["bp_status_name"] in dfcurrstatuslist:
                    color="success"
                else:
                    color = "light"
            else:
                color = "light"
            dlist.append(dbc.Button([row["bp_status_name"]], color=color, style={'margin-top':"5px"}))

            if dfstatus.shape[0]-1>index:
                dlist.append(html.I(className='fas fa-arrow-alt-circle-right')) #, className="mr-1"



    else:
        # bp_approval_flow_new1_id
        # bp_approval_flow_new2_id

        sqlstatus1 = '''select approval_flow_step_number, bp_status_name
            FROM basic_papers bp
            INNER JOIN bp_approval_flows baf ON bp.bp_approval_flow_new1_id = baf.approval_flow_id
            INNER JOIN bp_approval_flow_steps bafs ON bafs.approval_flow_id =bp.bp_approval_flow_new1_id
            INNER JOIN bp_statuses bs ON bs.bp_status_id = bafs.bp_status_id
            WHERE bp.bp_id=%s and approval_flow_step_delete_ind = %s
            ORDER BY approval_flow_step_number '''
        valuesstatus1 = (bp_id, False)
        columnsstatus1 = ['approval_flow_step_number', 'bp_status_name']
        dfstatus1 = securequerydatafromdatabase(sqlstatus1, valuesstatus1, columnsstatus1)

        sqlstatus2 = '''select approval_flow_step_number, bp_status_name
            FROM basic_papers bp
            INNER JOIN bp_approval_flows baf ON bp.bp_approval_flow_new2_id = baf.approval_flow_id
            INNER JOIN bp_approval_flow_steps bafs ON bafs.approval_flow_id =bp.bp_approval_flow_new2_id
            INNER JOIN bp_statuses bs ON bs.bp_status_id = bafs.bp_status_id
            WHERE bp.bp_id=%s and approval_flow_step_delete_ind = %s
            ORDER BY approval_flow_step_number '''
        valuesstatus2 = (bp_id, False)
        columnsstatus2 = ['approval_flow_step_number', 'bp_status_name']
        dfstatus2 = securequerydatafromdatabase(sqlstatus2, valuesstatus2, columnsstatus2)


        dfstatus1 = dfstatus1.append({'approval_flow_step_number': 0, 'bp_status_name': 'Draft'}, ignore_index=True)
        dfstatus2 = dfstatus2.append({'approval_flow_step_number': 100, 'bp_status_name': 'Processed'}, ignore_index=True)
        dfstatus1.sort_values("approval_flow_step_number", inplace=True)
        dfstatus2.sort_values("approval_flow_step_number", inplace=True)

        dfstatus3_list = [dfstatus1, dfstatus2]
        dfstatus3 = pd.concat(dfstatus3_list)

        sqlcurrstatus = '''select bp_status_name
            FROM basic_papers bp
            LEFT JOIN bp_status_changes bsc ON bsc.bp_id = bp.bp_id
            INNER JOIN bp_statuses bs ON bs.bp_status_id = bsc.bp_status_id
            WHERE bp.bp_id=%s
            '''


        valuescurrstatus = (bp_id,)
        columnscurrstatus = ['bp_status_name']
        dfcurrstatus = securequerydatafromdatabase(sqlcurrstatus, valuescurrstatus, columnscurrstatus)

        dlist = []
        colorsuccess=True
        dfcurrstatuslist = dfcurrstatus['bp_status_name'].tolist()
        for index, row in dfstatus3.iterrows():

            if not dfcurrstatus.empty:
                if row["bp_status_name"] in dfcurrstatuslist:
                    color="success"
                else:
                    color = "light"
            else:
                color = "light"


            dlist.append(dbc.Button([row["bp_status_name"]], color=color, style={'margin-top':"5px"}))

            if dfstatus3.shape[0]-1>index:
                dlist.append(html.I(className='fas fa-arrow-alt-circle-right')) #, className="mr-1"

    return dlist
    # return dlist

#######################################################################################
#approve leaves
#######################################################################################

def returnleavestatuses(leave_emp_id):
    sqlstatus='''select leave_approval_flow_step_number, leave_status_name
        FROM leave_employees le INNER JOIN leave_approval_flows laf ON le.leave_approval_flow_id = laf.leave_approval_flow_id
        INNER JOIN leave_approval_flow_steps lafs ON lafs.leave_approval_flow_id = le.leave_approval_flow_id
        INNER JOIN leave_statuses ls ON ls.leave_status_id = lafs.leave_status_id
        WHERE le.leave_emp_id=%s and leave_approval_flow_step_delete_ind = %s
        ORDER BY leave_approval_flow_step_number '''
    valuesstatus = (leave_emp_id,False)
    columnsstatus = ['leave_approval_flow_step_number', 'leave_status_name']
    dfstatus = securequerydatafromdatabase(sqlstatus, valuesstatus, columnsstatus)
    dfstatus = dfstatus.append({'leave_approval_flow_step_number': 0, 'leave_status_name':'Draft'}, ignore_index=True)
    # dfstatus.append(html.I(className='fas fa-arrow-alt-circle-right'))
    # dfstatus = dfstatus.append({'leave_approval_flow_step_number': 100, 'leave_status_name':'Approved'}, ignore_index=True)
    dfstatus.sort_values("leave_approval_flow_step_number", inplace=True)

    sqlcurrstatus='''select leave_status_name
        FROM leave_employees le LEFT JOIN leave_status_changes lsc ON lsc.leave_emp_id = le.leave_emp_id
        INNER JOIN leave_statuses ls ON ls.leave_status_id = lsc.leave_status_id
        WHERE le.leave_emp_id=%s
        '''
    valuescurrstatus = (leave_emp_id,)
    columnscurrstatus = ['leave_status_name']
    dfcurrstatus = securequerydatafromdatabase(sqlcurrstatus, valuescurrstatus, columnscurrstatus)


    dlist = []
    colorsuccess=True
    dfcurrstatuslist = dfcurrstatus['leave_status_name'].tolist()
    for index, row in dfstatus.iterrows():
        # if colorsuccess:
        #     color="success"
        # else:
        #     color = "light"
        if dfstatus.shape[0]-1>index:
            dlist.append(html.I(className='fas fa-arrow-alt-circle-right')) #, className="mr-1"
        if not dfcurrstatus.empty:
            if row["leave_status_name"] in dfcurrstatuslist:
                color="success"
            else:
                color = "light"
        else:
            color = "light"
        dlist.append(dbc.Button([row["leave_status_name"]], color=color, style={'margin-top':"5px"}))

    return dlist

def getleavestatusofstepnumber(leave_approval_flow_id, leave_approval_flow_step_number):
    sql4 = '''
                SELECT leave_status_id
                  FROM leave_approval_flow_steps
                 WHERE leave_approval_flow_id = %s
                   AND leave_approval_flow_step_number = %s
                   AND leave_approval_flow_step_delete_ind = %s
            '''

    values4 = (leave_approval_flow_id, leave_approval_flow_step_number, False)
    columns4 = ['leave_status_id']
    df4 = securequerydatafromdatabase(sql4, values4, columns4)
    leave_status_id_new = int(df4["leave_status_id"][0])
    return leave_status_id_new

def getcurrentleaveflowstepnumber(leave_approval_flow_id, leave_status_id):
    sql3 = '''
                SELECT leave_approval_flow_step_number
                  FROM leave_approval_flow_steps
                 WHERE leave_approval_flow_id = %s
                   AND leave_status_id = %s
                   AND leave_approval_flow_step_delete_ind = %s
            '''
    values3 = (leave_approval_flow_id, leave_status_id, False)
    columns3 = ['leave_approval_flow_step_number']


    df3 = securequerydatafromdatabase(sql3, values3, columns3)


    leave_approval_flow_step_number = int(df3["leave_approval_flow_step_number"][0])
    return leave_approval_flow_step_number


def getleaveflowid(leave_emp_id):
    sql2 = ''' SELECT leave_approval_flow_id
                 FROM leave_employees le
                WHERE leave_emp_id = %s
            '''
    values2 = (leave_emp_id,)
    columns2 = ['leave_approval_flow_id']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)
    leave_approval_flow_id = int(df2["leave_approval_flow_id"][0])
    return leave_approval_flow_id


def insertnewleaveempidstatuschange(bp_id, bp_status_id):

    sql6 = """
            INSERT INTO bp_status_changes(bp_id, bp_status_id, bp_status_change_current_ind,
               bp_status_change_delete_ind)
            VALUES (%s, %s, %s, %s)
        """
    values6 = [bp_id, bp_status_id, True, False]
    modifydatabase(sql6, values6)

def getleaverolestatusesasdf(role_id):
    sql0 = '''
        SELECT leave_status_id
          FROM leave_status_roles
         WHERE role_id = %s
           AND leave_status_role_delete_ind = %s
    '''
    columns0 = ['leave_status_id']
    values0 = (role_id, False)
    df0 = securequerydatafromdatabase(sql0, values0, columns0)
    return df0

def getcurrentleaveappstatus(leave_emp_id):
    sql1 = '''
                SELECT leave_status_id
                  FROM leave_status_changes
                 WHERE leave_emp_id = %s
                   AND leave_status_change_current_ind = %s
            '''

    values1 = (leave_emp_id, True)
    columns1 = ['leave_status_id'] #, 'leave_status_change_id'
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    leave_status_id = int(df1["leave_status_id"][0])
    return leave_status_id

def fillinapproverofleavecurrentstatus(current_role, role_id, user_id, leave_emp_id, leave_approval_profile_numberworkingdaysapprovedremarks):
    if current_role in [38]: #if hrdo analyst benefits
        sql55 = """
                    UPDATE leave_status_changes
                       SET leave_status_change_user_role_id = %s,
                           leave_status_change_by = %s,
                           leave_status_change_on = %s,
                           leave_status_change_remarks = %s
                     WHERE leave_emp_id = %s
                       AND leave_status_change_current_ind = %s
                    """
        values55 = (role_id, user_id, datetime.now(), leave_approval_profile_numberworkingdaysapprovedremarks, leave_emp_id, True)
        modifydatabase(sql55, values55)
    else:
        sql55 = """
                    UPDATE leave_status_changes
                       SET leave_status_change_user_role_id = %s,
                           leave_status_change_by = %s,
                           leave_status_change_on = %s
                     WHERE leave_emp_id = %s
                       AND leave_status_change_current_ind = %s
                    """
        values55 = (role_id, user_id, datetime.now(), leave_emp_id, True)
        modifydatabase(sql55, values55)

def setallleavestatuschangestofalse(leave_emp_id):
    sql5 = """
                UPDATE leave_status_changes
                   SET leave_status_change_current_ind = %s
                 WHERE leave_emp_id = %s
                """
    values5 = (False, leave_emp_id)
    modifydatabase(sql5, values5)


def insertnewleavestatuschange(leave_emp_id, leave_status_id):

    sql6 = """
            INSERT INTO leave_status_changes (leave_emp_id, leave_status_id, leave_status_change_current_ind, leave_status_change_delete_ind)
            VALUES (%s, %s, %s, %s)
        """
    values6 = [leave_emp_id, leave_status_id, True, False]
    modifydatabase(sql6, values6)

def updatenumberofdays(leave_emp_id, leave_approval_profile_numberworkingdaysapproved, leave_approval_profile_startdateapproved, leave_approval_profile_enddateapproved, leave_approval_is_with_pay_ddapproved, leave_approval_inclusivity_ddapproved):

    sql8 = """
                UPDATE leave_employees
                   SET leave_is_with_pay = %s, leave_start_date = %s, leave_end_date = %s, leave_inclusivity_id = %s
                 WHERE leave_emp_id = %s
                """
    values8 =(leave_approval_is_with_pay_ddapproved, leave_approval_profile_startdateapproved, leave_approval_profile_enddateapproved, leave_approval_inclusivity_ddapproved, leave_emp_id)
    modifydatabase(sql8, values8)

    sqlwithpay = '''SELECT leave_is_with_pay FROM leave_employees
                WHERE leave_emp_id = %s'''
    valueswithpay =(leave_emp_id,)
    columnswithpay = ['leave_is_with_pay']
    df = securequerydatafromdatabase(sqlwithpay, valueswithpay, columnswithpay)
    leave_is_with_pay = df["leave_is_with_pay"][0]

    if leave_is_with_pay == True or leave_is_with_pay == None:

        sql7 = """
                    UPDATE leave_employees
                       SET leave_emp_num_days_wpay = %s, lwop_equivalent_days = %s
                     WHERE leave_emp_id = %s
                    """
        values7 =(leave_approval_profile_numberworkingdaysapproved, None, leave_emp_id)
        modifydatabase(sql7, values7)
    elif leave_is_with_pay == False:
        sql7 = """
                    UPDATE leave_employees
                       SET lwop_equivalent_days = %s, leave_emp_num_days_wpay = %s
                     WHERE leave_emp_id = %s
                    """
        values7 =(leave_approval_profile_numberworkingdaysapproved, None, leave_emp_id)
        modifydatabase(sql7, values7)
    else:
        pass

def updateleavestatusid(leave_emp_id, leave_status_id):

    sql6 = """
            UPDATE leave_employees
            SET leave_status_id = %s
            WHERE leave_emp_id = %s
        """
    values6 = [leave_status_id, leave_emp_id]
    modifydatabase(sql6, values6)


def getslvlofemp(emp_id):
    sqlcommandempmore = '''SELECT CASE WHEN lt.leave_type_class_id = %s THEN 'Sick Leave Credit Earned'
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
                    ORDER BY LeaveType
                    '''
    valuesempmore = [2, 1, True, 1, 2, False, emp_id]

    columnsempmore = ['leave_type_name', 'leave_credits_balance', 'Date']
    dfempmore = securequerydatafromdatabase(sqlcommandempmore, valuesempmore, columnsempmore)
    slcount = dfempmore["leave_credits_balance"][0]
    vlcount = dfempmore["leave_credits_balance"][1]

    return slcount, vlcount

def approveleave(leave_emp_id, user_id, current_role, user_role, leave_approval_profile_numberworkingdaysapprovedremarks, leave_approval_profile_numberworkingdaysapproved, leave_approval_profile_startdateapproved, leave_approval_profile_enddateapproved, leave_approval_is_with_pay_ddapproved, leave_approval_inclusivity_ddapproved):
    # Retrieve approval_flow_id of given leave emp

    leave_approval_flow_id = getleaveflowid(leave_emp_id)

    #Retrieve allowed bp_status approvals of current role
    df0 = getleaverolestatusesasdf(current_role)


    # Retrieve current bp_status of given bp
    leave_status_id = getcurrentleaveappstatus(leave_emp_id)


    #if current bp status matches the status in bp_status roles, proceed. Otherwise, do not proceed with approval.
    if leave_status_id in df0["leave_status_id"].tolist():
        # if status == for reqt fulfillment, update to for HRDO analyst
        # if leave_status_id in [27]: #In process
        #     leave_status_id_new = 6 #HRDO appt

        # elif bp_status_id in [21]:
        #     bp_status_id_new = getpreviousbpstatus(bp_id)
        #     setallstatuschangestofalse(bp_id)
        #     insertnewbpstatuschange(bp_id, 1)
        # elif bp_status_id in [1]:
        #     bp_status_id_new = getfirstflowstatus(bp_approval_flow_id)
        # elif bp_status_id in [22]:
        #     bp_status_id_new = getfirstflowstatus(bp_approval_flow_id)
        #     setallstatuschangestofalse(bp_id)
        #     insertnewbpstatuschange(bp_id, 1)
        if leave_status_id in [19, '19'] or leave_status_id == 19:

            leave_status_id_new = getpreviousleavestatus(leave_emp_id)
            leavesetallstatuschangestofalse(leave_emp_id)
            insertnewleavestatuschange(leave_emp_id, 4)
        elif leave_status_id in [4, '4'] or leave_status_id == 4:

            leave_status_id_new = leavegetfirstflowstatus(leave_approval_flow_id)
        elif leave_status_id in [20, '20'] or leave_status_id == 20:

            leave_status_id_new = leavegetfirstflowstatus(leave_approval_flow_id)
            leavesetallstatuschangestofalse(leave_emp_id)
            insertnewleavestatuschange(leave_emp_id, 4)
        else:# Retreive current flow step number of bp_status of given bp

            sql3 = '''
                        SELECT leave_approval_flow_step_number
                          FROM leave_approval_flow_steps
                         WHERE leave_approval_flow_id = %s
                           AND leave_status_id = %s
                           AND leave_approval_flow_step_delete_ind = %s
                    '''

            values3 = (leave_approval_flow_id, leave_status_id, False)
            columns3 = ['leave_approval_flow_step_number']


            df3 = securequerydatafromdatabase(sql3, values3, columns3)


            leave_approval_flow_step_number = int(df3["leave_approval_flow_step_number"][0])
            getcurrentleaveflowstepnumber(getleaveflowid(leave_emp_id), leave_status_id)

            # Increment flow step number by 1, moving to the next step
            leave_approval_flow_step_number_new = leave_approval_flow_step_number + 1


            # Retreive NEW bp_status_id of incremented step number
            leave_status_id_new = getleavestatusofstepnumber(leave_approval_flow_id, leave_approval_flow_step_number_new)


        # Set approver of previous step
        fillinapproverofleavecurrentstatus(current_role, user_role, user_id, leave_emp_id, leave_approval_profile_numberworkingdaysapprovedremarks)

        # Set all other bp_statuses in bp_status_change table to FALSE
        setallleavestatuschangestofalse(leave_emp_id)

        # Insert new bp_status to bp_status_changes
        insertnewleavestatuschange(leave_emp_id, leave_status_id_new)

        if current_role in [38]: #if hrdo analyst benefits
        #update number of days and dates
            updatenumberofdays(leave_emp_id, leave_approval_profile_numberworkingdaysapproved, leave_approval_profile_startdateapproved, leave_approval_profile_enddateapproved, leave_approval_is_with_pay_ddapproved, leave_approval_inclusivity_ddapproved)
        else:
            pass

        #if approved by all
        if leave_status_id_new == 2:

            updateleavestatusid(leave_emp_id, leave_status_id_new)
            deductcredits(leave_emp_id, user_id)
            #Get emp id, type of leave, with/wo pay, # of days of the leave application
            # sqlempid = '''SELECT emp_id, leave_type_id, leave_is_with_pay, lwop_equivalent_days, leave_emp_num_days_wpay FROM leave_employees
            #     WHERE leave_emp_id = %s'''
            # valuesempid = (leave_emp_id,)
            # columnsempid = ['emp_id', 'leave_type_id', 'leave_is_with_pay', 'lwop_equivalent_days', 'leave_emp_num_days_wpay']
            # dfempid = securequerydatafromdatabase(sqlempid, valuesempid, columnsempid)
            # emp_id = str(dfempid["emp_id"][0])
            # leave_type_id = int(dfempid["leave_type_id"][0])
            # leave_is_with_pay = dfempid['leave_is_with_pay'][0]
            # current_sl, current_vl = getslvlofemp(emp_id)
            #
            # if leave_is_with_pay == False:
            #     numdays = 0 #dfempid['lwop_equivalent_days'][0]
            # else:
            #     numdays = dfempid['leave_emp_num_days_wpay'][0]
            #
            # leave_monetization_slcount = current_sl
            # leave_monetization_vlcount = current_vl
            # leave_monetization_vlcreditsinput = numdays
            #
            # vl_allowed_deduction = max(0, math.floor(leave_monetization_vlcount) - 5)
            # sl_allowed_deduction = max(0, math.floor(leave_monetization_slcount) - 15)
            # if leave_monetization_vlcreditsinput <= vl_allowed_deduction:
            #     vl_actual_deduction = leave_monetization_vlcreditsinput
            #     sl_actual_deduction = 0
            # else:
            #     vl_actual_deduction = vl_allowed_deduction
            #     sl_actual_deduction = leave_monetization_vlcreditsinput - vl_actual_deduction
            #
            # vl_leftover = leave_monetization_vlcount - vl_actual_deduction
            # sl_leftover = leave_monetization_slcount - sl_actual_deduction
            #
            # if leave_type_id == 7 and leave_is_with_pay == True: #if sick leave
            #     #Get sick leave credits
            #     sqlsickcredits = '''SELECT leave_credits_balance
            #                           FROM leave_employees le
			# 						 INNER JOIN leave_types lt ON lt.leave_type_id = le.leave_type_id
            #                          WHERE leave_credits_current_bal_ind = %s
            #                            AND emp_id = %s
            #                            AND leave_emp_delete_ind = %s
			# 						   AND lt.leave_type_class_id = %s'''
            #     valuessickcredits = (True, emp_id, False, 2)
            #     columnssickcredits = ['emp_id']
            #     dfsickcredits = securequerydatafromdatabase(sqlsickcredits, valuessickcredits, columnssickcredits)
            #     sickleavecredits = str(dfsickcredits["emp_id"][0])
            #
            #     #Update all current ind of sick leave and SL earned to false
            #     sqlupdatesick = '''UPDATE leave_employees
            #                         SET leave_credits_current_bal_ind = %s
            #                         WHERE emp_id = %s
            #                         AND leave_type_id IN (SELECT leave_type_id
			# 											    FROM leave_types
			# 											   WHERE leave_type_class_id = %s)
            #     '''
            #     valuesupdatesick = [False, emp_id, 2]
            #     modifydatabase(sqlupdatesick, valuesupdatesick)
            #
            #     leave_credits_balance = float(sickleavecredits) - float(numdays)
            #
            #     #Update balance of sick leave application
            #     sqlnewbalsick = '''UPDATE leave_employees
            #         SET leave_credits_balance = %s, leave_credits_current_bal_ind = %s, leave_credits_balance_as_of = %s
            #         WHERE leave_emp_id = %s
            #     '''
            #     valuesnewbalsick = [leave_credits_balance, True, datetime.now(), leave_emp_id]
            #     modifydatabase(sqlnewbalsick, valuesnewbalsick)
            #
            # elif (leave_type_id in [12, 29, 47, 53] and leave_is_with_pay == True) or (leave_type_id in [18, 47, 53]): #if vacation leave or mandatory leave (deducted to VL credits)
            #
            #     sqlvlcredits = '''SELECT leave_credits_balance FROM leave_employees
            #         where emp_id = %s
            #         AND leave_credits_current_bal_ind = %s
            #         AND leave_emp_delete_ind = %s
            #         AND leave_type_id IN %s'''
            #     valuesvlcredits = (emp_id, True, False, getallvacationleaves_tuple())
            #     columnsvlcredits = ['emp_id']
            #     dfvlcredits = securequerydatafromdatabase(sqlvlcredits, valuesvlcredits, columnsvlcredits)
            #     vlleavecredits = str(dfvlcredits["emp_id"][0])
            #
            #     #Update all current ind of vacation leave and vacation earned to false
            #     sqlupdatevl = '''UPDATE leave_employees
            #         SET leave_credits_current_bal_ind = %s
            #         WHERE emp_id = %s
            #         AND leave_type_id IN %s
            #     '''
            #     valuesupdatevl = [False, emp_id, getallvacationleaves_tuple()]
            #     modifydatabase(sqlupdatevl, valuesupdatevl)
            #
            #     if leave_type_id in [53]:
            #         leave_credits_balance = vl_leftover
            #     else:
            #         leave_credits_balance = float(vlleavecredits) - float(numdays)
            #
            #     #Update balance of vacation leave application
            #     sqlnewbalvl = '''UPDATE leave_employees
            #         SET leave_credits_balance = %s, leave_credits_current_bal_ind = %s, leave_credits_balance_as_of = %s
            #         WHERE leave_emp_id = %s
            #     '''
            #     valuesnewbalvl = [leave_credits_balance, True, datetime.now(), leave_emp_id]
            #     modifydatabase(sqlnewbalvl, valuesnewbalvl)
            #
            # elif leave_type_id in [42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55]:#regular phase 2 mone or special mone
            #
            #     # sqlsickcredits = '''SELECT leave_credits_balance FROM leave_employees
            #     #                     where emp_id = %s
            #     #                     AND leave_credits_current_bal_ind = %s
            #     #                     AND leave_emp_delete_ind = %s
            #     #                     AND leave_type_id IN %s'''
            #     # valuessickcredits = (emp_id, True, False, (7, 20, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52))
            #     # columnssickcredits = ['emp_id']
            #     # dfsickcredits = securequerydatafromdatabase(sqlsickcredits, valuessickcredits, columnssickcredits)
            #     # sickleavecredits = str(dfsickcredits["emp_id"][0])
            #
            #     # Update all current ind of sick leave and SL earned to false
            #     sqlupdatesick = '''UPDATE leave_employees
            #                         SET leave_credits_current_bal_ind = %s
            #                         WHERE emp_id = %s
            #                         AND leave_type_id IN %s
            #                     '''
            #     valuesupdatesick = [False, emp_id, (7, 20, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55)]
            #     modifydatabase(sqlupdatesick, valuesupdatesick)
            #
            #     # leave_credits_balance = float(sickleavecredits) - float(numdays)
            #     # print(numdays, 'numdays')
            #     # print(sickleavecredits, 'vlleavecredits')
            #     # print(leave_credits_balance, 'leave_credits_balance')
            #
            #     # Update balance of sick leave application
            #     sqlnewbalsick = '''UPDATE leave_employees
            #                         SET leave_credits_balance = %s, leave_credits_current_bal_ind = %s, leave_credits_balance_as_of = %s
            #                         WHERE leave_emp_id = %s
            #                     '''
            #     valuesnewbalsick = [sl_leftover, True, datetime.now(), leave_emp_id]
            #     modifydatabase(sqlnewbalsick, valuesnewbalsick)
            #
            #     # print('HERE345', vl_actual_deduction)
            #     if float(vl_actual_deduction) > 0:
            #
            #         sqlupdatesick = '''UPDATE leave_employees
            #                             SET leave_credits_current_bal_ind = %s
            #                             WHERE emp_id = %s
            #                             AND leave_type_id IN (SELECT leave_type_id FROM leave_types WHERE leave_type_class_id IN %s)
            #                         '''
            #         valuesupdatesick = [False, emp_id, (1,-1)]
            #         modifydatabase(sqlupdatesick, valuesupdatesick)
            #         if leave_emp_id in [42, 43, 44, 45, 46, 55]:
            #             leave_type_id = 47
            #         else:
            #             leave_type_id = 53
            #         sql6 = """
            #         INSERT INTO leave_employees(emp_id, leave_type_id, leave_emp_inserted_on, leave_emp_delete_ind,
            #                         leave_credits_balance, leave_credits_current_bal_ind, leave_credits_balance_as_of, leave_emp_inserted_by)
            #         VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            #             """
            #         values6 = [emp_id, leave_type_id, datetime.now(), False, vl_leftover, True, datetime.now(), int(user_id)]
            #         modifydatabase(sql6, values6)




        else:

            pass

def deductcredits(leave_emp_id, user_id):
    sqlempid = '''SELECT emp_id, leave_type_id, leave_is_with_pay, lwop_equivalent_days, leave_emp_num_days_wpay FROM leave_employees
        WHERE leave_emp_id = %s'''
    valuesempid = (leave_emp_id,)
    columnsempid = ['emp_id', 'leave_type_id', 'leave_is_with_pay', 'lwop_equivalent_days', 'leave_emp_num_days_wpay']
    dfempid = securequerydatafromdatabase(sqlempid, valuesempid, columnsempid)
    emp_id = str(dfempid["emp_id"][0])
    leave_type_id = int(dfempid["leave_type_id"][0])
    leave_is_with_pay = dfempid['leave_is_with_pay'][0]
    current_sl, current_vl = getslvlofemp(emp_id)

    if leave_is_with_pay == False:
        numdays = 0 #dfempid['lwop_equivalent_days'][0]
    else:
        numdays = dfempid['leave_emp_num_days_wpay'][0]

    leave_monetization_slcount = current_sl
    leave_monetization_vlcount = current_vl
    leave_monetization_vlcreditsinput = numdays

    vl_allowed_deduction = max(0, math.floor(leave_monetization_vlcount) - 5)
    sl_allowed_deduction = max(0, math.floor(leave_monetization_slcount) - 15)
    if leave_monetization_vlcreditsinput <= vl_allowed_deduction:
        vl_actual_deduction = leave_monetization_vlcreditsinput
        sl_actual_deduction = 0
    else:
        vl_actual_deduction = vl_allowed_deduction
        sl_actual_deduction = leave_monetization_vlcreditsinput - vl_actual_deduction

    vl_leftover = leave_monetization_vlcount - vl_actual_deduction
    sl_leftover = leave_monetization_slcount - sl_actual_deduction

    #get leave types deducted to sick leave Credits
    sqlsickleavetypes = '''SELECT leave_type_id
                          FROM leave_types lt
                          WHERE leave_type_class_id = %s
                          AND leave_type_delete_ind = %s
                          AND leave_type_current_ind = %s
                        '''
    valuessickleavetypes = (2, False, True,)
    columnssickleavetypes = ['leave_type_id']
    dfsickleavetypes = securequerydatafromdatabase(sqlsickleavetypes, valuessickleavetypes, columnssickleavetypes)

    sickleavetypes = dfsickleavetypes["leave_type_id"].tolist()
    sickleavetypes = tuple(sickleavetypes)

    #get leave types deducted to vacation leave Credits
    sqlvleavetypes = '''SELECT leave_type_id
                          FROM leave_types lt
                          WHERE leave_type_class_id = %s
                          AND leave_type_delete_ind = %s
                          AND leave_type_current_ind = %s
                        '''
    valuesvleavetypes = (1, False, True,)
    columnsvleavetypes = ['leave_type_id']
    dfvleavetypes = securequerydatafromdatabase(sqlvleavetypes, valuesvleavetypes, columnsvleavetypes)

    vleavetypes = dfvleavetypes["leave_type_id"].tolist()
    vleavetypes = tuple(vleavetypes)


    if (leave_type_id == 7 or leave_type_id in sickleavetypes) and leave_type_id not in [42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55] and leave_is_with_pay == True: #if sick leave
        print('bawas sl')
        #Get sick leave credits
        sqlsickcredits = '''SELECT leave_credits_balance
                              FROM leave_employees le
                             INNER JOIN leave_types lt ON lt.leave_type_id = le.leave_type_id
                             WHERE leave_credits_current_bal_ind = %s
                               AND emp_id = %s
                               AND leave_emp_delete_ind = %s
                               AND lt.leave_type_class_id = %s'''
        valuessickcredits = (True, emp_id, False, 2)
        columnssickcredits = ['emp_id']
        dfsickcredits = securequerydatafromdatabase(sqlsickcredits, valuessickcredits, columnssickcredits)
        sickleavecredits = str(dfsickcredits["emp_id"][0])

        #Update all current ind of sick leave and SL earned to false
        sqlupdatesick = '''UPDATE leave_employees
                            SET leave_credits_current_bal_ind = %s
                            WHERE emp_id = %s
                            AND leave_type_id IN (SELECT leave_type_id
                                                    FROM leave_types
                                                   WHERE leave_type_class_id = %s)
        '''
        valuesupdatesick = [False, emp_id, 2]
        modifydatabase(sqlupdatesick, valuesupdatesick)

        leave_credits_balance = float(sickleavecredits) - float(numdays)

        #Update balance of sick leave application
        sqlnewbalsick = '''UPDATE leave_employees
            SET leave_credits_balance = %s, leave_credits_current_bal_ind = %s, leave_credits_balance_as_of = %s
            WHERE leave_emp_id = %s
        '''
        valuesnewbalsick = [leave_credits_balance, True, datetime.now(), leave_emp_id]
        modifydatabase(sqlnewbalsick, valuesnewbalsick)

    elif ((leave_type_id in [12, 29, 47, 53] or leave_type_id in vleavetypes) and leave_type_id not in [42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55] and leave_is_with_pay == True) or (leave_type_id in [18, 47, 53]): #if vacation leave or mandatory leave (deducted to VL credits)
        print('bawas vl')
        sqlvlcredits = '''SELECT leave_credits_balance FROM leave_employees
            where emp_id = %s
            AND leave_credits_current_bal_ind = %s
            AND leave_emp_delete_ind = %s
            AND leave_type_id IN %s'''
        valuesvlcredits = (emp_id, True, False, getallvacationleaves_tuple())
        columnsvlcredits = ['emp_id']
        dfvlcredits = securequerydatafromdatabase(sqlvlcredits, valuesvlcredits, columnsvlcredits)
        vlleavecredits = str(dfvlcredits["emp_id"][0])

        #Update all current ind of vacation leave and vacation earned to false
        sqlupdatevl = '''UPDATE leave_employees
            SET leave_credits_current_bal_ind = %s
            WHERE emp_id = %s
            AND leave_type_id IN %s
        '''
        valuesupdatevl = [False, emp_id, getallvacationleaves_tuple()]
        modifydatabase(sqlupdatevl, valuesupdatevl)

        if leave_type_id in [53]:
            leave_credits_balance = vl_leftover
        else:
            leave_credits_balance = float(vlleavecredits) - float(numdays)

        #Update balance of vacation leave application
        sqlnewbalvl = '''UPDATE leave_employees
            SET leave_credits_balance = %s, leave_credits_current_bal_ind = %s, leave_credits_balance_as_of = %s
            WHERE leave_emp_id = %s
        '''
        valuesnewbalvl = [leave_credits_balance, True, datetime.now(), leave_emp_id]
        modifydatabase(sqlnewbalvl, valuesnewbalvl)

    elif leave_type_id in [42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55]:#regular phase 2 mone or special mone
        print('bawas mone')
        # sqlsickcredits = '''SELECT leave_credits_balance FROM leave_employees
        #                     where emp_id = %s
        #                     AND leave_credits_current_bal_ind = %s
        #                     AND leave_emp_delete_ind = %s
        #                     AND leave_type_id IN %s'''
        # valuessickcredits = (emp_id, True, False, (7, 20, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52))
        # columnssickcredits = ['emp_id']
        # dfsickcredits = securequerydatafromdatabase(sqlsickcredits, valuessickcredits, columnssickcredits)
        # sickleavecredits = str(dfsickcredits["emp_id"][0])

        # Update all current ind of sick leave and SL earned to false
        sqlupdatesick = '''UPDATE leave_employees
                            SET leave_credits_current_bal_ind = %s
                            WHERE emp_id = %s
                            AND leave_type_id IN %s
                        '''
        valuesupdatesick = [False, emp_id, (7, 20, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55)]
        modifydatabase(sqlupdatesick, valuesupdatesick)

        # leave_credits_balance = float(sickleavecredits) - float(numdays)
        # print(numdays, 'numdays')
        # print(sickleavecredits, 'vlleavecredits')
        # print(leave_credits_balance, 'leave_credits_balance')

        # Update balance of sick leave application
        sqlnewbalsick = '''UPDATE leave_employees
                            SET leave_credits_balance = %s, leave_credits_current_bal_ind = %s, leave_credits_balance_as_of = %s
                            WHERE leave_emp_id = %s
                        '''
        valuesnewbalsick = [sl_leftover, True, datetime.now(), leave_emp_id]
        modifydatabase(sqlnewbalsick, valuesnewbalsick)

        # print('HERE345', vl_actual_deduction)
        if float(vl_actual_deduction) > 0:

            sqlupdatesick = '''UPDATE leave_employees
                                SET leave_credits_current_bal_ind = %s
                                WHERE emp_id = %s
                                AND leave_type_id IN (SELECT leave_type_id FROM leave_types WHERE leave_type_class_id IN %s)
                            '''
            valuesupdatesick = [False, emp_id, (1,-1)]
            modifydatabase(sqlupdatesick, valuesupdatesick)
            if leave_emp_id in [42, 43, 44, 45, 46, 55]:
                leave_type_id = 47
            else:
                leave_type_id = 53
            sql6 = """
            INSERT INTO leave_employees(emp_id, leave_type_id, leave_emp_inserted_on, leave_emp_delete_ind,
                            leave_credits_balance, leave_credits_current_bal_ind, leave_credits_balance_as_of, leave_emp_inserted_by)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """
            values6 = [emp_id, leave_type_id, datetime.now(), False, vl_leftover, True, datetime.now(), int(user_id)]
            modifydatabase(sql6, values6)
    else:
        print('wala bawas')
        pass

def getallvacationleaves_tuple():
    sqlupdatevl = '''
    SELECT leave_type_id
    FROM leave_types
    WHERE leave_type_delete_ind = %s
    AND leave_type_class_id = %s
    '''
    valuesupdatevl = [False, 1]
    columns = ['leave_type_id']
    dfvlcredits = securequerydatafromdatabase(sqlupdatevl, valuesupdatevl, columns)

    vl_types = dfvlcredits['leave_type_id'].tolist()
    vl_types = tuple(vl_types)

    return vl_types




def isbpinlaststep(bp_id):
    flow_type = getbpflowtype(bp_id)
    if flow_type == 1:
        flowid = getbpflowidnew1(bp_id)
    elif flow_type == 2:
        flowid = getbpflowidnew2(bp_id)
    else:
        flowid = getbpflowid(bp_id)
    sql1 = '''
            SELECT MAX(approval_flow_step_number)
            FROM bp_approval_flow_steps
            WHERE approval_flow_id = %s
            AND approval_flow_step_delete_ind = %s
    '''
    values1 = (flowid, False)
    columns1 = ['approval_flow_step_number']
    df = securequerydatafromdatabase(sql1, values1, columns1)
    maxflowid = int(df["approval_flow_step_number"][0])
    if maxflowid == int(getflowstepnumber(bp_id)):
        laststep = True
    else:
        laststep = False

    return laststep

def doesbphavenonterminalprinting(bp_id):
    #get flow id of bp
    # flowid = getbpflowid(bp_id)
    flowtype = getbpflowtype(bp_id)
    if flowtype == 1:
        flowid = getbpflowidnew1(bp_id)
    elif flowtype == 2:
        flowid = getbpflowidnew2(bp_id)
    else:
        flowid = getbpflowid(bp_id)

    #get final bp_status_id of the flow
    sql1 = '''
            SELECT MAX(approval_flow_step_number)
            FROM bp_approval_flow_steps
            WHERE approval_flow_id = %s
            AND approval_flow_step_delete_ind = %s
    '''
    values1 = (flowid, False)
    columns1 = ['approval_flow_step_number']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    laststepnumber = int(df1["approval_flow_step_number"][0])


    #get all flow steps except the last
    sql2 = '''
        SELECT bp_status_id
        FROM bp_approval_flow_steps
        WHERE approval_flow_id = %s
        AND approval_flow_step_delete_ind = %s
        AND approval_flow_step_number != %s
    '''
    values2 = (flowid, False, laststepnumber)
    columns2 = ['approval_flow_step_number']
    df2 = securequerydatafromdatabase(sql2, values2, columns2)

    nonterminalstatuses_list = df2['approval_flow_step_number'].tolist()

    printing_statuses = [26, 32, 33]

    is_there_nonterminal_printing_status = False
    for i in printing_statuses:
        if i in nonterminalstatuses_list:
            is_there_nonterminal_printing_status = True
            break

    return is_there_nonterminal_printing_status


def changeleavestatuswithremarks(leave_emp_id, newleavestatus, sendbackremarks, user_id, user_role_id):
    # Set all other bp_statuses in bp_status_change table to FALSE
    sql5 = """
                UPDATE leave_status_changes
                   SET leave_status_change_current_ind = %s
                 WHERE leave_emp_id = %s
                """
    values5 = (False, leave_emp_id)
    modifydatabase(sql5, values5)

    # Insert new bp_status to bp_status_changes and as active
    sql6 = """
            INSERT INTO leave_status_changes(leave_emp_id, leave_status_id, leave_status_change_current_ind, leave_status_change_by, leave_status_change_user_role_id,
                leave_status_change_on, leave_status_change_delete_ind, leave_status_change_remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

        """
    values6 = [leave_emp_id, newleavestatus, True, user_id, user_role_id, datetime.now(), False, sendbackremarks]
    modifydatabase(sql6, values6)

def getpersonidfrombp(bp_id):
    sql1 = '''
            SELECT person_id
            FROM basic_papers
            WHERE bp_id = %s
    '''
    values1 = (bp_id,)
    columns1 = ['person_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    person_id = int(df1["person_id"][0])

    return person_id

def getempclassidfrombp(bp_id):
    sql1 = '''
            SELECT bp_emp_class_id
            FROM basic_papers
            WHERE bp_id = %s
    '''
    values1 = (bp_id,)
    columns1 = ['bp_emp_class_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    bp_emp_class_id = int(df1["bp_emp_class_id"][0])

    return bp_emp_class_id

def getunitfrombp(bp_id):
    sql1 = '''
            SELECT bp_designation_unit_id
            FROM basic_papers
            WHERE bp_id = %s
    '''
    values1 = (bp_id, )
    columns1 = ['bp_designation_unit_id']
    df1 = securequerydatafromdatabase(sql1, values1, columns1)
    bp_designation_unit_id = int(df1["bp_designation_unit_id"][0])

    return bp_designation_unit_id


def generate_empnum(person_id, emp_type):

    sql = '''
                                SELECT emp_number
                                FROM employees
                        '''
    values = (1,)

    columns = ['emp_number']

    df = securequerydatafromdatabase(sql, values, columns)

    emp_nums = df['emp_number']

    emp_nums_list = emp_nums.values.tolist()
    emp_nums_list_str = [str(x) for x in emp_nums_list]

    sql = '''
                                SELECT person_last_name
                                FROM persons
                                WHERE person_id = %s
                        '''
    values = (person_id,)

    columns = ['person_last_name']
    df = securequerydatafromdatabase(sql, values, columns)

    firstletter_num = ord(df['person_last_name'][0].lower()[0]) - 96

    for i in range(2 - len(str(firstletter_num))):
        zer_str = "0"
        firstletter_num = str(firstletter_num)
        firstletter_num = zer_str + firstletter_num
    emp_str1 = str(firstletter_num)
    sql = '''
                                SELECT emp_class_id
                                FROM employees
                                WHERE person_id = %s
                        '''
    values = (1,)

    columns = ['emp_class_id']

    df = securequerydatafromdatabase(sql, values, columns)

    # emp_str2_proxy = str(df['emp_class_id'][0])#getting emp_type from db
    emp_str2_proxy = str(emp_type)  # using emp_type in dd

    if emp_str2_proxy == "1":
        emp_str2 = "1"
    elif emp_str2_proxy == "2":
        emp_str2 = "3"
    elif emp_str2_proxy == "3":
        emp_str2 = "2"
    else:
        emp_str2 = "3"

    for x in range(1000000):
        for i in range(6 - len(str(x))):
            zer_str = "0"
            x = str(x)
            x = str(zer_str + x)

        emp_num_fin = emp_str1 + emp_str2 + str(x)

        if emp_num_fin in emp_nums_list_str:
            print('')

        else:

            emp_num = emp_num_fin
            break

    return emp_num


def title_w_escape(input_string):
    # list of articles

    articles = ["a", "an", "the"]

    # list of coordinating conjunctins
    conjunctions = ["and", "but",
                    "for", "nor",
                    "or", "so",
                    "yet"]

    # list of some short articles
    prepositions = ["in", "to", "for",
                    "with", "on", "at",
                    "from", "by",
                    "as", "of"]

    # merging the 3 lists
    lower_case = articles + conjunctions + prepositions

    # variable declaration for the output text
    output_string = ""

    # separating each word in the string
    input_list = input_string.split(" ")

    # checking each word
    for word in input_list:

        # if the word exists in the list
        # then no need to capitalize it
        if word.lower() in lower_case:
            output_string += word.lower() + " "

        # if the word does not exists in
        # the list, then capitalize it
        else:
            temp = word.title()
            output_string += temp + " "

    if output_string[-1] == " ":
        output_string = output_string[:-1]

    return output_string


def returnadminpos(unit_id, position_id):
    sqlcommand = '''
    SELECT person_first_name || ' ' || COALESCE( CONCAT(LEFT(person_middle_name,1), '.') ,'') || ' ' || person_last_name || ' ' ||COALESCE(person_name_extension, '')
    FROM admin_positions ap INNER JOIN admin_employees ae ON ap.admin_pos_id = ae.admin_pos_id
    INNER JOIN employees e ON e.emp_id = ae.emp_id
    INNER JOIN persons p ON p.person_id = e.person_id
    WHERE ap.admin_pos_unit_id = %s AND ap.admin_designation_id = %s
    '''
    df =securequerydatafromdatabase(sqlcommand, [unit_id, position_id],['name'])
    if df.empty:
        return "No Admin Employee in Settings"
    else:
        return df['name'][0]


def generateplantillaitemversions(plantillaid, tab_number):
    #start of plantilla versions
    sqlcommandplantillaversions = '''
                    SELECT pi.plantilla_id,  CONCAT('UPSB-', piv.plantilla_number) AS plantilla_number, plantilla_version_year,
                           CASE WHEN piv.plantilla_version_is_active = True THEN 'Active'
                                WHEN piv.plantilla_version_is_active = False THEN 'Inactive'
                                ELSE ''
                           END
                      FROM plantilla_items pi
                    LEFT JOIN plantilla_item_versions piv ON piv.plantilla_id = pi.plantilla_id
                     WHERE plantilla_version_delete_ind = %s
                       AND pi.plantilla_id = %s
                       AND plantilla_delete_ind = %s
                    ORDER BY plantilla_version_year DESC
        '''
    valuesplantillaversions = [False, plantillaid, False]
    columnsplantillaversions = ['plantilla_id',
                                'plantilla_number',
                                'plantilla_version_year',
                                'plantilla_version_is_active',]

    dfplantilla = securequerydatafromdatabase(sqlcommandplantillaversions, valuesplantillaversions, columnsplantillaversions)
    dfplantilla.columns = ["Plantilla ID",
                           "Plantilla #",
                           "Version Year",
                           "Currently Active?"]

    tableplantillaversions = dbc.Table.from_dataframe(dfplantilla, striped=True, bordered=True, hover=True)
    return tableplantillaversions


def generateplantillafillstatuschanges(plantillaid, tab_number):
    #start of plantilla versions
    sqlcommandplantillafillstatuschanges = '''
                    SELECT pi.plantilla_id, CONCAT('UPSB-', piv.plantilla_number) AS plantilla_number, u.unit_name AS "Unit Owner", dn.designation_name AS "UP DESIGNATION Equivalent",
                           pfs.plantilla_fill_status_name, pfsc.plantilla_fill_status_date,
                           CASE
                            WHEN plantilla_fill_status_change_current_ind = 'True' THEN 'Yes'
                            ELSE 'No'
                           END
                      FROM plantilla_items pi
                    LEFT JOIN plantilla_item_versions piv ON piv.plantilla_id = pi.plantilla_id
                    LEFT JOIN plantilla_fill_status_changes pfsc ON pfsc.plantilla_id = pi.plantilla_id
                    LEFT JOIN plantilla_fill_statuses pfs ON pfs.plantilla_fill_status_id = pfsc.plantilla_fill_status_id
                    LEFT JOIN units u ON u.unit_id = pi.plantilla_owner_unit_id
                    LEFT JOIN designations d ON d.designation_id = pi.plantilla_dbm_position_title_id
                    LEFT JOIN designations dn ON dn.designation_id = pi.plantilla_up_designation_id
                     WHERE piv.plantilla_version_is_active = %s
                       AND piv.plantilla_version_delete_ind = %s
					   AND pfsc.plantilla_fill_status_change_delete_ind = %s
                       AND pi.plantilla_delete_ind = %s
					   AND pi.plantilla_id = %s
                    ORDER BY pfsc.plantilla_fill_status_change_inserted_on DESC, plantilla_fill_status_date DESC
        '''
    valuesplantillafillstatuschanges = [True, False, False, False, plantillaid,]
    columnsplantillafillstatuschanges = [
                                        'plantilla_id',
                                        'plantilla_number',
                                        'unit_name',
                                        'designation_name',
                                        'plantilla_fill_status_name',
                                        'plantilla_fill_status_date',
                                        'plantilla_fill_status_change_current_ind',
                                        ]

    dfplantilla = securequerydatafromdatabase(sqlcommandplantillafillstatuschanges, valuesplantillafillstatuschanges, columnsplantillafillstatuschanges)
    dfplantilla.columns = ["Plantilla ID",
                           "Plantilla #",
                           "Unit",
                           "Designation",
                           "Fill Status",
                           "Fill Date",
                           "Current Status"]
    tableplantillafillstatuschanges = dbc.Table.from_dataframe(dfplantilla, striped=True, bordered=True, hover=True)
    for index, row in dfplantilla.iterrows():
        if row["Current Status"] == "Yes":
            tableplantillafillstatuschanges.children[1].children[index].style={'backgroundColor':"rgba(40,167,69,0.5)"}
    return tableplantillafillstatuschanges

def getfirstofthemonthfromdate():
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')

    print('HERE34545', year, month)
    first_day = '01'
    last_day = calendar.monthrange(int(year), int(month))[1]

    print('HERE34546', first_day, last_day)

    first_yyyymmdd = year + '-' + month + '-' + str(first_day)
    last_yyyymmdd = year + '-' + month + '-' + str(last_day)

    print('HERE34547', first_yyyymmdd, last_yyyymmdd)

    return first_yyyymmdd

def getlastofthemonthfromdate():
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')

    print('HERE34545', year, month)
    first_day = '01'
    last_day = calendar.monthrange(int(year), int(month))[1]

    print('HERE34546', first_day, last_day)

    first_yyyymmdd = year + '-' + month + '-' + str(first_day)
    last_yyyymmdd = year + '-' + month + '-' + str(last_day)

    print('HERE34547', first_yyyymmdd, last_yyyymmdd)

    return last_yyyymmdd

def getlistingcountthismonth():
    sql = '''
        SELECT COUNT(job_listing_id) as count
        FROM job_listings1
        WHERE job_listing_created_on > %s
        AND job_listing_created_on < %s
        AND job_listing_delete_ind = %s

    '''

    values = (getfirstofthemonthfromdate(), getlastofthemonthfromdate(), False)

    columns = ['count']

    df = securequerydatafromdatabase(sql, values, columns)

    count = df['count'][0]
    count = int(count)
    count += 1
    return str(count)
