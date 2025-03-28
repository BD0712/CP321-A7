import dash
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State 


# Creating a DataFrame for the World Cup winners
data = {
    "Year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 
             1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    
    "Winners": ["Uruguay", "Italy", "Italy", "Uruguay", "Germany", "Brazil", 
                "Brazil", "England", "Brazil", "Germany", "Argentina", 
                "Italy", "Argentina", "Germany", "Brazil", "France", 
                "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"],

    "Runners-up": ["Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", 
                   "Sweden", "Czechoslovakia", "Germany", "Italy", "Netherlands", 
                   "Netherlands", "Germany", "Germany", "Argentina", "Italy", 
                   "Brazil", "Germany", "France", "Netherlands", "Argentina", 
                   "Croatia", "France"],

    "ISO3_Winners": ["URY", "ITA", "ITA", "URY", "DEU", "BRA", 
                     "BRA", "GBR", "BRA", "DEU", "ARG", 
                     "ITA", "ARG", "DEU", "BRA", "FRA", 
                     "BRA", "ITA", "ESP", "DEU", "FRA", "ARG"],

    "ISO3_Runners-up": ["ARG", "CSK", "HUN", "BRA", "HUN", 
                        "SWE", "CSK", "DEU", "ITA", "NLD", 
                        "NLD", "DEU", "DEU", "ARG", "ITA", 
                        "BRA", "DEU", "FRA", "NLD", "ARG", 
                        "HRV", "FRA"]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)




#winners = df3["Winners"]
#print(winners)


# Create the choropleth map using Plotly Express.
fig = px.choropleth(
    df,
    locations="ISO3_Winners",
    color="Winners",
    hover_name="Winners",
    hover_data=["Year"],
    color_continuous_scale="Viridis",
    title="FIFA World Cup Winners by Country"
)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Winners and Runner-ups Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown menus at the top
    html.Div([
        html.Div([
            html.Label("Select a Country:", style={'color': 'red', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} 
                         for country in sorted(df['Winners'].unique())],
                placeholder="Select a country"
            ),
            html.Div(id='country-output', style={'marginTop': 10, 'fontWeight': 'bold', 'color': 'red'})
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '0 20px'}),
        
        html.Div([
            html.Label("Select a Year:", style={'color': 'red', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} 
                         for year in sorted(df['Year'].unique())],
                placeholder="Select a year"
            ),
            html.Div(id='year-output', style={'marginTop': 10, 'fontWeight': 'bold', 'color': 'red'})
        ], style={'width': '45%', 'display': 'inline-block', 'padding': '0 20px'})
    ], style={'textAlign': 'center', 'padding': '20px 0'}),
    
    # Choropleth map placed below the dropdowns
    dcc.Graph(figure=fig)
])

# Callback to update the country output: number of times the selected country has won.
@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country(selected_country):
    if not selected_country:
        return ""
    wins = df[df['Winners'] == selected_country].shape[0]
    return f"{selected_country} has won the World Cup {wins} time{'s' if wins != 1 else ''}."

# Callback to update the year output: show winner and runner-up for the selected year.
@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year(selected_year):
    if not selected_year:
        return ""
    row = df[df['Year'] == selected_year]
    if row.empty:
        return "No data available for the selected year."
    winner = row.iloc[0]['Winners']
    runner_up = row.iloc[0]['Runners-up']
    return f"In {selected_year}, the winner was {winner} and the runner-up was {runner_up}."


app.run(debug=True)