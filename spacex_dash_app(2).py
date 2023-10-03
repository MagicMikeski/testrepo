import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Calculate the maximum and minimum payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    
    html.Br(),
    
    dcc.Graph(id='success-pie-chart'),
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]),
    
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Define callbacks to update the charts based on user input
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='class', title='Total Success Launches By Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Total Success Launches for Site {selected_site}'
        fig = px.pie(filtered_df, names='class', title=title)
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        filtered_site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_site_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Correlation between Payload and Success for Site {selected_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Calculate the maximum and minimum payload values
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    
    html.Br(),
    
    dcc.Graph(id='success-pie-chart'),
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: str(i) for i in range(0, 10001, 1000)},
                    value=[min_payload, max_payload]),
    
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Define callbacks to update the charts based on user input
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='class', title='Total Success Launches By Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for Site {selected_site}')
    return fig

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        low, high = payload_range
        df = spacex_df
        mask = (df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)
        fig = px.scatter(df[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         size='Payload Mass (kg)', hover_data=['Payload Mass (kg)'])
        fig.update_layout(title='Correlation between Payload and Success for all Sites')
    else:
        low, high = payload_range
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        mask = (df['Payload Mass (kg)'] >= low) & (df['Payload Mass (kg)'] <= high)
        fig = px.scatter(df[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         size='Payload Mass (kg)', hover_data=['Payload Mass (kg)'])
        fig.update_layout(title=f'Correlation between Payload and Success for Site {selected_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)