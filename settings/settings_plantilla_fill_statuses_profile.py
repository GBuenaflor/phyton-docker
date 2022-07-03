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
import logging

app.config.suppress_callback_exceptions = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Plantilla Fill Status", id="plantilla_fill_status_profile_card_head"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Plantilla Fill Statuses", id="plantilla_fill_status_profile_edit_modal_head"),
                dbc.ModalBody([
                ], id="plantilla_fill_status_profile_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="plantilla_fill_status_profile_edit_modal_head_close",
                                       color="primary", block=True),
                        ], id="plantilla_fill_status_profile_edit_modal_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="plantilla_fill_status_profile_edit_modal_head_return_btn",
                                       color="primary", block=True, href='/settings/settings_plantilla_fill_statuses'),
                        ], id="plantilla_fill_status_profile_edit_modal_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="plantilla_fill_status_profile_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Plantilla Fill Statuses', href='/settings/settings_plantilla_fill_statuses'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Fill Status Name*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="plantilla_fill_status_profile_name", placeholder="Enter Fill Status Name"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Fill Status Description*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="plantilla_fill_status_profile_description", placeholder="Enter Plantilla Fill Status Description"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='plantilla_fill_status_profile_chkmarkfordeletion', value=[]
                        ),
                    ], id='plantilla_fill_status_profile_delete_div',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Plantilla Fill Status", id="plantilla_fill_status_profile_submit_btn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="plantilla_fill_status_profile_cancel_btn",
                                   href='/settings/settings_plantilla_fill_statuses', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='plantilla_fill_status_profile_submit_status', type='text', value=0)
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='plantilla_fill_status_profile_plantilla_status_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='plantilla_fill_status_profile_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@ app.callback(
    [
        Output('plantilla_fill_status_profile_name', 'value'),
        Output('plantilla_fill_status_profile_description', 'value'),
        Output("plantilla_fill_status_profile_card_head", "children"),
        Output("plantilla_fill_status_profile_submit_btn", "children"),
        Output("plantilla_fill_status_profile_plantilla_status_id", 'value'),
        Output("plantilla_fill_status_profile_chkmarkfordeletion", "value"),
        Output("plantilla_fill_status_profile_delete_div", "style"),
    ],
    [
        Input('plantilla_fill_status_profile_submit_status', 'value'),
        Input("url", "search"),
        Input("url", "pathname"),
    ],
    [
        State('plantilla_fill_status_profile_card_head', "children"),
        State("plantilla_fill_status_profile_submit_btn", "children"),
        State("plantilla_fill_status_profile_plantilla_status_id", 'value'),
        State("plantilla_fill_status_profile_chkmarkfordeletion", "value"),
    ]
)
def returnfillstatusdata(plantilla_fill_status_profile_submit_status,  # plantilla_fill_status_profile_edit_modal_head_close,
                     url,
                     pathname,
                     plantilla_fill_status_profile_card_head,
                     plantilla_fill_status_profile_submit_btn,
                     plantilla_fill_status_profile_plantilla_status_id,
                     plantilla_fill_status_profile_chkmarkfordeletion):
    print('printing plantilla_fill_status_profile_submit_status, ', plantilla_fill_status_profile_submit_status)
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query and (pathname == "/settings/settings_plantilla_fill_statuses_profile"):

        if parse_qs(parsed.query)['mode'][0] == "edit":
            plantilla_fill_status_profile_plantilla_status_id = parse_qs(parsed.query)['plantilla_fill_status_id'][0]
            sql = '''
                    SELECT plantilla_fill_status_id, plantilla_fill_status_name, plantilla_fill_status_description
                      FROM plantilla_fill_statuses
                     WHERE plantilla_fill_status_delete_ind = %s
                       AND plantilla_fill_status_id = %s
                  '''
            values = (False, plantilla_fill_status_profile_plantilla_status_id)
            columns = ['plantilla_fill_status_id', 'plantilla_fill_status_name', 'plantilla_fill_status_description']
            df = securequerydatafromdatabase(sql, values, columns)
            plantilla_fill_status_name = df["plantilla_fill_status_name"][0]
            plantilla_fill_status_description = df["plantilla_fill_status_description"][0]

            values = [plantilla_fill_status_name,
                        plantilla_fill_status_description,
                        "Edit Existing Plantilla Fill Status:",
                        "Save Changes",
                        plantilla_fill_status_profile_plantilla_status_id,
                        [],
                        {'text-align': 'middle', 'display': 'inline'}
                    ]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":

            values = ["",
                        "",
                        plantilla_fill_status_profile_card_head,
                        plantilla_fill_status_profile_submit_btn,
                        plantilla_fill_status_profile_plantilla_status_id,
                        [],
                        {'display': 'none'}]
            return values
        else:
            print('printing im here here here here')
            raise PreventUpdate
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output('plantilla_fill_status_profile_name', 'valid'),
        Output('plantilla_fill_status_profile_name', 'invalid'),
        Output('plantilla_fill_status_profile_description', 'valid'),
        Output('plantilla_fill_status_profile_description', 'invalid'),
        Output('plantilla_fill_status_profile_submit_status', "value"),
        Output('plantilla_fill_status_profile_modal', "is_open"),
        Output('plantilla_fill_status_profile_results_body', "children"),
        Output('plantilla_fill_status_profile_edit_modal_head_close', "style"),
        Output('plantilla_fill_status_profile_edit_modal_head_return', "style"),
    ],
    [
        Input('plantilla_fill_status_profile_submit_btn', 'n_clicks'),
        Input('plantilla_fill_status_profile_edit_modal_head_close', 'n_clicks'),
        Input('plantilla_fill_status_profile_edit_modal_head_return_btn', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('plantilla_fill_status_profile_name', 'value'),
        State('plantilla_fill_status_profile_description', 'value'),
        State("plantilla_fill_status_profile_submit_btn", "children"),
        State("plantilla_fill_status_profile_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('plantilla_fill_status_profile_plantilla_status_id', 'value'),
    ]

)
def processdata(plantilla_fill_status_profile_submit_btn,
                plantilla_fill_status_profile_edit_modal_head_close,
                plantilla_fill_status_profile_edit_modal_head_return_btn,
                current_user_id,
                plantilla_fill_status_profile_name,
                plantilla_fill_status_profile_description,
                mode,
                plantilla_fill_status_profile_chkmarkfordeletion,
                url,
                plantilla_fill_status_profile_plantilla_status_id
                ):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False,  # False, False, False, False,False, False, False, False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'plantilla_fill_status_profile_submit_btn':
            if plantilla_fill_status_profile_name:
                is_valid_fill_status_name = True
            else:
                is_valid_fill_status_name = False

            if plantilla_fill_status_profile_description:
                is_valid_fill_status_description = True
            else:
                is_valid_fill_status_description = False

            validity = [
                is_valid_fill_status_name, not is_valid_fill_status_name,
                is_valid_fill_status_description, not is_valid_fill_status_description,
            ]
            allvalid = [is_valid_fill_status_name,
                        is_valid_fill_status_description]
            if all(allvalid):
                if mode == "Save New Plantilla Fill Status":
                    if plantilla_fill_status_profile_description == '':
                        plantilla_fill_status_profile_description = None
                    else:
                        plantilla_fill_status_profile_description

                    sql = """
                        INSERT INTO plantilla_fill_statuses (plantilla_fill_status_name,
                                                             plantilla_fill_status_description,
                                                             plantilla_fill_status_inserted_by,
                                                             plantilla_fill_status_inserted_on,
                                                             plantilla_fill_status_delete_ind
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING plantilla_fill_status_id
                    """
                    values = (plantilla_fill_status_profile_name,
                              plantilla_fill_status_profile_description,
                              current_user_id,
                              datetime.now(),
                              False
                              )
                    plantilla_fill_status_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new plantilla fill status"
                    status = "1"
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                else:
                    print('not maximilain')
                    sql = """
                        UPDATE plantilla_fill_statuses
                           SET plantilla_fill_status_name = %s,
                               plantilla_fill_status_description = %s,
                               plantilla_fill_status_delete_ind= %s,
                               plantilla_fill_status_inserted_by = %s,
                               plantilla_fill_status_inserted_on = %s
                        WHERE  plantilla_fill_status_id = %s
                    """
                    if '1' in plantilla_fill_status_profile_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False

                    values = (plantilla_fill_status_profile_name,
                              plantilla_fill_status_profile_description,
                              fordelete,
                              current_user_id,
                              datetime.now(),
                              plantilla_fill_status_profile_plantilla_status_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False, False,  # False, False, False, False,False, False, False, False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited plantilla fill status information"
                    status = "1"
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display': 'inline'}
                stylehead_return = {'display': 'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        elif eventid == 'plantilla_fill_status_profile_edit_modal_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display': 'inline'}
            stylehead_return = {'display': 'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
