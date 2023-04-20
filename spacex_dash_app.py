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
allSites = {'All Sites': 'ALL'}
sites_list = spacex_df['Launch Site'].unique().tolist()
for site in sites_list:
    allSites[site] = site



# Create a dash application
app = dash.Dash(__name__)
#app.enable_dev_tools


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)

                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': key, 'value': value} for key, value in allSites.items()
                                ],
                                    placeholder='Select a launch site',
                                    value = 'ALL',
                                    style={'align-items': 'center','font-size': 20, 'width': '100%', 'padding': 3},
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                #marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                marks={i: str(i) for i in range (0,10000,2500)},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    #auto_data[auto_data['drive-wheels']==value].groupby(['drive-wheels','body-style'],as_index=False)['price']
    #filtered_df = spacex_df.groupby(['Launch Site'], as_index=False)['class']
    filtered_df = spacex_df[spacex_df['class']==1].groupby(['Launch Site', 'class'], as_index=False)['class'].count()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Sucess Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby(['class'], as_index=False)['class'].count()
        fig = px.pie(filtered_df, values='class', 
        names='class', 
        title='Total Sucess Launches By Site')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(entered_site, payload_range):
    min_p = payload_range[0]
    max_p = payload_range[1]
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=min_p) & (spacex_df['Payload Mass (kg)']<=max_p)]

    if entered_site == 'ALL':
        fig2 = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
        title='Correlation between Payload and Success for all Sites',
        color="Booster Version Category")
        #print(filtered_df)
        return fig2
    else:
        graph_title = 'Correlation between Payload and Success for site ' + entered_site
        #print(payload_range)
        filtered_df = filtered_df[(filtered_df['Launch Site']==entered_site)] 
        #print(filtered_df)
        fig2 = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
        title=graph_title,
        color="Booster Version Category")
        return fig2





# Run the app
if __name__ == '__main__':
    #app.run_server()
    app.run_server(debug=True)
