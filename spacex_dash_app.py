# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                #dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',  # Unique identifier for the dropdown
                                    options=[
                                    {'label': 'All Sites', 'value': 'ALL'},  # Default option to show all sites
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},  # Replace 'site1' with actual launch site names
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},  # Add more options as needed
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},],
                                    value='ALL',  # Default value when the page loads, showing data for all sites
                                    placeholder="Select a Launch Site here",  # Text description for the dropdown
                                    searchable=True  # Allow users to enter keywords to search launch sites
                                    ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',  # Unique identifier for the RangeSlider
                                    min=0,  # Slider starting point (in Kg)
                                    max=10000,  # Slider ending point (in Kg)
                                    step=1000,  # Slider interval (in Kg)
                                    marks={0: '0', 10000: '10000'},  # Marks to indicate values on the slider
                                    value=[min_payload, max_payload]  # Current selected range
                                    ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Callback function to update the pie chart based on site selection
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
        
    # Check if ALL sites are selected
    if entered_site == 'ALL':
        fig = px.pie(filtered_df,names='class', title='Total Success Launches')
    else:
        # If a specific launch site is selected, filter the dataframe for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Create a pie chart for the selected site showing success and failure counts
        fig = px.pie(filtered_df, names='class', title=f'Success and Failure Count for {entered_site}')
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Callback function to update the scatter plot based on site selection and payload range
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def update_scatter_chart(selected_site, selected_payload_range):
    # Filter the dataframe based on the selected site
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Filter the dataframe based on the selected payload range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= selected_payload_range[0]) & 
                              (filtered_df['Payload Mass (kg)'] <= selected_payload_range[1])]
    
    # Create scatter plot with Payload Mass (kg) on the x-axis, class on the y-axis, and color by Booster Version
    scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                             title='Payload vs. Launch Outcome', labels={'class': 'Launch Outcome'})
    
    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8052)
