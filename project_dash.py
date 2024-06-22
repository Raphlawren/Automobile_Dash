import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv")

year_list = [i for i in range(1980, 2024)]
app.layout = html.Div(children=[
    html.H1('Automobile Sales Statistics for Year 1980 - 2013',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    dcc.Dropdown(id='dropdown-statistics',
                 options=[
                     {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                     {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                 ],
                 placeholder='Select a report type', value='Select Statistics',
                 style={'textAlign': 'center', 'width': '80%', 'height': '3px', 'font-size': '20px'}),

    dcc.Dropdown(id='select-year',
                 options=[{'label': i, 'value': i} for i in year_list],
                 placeholder='Select year',
                 style={'textAlign': 'center', 'width': '80%', 'height': '3px', 'font-size': '20px'}),

    html.Div([
        html.Div(id='output-container', className='chart-grid',
                 style={'display': 'flex'}),
    ])
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='dropdown-statistics', component_property='value'), 
    Input(component_id='select-year', component_property='value')
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales during Recession'))

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        avg_veh = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_veh, x='Vehicle_Type', y='Automobile_Sales', title='Number of cars sold by Vehicle Type'))

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', 
                          title='Expenditure share by vehicle type during recessions'))

        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        un_vh = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(un_vh, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'}, 
                          title='Effect of Unemployment rate on Vehicles & Sales'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], 
                     style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], 
                     style={'display': 'flex'})
        ]

    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = df[df['Year'] == input_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales'))
        
        #Plot 2: Total Monthly Automobile sales using line chart.
        
        mas = df.groupby('Month')['Automobile_Sales'].mean().reset_index()
        
        Y_chart2 = dcc.Graph(
            px.line(mas, x= 'Month', y='Automobile_Sales', title='Monthly Automobile Sales'))
        
        # Plot 3: Plot bar chart for average number of vehicles sold during the given year
        
        avr_vsa = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        
        Y_chart3 = dcc.Graph(
            figure =px.bar(avr_vsa, x='Year', y='Automobile_Sales', title='Average Number of Vehicle sold during the year'))
        
        # plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        
        tas = df.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        
        Y_chart4 = dcc.Graph(
            figure=px.pie(tas, 
                          values='Advertising_Expenditure',
                          names= 'Vehicle_Type',
                          title= 'Total Advertisment Expenditure for Each Vehicle')
        )
        return [
            html.Div(className='chart-item', children=[html.Div(children= Y_chart1), html.Div(children=Y_chart2)], style={'display':'flex'}),
            html.Div(className='chart-item', children=[html.Div(children= Y_chart3), html.Div(children=Y_chart4)], style={'display':'flex'})
            
        ]
        
if __name__ == '__main__':
    app.run_server(debug=True)
