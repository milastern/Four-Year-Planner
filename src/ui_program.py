import dash
from dash import dcc, html, Input, Output, callback_context as ctx
import numpy as np
import os
import plotly.express as px
from src.get_courses import make_a_schedule
import matplotlib.pyplot as plt
import io
import base64 
from IPython.display import Image
import dash_bootstrap_components as dbc


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets= [dbc.themes.COSMO])

# Load data for majors and minors from files
major_filepath = os.path.join("data", "majors_list.npy")
all_majors = np.load(major_filepath, allow_pickle=True).tolist()
minor_filepath = os.path.join("data", "minors_list.npy")
minors = np.load(minor_filepath, allow_pickle=True).tolist()
langs = ['N/A','spanish', 'french', 'arabic', 'chinese', 'italian', 'german', 'japanese', 'russian']
ops = ["I am planning on doing a semester abroad", "I am not planning on doing a semester abroad, but I might still study abroad", "I am not planning on studying abroad"]

# Layout of the app
app.layout = html.Div(
    style = {"border": "3px solid black",      # thickness, style, and color
        "padding": "20px",                # space inside the border
        "margin": "20px",                 # space outside the border
        "height": "95vh",                 # fill most of the viewport height
        "boxSizing": "border-box"         # include padding in height
    },
    children = [
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
        
        html.Div(id='output-div') ] # Placeholder for the chart or user feedback 

) 

# Callback to dynamically update dropdown visibility and options
@app.callback(
    [Output('dropdown-secondary-major-container', 'style'),
     Output('dropdown-minor-container', 'style'),
     Output('dropdown-secondary-major', 'options')],
    [Input('degree-type', 'value'),
     Input('dropdown-primary-major', 'value')]
)
def update_dropdown_visibility(degree_type: str, 
                               primary_major: str) -> tuple:
    """
    Dynamically updates the visibility and options of the secondary major and minor dropdowns
    based on the selected degree type and primary major.

    Args:
        degree_type (str): The selected degree type ('single', 'double', 'major-minor').
        primary_major (str): The selected primary major.

    Returns:
        tuple: The updated styles for the secondary major and minor dropdowns, and the secondary major options.
    """
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
def handle_submission(primary_major:  str, 
                      lang: str, 
                      abroad: str, 
                      secondary_major: str, 
                      minor: str, 
                      credits: int, 
                      degree_type: str, 
                      n_clicks: int) -> html:
    """
    Handles the submission of user preferences, generates the personalized schedule, and displays it.

    Args:
        primary_major (str): The selected primary major.
        lang (str): The selected language.
        abroad (str): The selected study abroad preference.
        secondary_major (str): The selected secondary major (if applicable).
        minor (str): The selected minor (if applicable).
        credits (int): The number of credits already earned by the student.
        degree_type (str): The selected degree type ('single', 'double', 'major-minor').
        n_clicks (int): The number of times the submit button has been clicked.

    Returns:
        html.Div: The HTML div containing the generated course schedule.
    """
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

        elif degree_type =='major-minor':
            do_it = make_a_schedule(primary_major,lang, minor= minor, study_abroad= abroad, credits = credits)   

        else: 
            do_it = make_a_schedule(primary_major,lang, study_abroad= abroad, credits = credits)
        
        buf = io.BytesIO()
        do_it.make_chart(output=buf)  # Modify make_chart to accept a buffer instead of saving to file
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        src = f'data:image/png;base64,{encoded_image}'

        return html.Div([
            html.H1("Course Schedule"),
            html.Img(src=src, style={'width': '60%', 'height': 'auto'})
        ])
       
    return ""

if __name__ == '__main__':
    app.run(debug=True)
