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
                html.H4("Add New School", id="school_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Schools", id="school_results_head"),
                dbc.ModalBody([
                ], id="school_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_school_head_close",
                                       color="primary", block=True),
                        ], id="school_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_school_results_head_return",
                                       color="primary", block=True, href='/settings/settings_schools'),
                        ], id="school_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="school_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Schools', href='/settings/settings_schools'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("School Name*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_name", placeholder="Enter School Name"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label(
                            [
                                "School Country*",
                                html.Span(dbc.FormText("Default country is Philippines"),
                                          style={"font-style": "italic"})
                            ], width=2, style={"text-align": "left"}
                        ),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="school_country",
                                    options=[

                                    ],
                                    value=168,  # Philippines
                                    searchable=True
                                ),
                                # dbc.FormFeedback("Too short or already taken", valid = False)
                            ],
                            width=8
                        )],
                        row=True
                    ),
                    html.Div([
                        dbc.FormGroup(
                            [dbc.Label("School Province", width=2, style={"text-align": "left"}),

                             dbc.Col([
                                 dcc.Dropdown(
                                     id="school_province",
                                     options=[
                                     ],
                                     searchable=True,
                                 ),
                                 # dbc.FormFeedback("Too short or already taken", valid = False)
                             ],
                                width=8
                            )],
                            row=True
                        ),
                        dbc.FormGroup(
                            [dbc.Label(
                                [
                                    "School City (Philippines)",
                                    html.Span(dbc.FormText("Please select province first"),
                                              style={"font-style": "italic"})
                                ], width=2, style={"text-align": "left"}
                            ),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id="school_city",
                                        options=[
                                        ],
                                        searchable=True
                                    ),
                                    # dbc.FormFeedback("Too short or already taken", valid = False)
                                ],
                                width=8
                            )],
                            row=True
                        ),
                    ], id='school_prov_city_main_div',
                        style={'text-align': 'middle', 'display': 'inline'}),  # div for opening and closing city and province based on country philippines
                    dbc.FormGroup(
                        [dbc.Label("School Complete Address", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_address", placeholder="Enter School Address"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("School Postal Code", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_postal_code", placeholder="Enter School Postal Code"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("School Contact Person", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_contact_person", placeholder="Enter School Contact Person"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("School Contact Number", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_contact_number", placeholder="Enter School Number"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("School E-mail", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_contact_email", placeholder="Enter School E-mail"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("School Website", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_website", placeholder="Enter School Website"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("School Facebook Page", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_facebook_page", placeholder="Enter School Facebook Page"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("School Twitter", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="school_twitter", placeholder="Enter School Twitter Account"
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
                                {'label': 'Mark for Deletion?', 'value': '1'},
                            ], id='school_chkmarkfordeletion', value=[]
                        ),
                    ], id='div_school_delete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New School", id="school_submit_btn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="school_cancel",
                                   href='/settings/settings_schools', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='school_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='school_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='school_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@ app.callback(
    [
        Output('school_name', 'value'),
        Output('school_city', 'value'),
        Output('school_province', 'value'),
        Output('school_country', 'value'),
        Output('school_address', 'value'),
        Output('school_postal_code', 'value'),
        Output('school_contact_person', 'value'),
        Output('school_contact_number', 'value'),
        Output('school_contact_email', 'value'),
        Output('school_website', 'value'),
        Output('school_facebook_page', 'value'),
        Output('school_twitter', 'value'),
        Output("school_process_editmodalhead", "children"),
        Output("school_submit_btn", "children"),
        Output("school_id", 'value'),
        Output("school_chkmarkfordeletion", "value"),
        Output("div_school_delete", "style"),
        # Output('school_city', 'options'),
    ],
    [
        Input('school_submit_status', 'value'),
        # Input('btn_school_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('school_name', 'value'),
        State('school_city', 'value'),
        State('school_country', 'value'),
        State('school_process_editmodalhead', "children"),
        State("school_submit_btn", "children"),
        State("school_id", 'value'),
        State("school_chkmarkfordeletion", "value"),
    ]

)
def returnschooldata(school_submit_status,  # btn_school_head_close,
                     url,
                     school_name, school_city, school_country,
                     school_process_editmodalhead, school_submit_btn, school_id,
                     school_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            school_id = parse_qs(parsed.query)['school_id'][0]

            sql = '''
                    SELECT school_name, school_city_id, prov_id, school_country_id, school_address,
                           school_postal_code, school_contact_person, school_contact_number, school_contact_email,
                           school_website, school_facebook_page, school_twitter
                      FROM schools sch
					LEFT JOIN cities ct ON ct.city_id = sch.school_city_id
                     WHERE school_id = %s
                  '''
            values = (school_id,)
            columns = ['school_name', 'school_city_id',
                       'prov_id', 'school_country_id', 'school_address',
                       'school_postal_code', 'school_contact_person', 'school_contact_number',
                       'school_contact_email', 'school_website', 'school_facebook_page', 'school_twitter']
            df = securequerydatafromdatabase(sql, values, columns)
            school_name = df["school_name"][0]
            school_city_id = df["school_city_id"][0]
            school_country_id = df["school_country_id"][0]
            school_prov_id = df["prov_id"][0]
            school_address = df["school_address"][0]
            school_postal_code = df["school_postal_code"][0]
            school_contact_person = df["school_contact_person"][0]
            school_contact_number = df["school_contact_number"][0]
            school_contact_email = df["school_contact_email"][0]
            school_website = df["school_website"][0]
            school_facebook_page = df["school_facebook_page"][0]
            school_twitter = df["school_twitter"][0]
            values = [school_name, school_city_id, school_prov_id, school_country_id, school_address,
                      school_postal_code,  school_contact_person,  school_contact_number,
                      school_contact_email,  school_website,  school_facebook_page, school_twitter,
                      "Edit Existing School",
                      "Save Changes", school_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":

            values = ["", "", 0, 168, "", "", "", "", "", "", "", "", school_process_editmodalhead,
                      school_submit_btn, school_id, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output("school_name", "valid"),
        Output("school_name", "invalid"),
        # Output("school_city", "valid"),
        # Output("school_city", "invalid"),
        Output("school_country", "valid"),
        Output("school_country", "invalid"),
        Output('school_submit_status', "value"),
        Output('school_results_modal', "is_open"),
        Output('school_results_body', "children"),
        Output('school_results_head_close', "style"),
        Output('school_results_head_return', "style"),
    ],
    [
        Input('school_submit_btn', 'n_clicks'),
        Input('btn_school_head_close', 'n_clicks'),
        Input('btn_school_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('school_name', 'value'),
        # State('school_province', 'value'),
        State("school_city", "value"),
        State("school_country", "value"),
        State("school_address", "value"),
        State('school_postal_code', 'value'),
        State('school_contact_person', 'value'),
        State('school_contact_number', 'value'),
        State('school_contact_email', 'value'),
        State('school_website', 'value'),
        State('school_facebook_page', 'value'),
        State('school_twitter', 'value'),
        State("school_submit_btn", "children"),
        State("school_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('school_id', 'value'),
    ]

)
def processdata(school_submit_btn, btn_school_head_close, btn_school_results_head_return,
                current_user_id, school_name,  # school_province,
                school_city, school_country, school_address,
                school_postal_code, school_contact_person,
                school_contact_number, school_contact_email, school_website, school_facebook_page, school_twitter,
                mode, school_chkmarkfordeletion, url, school_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False,  # False, False, False, False,False, False, False, False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'school_submit_btn':
            if school_name:
                is_valid_school_name = True
            else:
                is_valid_school_name = False

            if school_country:
                is_valid_school_country = True
            else:
                is_valid_school_country = False

            validity = [
                is_valid_school_name, not is_valid_school_name,
                is_valid_school_country, not is_valid_school_country,
            ]
            allvalid = [is_valid_school_name,
                        is_valid_school_country]
            if all(allvalid):
                if mode == "Save New School":

                    if school_city == '':
                        school_city = None
                    else:
                        school_city

                    sql = """
                        INSERT INTO schools (school_name, school_city_id, school_country_id,  school_address, school_postal_code, school_contact_person,
                        school_contact_number, school_contact_email, school_website, school_facebook_page, school_twitter, school_inserted_by,
                        school_inserted_on, school_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING school_id
                    """
                    values = (school_name, school_city,
                              school_country, school_address, school_postal_code, school_contact_person,
                              school_contact_number, school_contact_email, school_website, school_facebook_page, school_twitter,
                              current_user_id, datetime.now(), False)
                    school_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new school"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE schools SET school_name = %s, school_city_id = %s, school_country_id = %s,  school_address = %s,
                            school_postal_code = %s, school_contact_person = %s,
                            school_contact_number = %s, school_contact_email = %s, school_website = %s, school_facebook_page = %s, school_twitter = %s,
                            school_delete_ind= %s, school_inserted_by = %s, school_inserted_on= %s WHERE
                            school_id = %s
                    """
                    if '1' in school_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (school_name, school_city, school_country, school_address, school_postal_code, school_contact_person,
                              school_contact_number, school_contact_email, school_website, school_facebook_page, school_twitter,
                              fordelete, current_user_id, datetime.now(), school_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False, False,  # False, False, False, False,False, False, False, False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited school information"
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
        elif eventid == 'btn_school_head_close':
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
#


@ app.callback(
    [
        Output('school_province', 'options'),
        # Output('school_cities', 'options'),
        Output('school_country', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
    ],
)
def fillindropdowns(pathname):
    if pathname == "/settings/settings_schools_profile":
        school_provinces = commonmodules.queryfordropdown('''
            SELECT prov_name AS label, prov_id AS value
              FROM provinces
             WHERE prov_delete_ind = %s
            ORDER BY prov_id
        ''', (False, ))

        # school_cities = commonmodules.queryfordropdown('''
        #     SELECT city_name AS LABEL, city_id AS VALUE
        #       FROM cities ct
        #     WHERE city_delete_ind = %s
        #     ORDER BY city_id
        # ''', (False, ))

        school_countries = commonmodules.queryfordropdown('''
            SELECT country_name AS label, country_id AS value
              FROM countries
            WHERE country_delete_ind = %s
            ORDER BY country_id
        ''', (False, ))

        return [school_provinces,  school_countries, ]
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output('school_city', 'options'),
    ],
    [
        Input('school_province', 'value'),
    ],
    [
        State('school_city', 'options'),
    ],

)
def toggle_cities_from_provinces(school_province, school_cities):
    ctx = dash.callback_context


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'school_province':
            school_cities = commonmodules.queryfordropdown('''
                         SELECT city_name AS LABEL, city_id AS VALUE
                           FROM cities ct
                          WHERE city_delete_ind = %s
                            AND prov_id = %s
                         ORDER BY city_id
                     ''', (False, school_province))
            return [school_cities]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output('school_prov_city_main_div', 'style'),
    ],
    [
        Input('school_country', 'value'),
    ],
)
def toggle_provinces_cities_div(school_country):
    ctx = dash.callback_context

    # if ctx.triggered:
    #     eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if school_country == 168:
        style = {'display': 'inline'}
        return [style]
    else:
        style = {'display': 'none'}
        return [style]
    # else:
    #     raise PreventUpdate
