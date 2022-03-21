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
launch_site_df =spacex_df.groupby(['Launch Site'],as_index=False).first()
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(['Launch Sites: ',dcc.Dropdown(id='site-dropdown',options=[
                                         {'label':'All Sites','value':'ALL'},
                                         {'label': launch_site_df.loc[0,'Launch Site'], 'value': launch_site_df.loc[0,'Launch Site']},
                                         {'label': launch_site_df.loc[1,'Launch Site'], 'value': launch_site_df.loc[1,'Launch Site']},
                                         {'label': launch_site_df.loc[2,'Launch Site'], 'value': launch_site_df.loc[2,'Launch Site']},
                                         {'label': launch_site_df.loc[3,'Launch Site'], 'value': launch_site_df.loc[3,'Launch Site']}
                                        ],value='ALL',placeholder='Select a Launch Site here',searchable=True)],style={'font-size':18,'width':'50%'}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
Input(component_id='site-dropdown',component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':

        fig=px.pie(spacex_df,values='class',names='Launch Site',title='Pie Chart')
        return fig
    else:
        launch_df=spacex_df.groupby(['Launch Site','class'],as_index=False).count()
        launch_df=launch_df[launch_df['Launch Site']==entered_site]
        launch_df['count']=launch_df['Mission Outcome']
        launch_df.loc[(launch_df['class']==0),'Outcomes']='Launch Failure'
        launch_df.loc[(launch_df['class']==1),'Outcomes']='Successful Launch'
        # title = 'Pie chart for'+ entered_site
        fig= px.pie(launch_df,values='count',names='Outcomes',title='Pie chart for ' + str(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
[Input(component_id='site-dropdown',component_property='value'),
Input(component_id='payload-slider',component_property='value')])
def get_scatter_plot(site,payload_slider):
    low,high = payload_slider
    if site == 'ALL':
        mask = (spacex_df['Payload Mass (kg)']>low) & (spacex_df['Payload Mass (kg)']< high)
        fig_1=px.scatter(spacex_df[mask],x='Payload Mass (kg)',y='class',color='Booster Version')
        return fig_1
    else:
        spacex_df_1=spacex_df[spacex_df['Launch Site']==site]
        mask = (spacex_df_1['Payload Mass (kg)']>low) & (spacex_df_1['Payload Mass (kg)']< high)
        fig_1=px.scatter(spacex_df_1[mask],x='Payload Mass (kg)',y='class',color='Booster Version')
        return fig_1

# Run the app
if __name__ == '__main__':
    app.run_server()
