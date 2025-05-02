import dash
from dash import dcc, html, Input, Output, callback_context as ctx
import pandas as pd
import numpy as np
import os
import plotly.express as px
from get_courses import make_a_schedule
# Initialize the Dash app
app = dash.Dash(__name__)

major_filepath = os.path.join("data", "majors_list.npy")
all_majors = np.load(major_filepath, allow_pickle=True).tolist()
minor_filepath = os.path.join("data", "minors_list.npy")
minors = np.load(minor_filepath, allow_pickle=True).tolist()
langs = ['N/A','spanish', 'french', 'arabic', 'chinese', 'italian', 'german', 'japanese', 'russian']
ops = ["I am planning on doing a semester abroad", "I am not planning on doing a semester abroad, but I might still study abroad", "I am not planning on studying abroad"]

# Layout of the app
app.layout = html.Div([
    html.Div([
        html.H1("Custom William & Mary Four Year Plans", style={'textAlign': 'center'}),
        html.P(
            "Welcome! Use this tool to create a personalized four-year plan. Start by entering your credits, "
            "selecting your primary major, and customizing additional preferences below.",
            style={'textAlign': 'center', 'marginBottom': '20px'}
        )
    ]),

   # Preferences Section Instructions
    html.Div([
        html.H3("Input Preferences Here:", style={'textAlign': 'left', 'marginBottom': '10px'}),
        html.P(
            "Provide your academic and study-abroad preferences. Depending on your degree type, additional "
            "fields will appear dynamically to guide your selections.",
            style={'marginBottom': '20px'}
        )
    ]),


    # Primary major selection
    html.Div([
        html.Label("Select Primary Major:"),
        dcc.Dropdown(
            id='dropdown-primary-major',
            options=[{'label': opt, 'value': opt} for opt in all_majors],
            placeholder="Choose..."
        )
    ], style={'marginBottom': '20px'}),

    # Input credits
    html.Div([
        html.Label("Enter Number of Credits Already Earned:"),
        dcc.Input(id='input-credits', type='number', placeholder="Enter credits...", min=0)
    ], style={'marginBottom': '20px'}),

    # Language dropdown
    html.Div([
        html.Label("Select Language:"),
        dcc.Dropdown(
            id='dd_lang',
            options=[{'label': opt, 'value': opt} for opt in langs],
            placeholder="Choose..."
        ),
        html.P(
            "NOTE: International Relations Majors must select a language even if they have already met the FLP requirement.",
            style={'marginBottom': '20px'}
        )
    ], style={'marginBottom': '20px'}),

    # Study abroad preference dropdown
    html.Div([
        html.Label("Semester Abroad Preference:"),
        dcc.Dropdown(
            id='dd_abroad',
            options=[{'label': opt, 'value': opt} for opt in ops],
            placeholder="Choose..."
        )
    ], style={'marginBottom': '20px'}),

    # Degree type selection
    html.Div([
        html.Label("Choose Degree Type:"),
        dcc.RadioItems(
            id='degree-type',
            options=[
                {'label': 'Single Major', 'value': 'single'},
                {'label': 'Double Major', 'value': 'double'},
                {'label': 'Major and Minor', 'value': 'major-minor'}
            ],
            value='single'
        )
    ], style={'marginBottom': '20px'}),

    # Dropdown for secondary major (hidden initially)
    html.Div(id='dropdown-secondary-major-container', children=[
        html.Label("Select Secondary Major:"),
        dcc.Dropdown(id='dropdown-secondary-major', 
                     options=[{'label': opt, 'value': opt} for opt in all_majors], 
                     placeholder="Choose...")
    ], style={'display': 'none'}),  # Hidden by default
    
    # Dropdown for minor (hidden initially)
    html.Div(id='dropdown-minor-container', children=[
        html.Label("Select Minor:"),
        dcc.Dropdown(id='dropdown-minor', 
                     options=[{'label': opt, 'value': opt} for opt in minors], 
                     placeholder="Choose...")
    ], style={'display': 'none'}),  # Hidden by default
    
    html.Button("Submit", id='submit-btn', n_clicks=0),
    
    html.Div(id='output-div')  # Placeholder for the chart or user feedback
])

# Callback to dynamically update dropdown visibility and options
@app.callback(
    [Output('dropdown-secondary-major-container', 'style'),
     Output('dropdown-minor-container', 'style'),
     Output('dropdown-secondary-major', 'options')],
    [Input('degree-type', 'value'),
     Input('dropdown-primary-major', 'value')]
)
def update_dropdown_visibility(degree_type, primary_major):
    # Exclude the primary major from secondary major dropdown
    secondary_options = [{'label': opt, 'value': opt} for opt in all_majors if opt != primary_major] if primary_major else [{'label': opt, 'value': opt} for opt in all_majors]

    if degree_type == 'double':
        # Show secondary major dropdown, hide minor dropdown
        return {'display': 'block', 'marginBottom': '20px'}, {'display': 'none', 'marginBottom': '20px'}, secondary_options
    elif degree_type == 'major-minor':
        # Show both secondary major and minor dropdowns
        return {'display': 'none'}, {'display': 'block', 'marginBottom': '20px'}, secondary_options
    else:
        # Hide both dropdowns
        return {'display': 'none'}, {'display': 'none'}, secondary_options
    

# Callback to handle submission and display selected options
@app.callback(
    Output('output-div', 'children'),
    [Input('dropdown-primary-major', 'value'),
     Input('dd_lang', 'value'),
     Input('dd_abroad', 'value'),
     Input('dropdown-secondary-major', 'value'),
     Input('dropdown-minor', 'value'),
     Input('input-credits', 'value'),
     Input('degree-type', 'value'),
     Input('submit-btn', 'n_clicks')]
)
def handle_submission(primary_major, lang, abroad, secondary_major, minor, credits, degree_type, n_clicks):
    if n_clicks > 0:
        # Validate required inputs
        if not primary_major:
            return "Please select a primary major."
        if lang is None:
            return "Please enter the language you wish to take or indicate that this requirement is not applicable."

        # Build output messages
        output = []
        if degree_type == "double": 
            do_it = make_a_schedule(primary_major,lang, secondary_major, study_abroad= abroad, credits = credits)
            schedule = do_it.compile()
            creds = do_it.get_credits()
            output.append(f"Schedule has {creds} credits in it")
            output.append("Courses to take: ")
            for i in schedule: 
                output.append(f"course: {i['course_code']}; credits: {i['credits']}; tag: {i['tag']}")

        elif degree_type =='major-minor':
            do_it = make_a_schedule(primary_major,lang, minor= minor, study_abroad= abroad, credits = credits)
            schedule = do_it.compile()
            creds = do_it.get_credits()
            output.append(f"Schedule has {creds} credits in it")
            output.append("Courses to take: ")
            for i in schedule: 
                output.append(f"course: {i['course_code']}; credits: {i['credits']}; tag: {i['tag']}")

        else: 
            do_it = make_a_schedule(primary_major,lang, study_abroad= abroad, credits = credits)
            schedule = do_it.compile()
            creds = do_it.get_credits()
            output.append(f"Schedule has {creds} credits in it")
            output.append("Courses to take: ")
            for i in schedule: 
                output.append(f"course: {i['course_code']}; credits: {i['credits']}; tag: {i['tag']}")

        # Return final output
        return html.Div([html.P(line) for line in output])
        return [html.P(item) for item in output]

    return ""

if __name__ == '__main__':
    app.run(debug=True)
