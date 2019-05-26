#Python Script---------------------------------------------------------------------------------------------------------------------------
#Title: Webpage
# coding: utf-8
#----------------------------------------------------------------------------------------------------------------------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from components import Header,get_logo, get_header, get_menu, make_dash_table, print_button
from PerformanceAnalyticsSDK import Performance

import pandas as pd

import datetime 
import math
import numpy as np
import scipy
from scipy.stats import trim_mean, kurtosis
from scipy.stats.mstats import mode, gmean, hmean
from scipy.stats import norm
from pandas.tseries.offsets import BDay

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

server = app.server

# read data
DB_Stock_Info = pd.read_csv("data/DB_Stock_Info.csv", sep = ";")

#The Dropdown Menue excludes Alcon because this company has only been included in the SMI in the past month
#We will include Alcon as soons as more data is available
DB_Dropdown = pd.read_csv("data/DB_Dropdown.csv", sep = ";")


#The following Definitions: overview, pricePerformance, riskMeasures, technicalAnalysis and noPage are used
#for the UI of the Webpage
overview = html.Div([  # page 1

            print_button(),
                        
            html.Div([
                            #Header
                            html.Div([     
                                    get_logo(app),                                              
                                    html.Div([html.Div([html.H5(html.Div(id='StockName_Tab1'))], className="twelve columns padded")],
                                              className="row gs-header gs-text-header"),
                                    
                                              html.Br([]),
                                    get_menu()
                                    ]),    #End #Header
                
                            # Row 1
                            html.Div([
                                    html.H6('Summary',
                                            className="gs-header gs-text-header padded"),
                                    html.Br([]),            
                                    
                                    html.P(id='Description'), 
                
                                        ], className="row"),  #End of Row 1
                
                            # Row 2
                            html.Div([
                
                                html.Div([
                                    html.H6('Cumulative Performance',
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph(id='Fig_Cumulative_Annual_Performance'),
                                         ], className="six columns"),
                
                                html.Div([
                                    html.H6("Hypothetical growth of $10,000",
                                            className="gs-header gs-table-header padded"),
                                            dcc.Graph(id='Fig_Hypothetical_Growth'),
                                
                                         ], className="six columns"),
                
                                ], className="row "), #End of Row 2
                                                     
                            #Row 3 
                            html.Div([ 
                                    html.H6(['Price Performance'],
                                            className="gs-header gs-text-header padded"),
                                            html.Div(id='Tab_Price_Performance'),
         
                                            ], className="row"),  #End of Row 3
                
                            #row 4
                            html.Div([
                
                                html.Div([
                                    html.H6('Average Annual Performance',
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph(id='Fig_Average_Performance'),
                                         ], className="six columns"),
                
                                html.Div([
                                    html.H6("Risk-Return Potential",
                                            className="gs-header gs-table-header padded"),
                                            dcc.Graph(id='Fig_Risk_Potential'),
                                
                                         ], className="six columns"),
                
                                ], className="row "), #End of Row 4
                                                                                                                  
                        ], className="subpage")
        ], className="page")

   
#------------------------------------------------------------------------------------------------------------------------------------  
pricePerformance = html.Div([  #page 2
            print_button(),
                        
            html.Div([ #subpage
                            #Header
                            html.Div([     
                                    get_logo(app),         
                                    html.Div([html.Div([html.H5(html.Div(id='StockName_Tab1'))], className="twelve columns padded")],
                                              className="row gs-header gs-text-header"),
                                    
                                    html.Br([]),
                                    get_menu()
                                    ]),    #End #Header
                            
                            
                            # Row 1
                            html.Div([
                                html.Div([ #Left Column
                                    html.H6(['Current Statistics'],
                                            className="gs-header gs-text-header padded"),
                                            html.Div(id='Tab_Current_Statistics'),
                                            ], className="six columns"),  #End Left Column
                
                                html.Div([ #Right Column
                                    html.H6("Historic Prices",
                                            className="gs-header gs-table-header padded"),
                                            html.Div(id='Tab_Historic_Prices'),
                                         ], className="six columns"), #End right Column
                
                                ], className="row "), #End of Row 1
                                    
                            
                            # Row 2
                            html.Div([
                                    html.H6(['Price Development'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_Price_Development")
                                ] , className="row "), #End Row 2 
                                    
                                    
                            # Row 3
                            html.Div([
                                    html.H6(['Returns'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_Returns")
                                ] , className="row "), #End Row 3 
                                    

                            #Row 4  
                            html.Div([ 
                                    html.H6(['Key Ratios'],
                                            className="gs-header gs-text-header padded"),
                                            html.Div(id='Tab_Key_Ratios')
                                ], className="row"), #End Row 4 
                                                      
        ], className="subpage")
    ], className="page")
    


#------------------------------------------------------------------------------------------------------------------------------------      
riskMeasures = html.Div([  #page 3
            print_button(),
                        
            html.Div([ #subpage
                            #Header
                            html.Div([     
                                    get_logo(app),         
                                    html.Div([html.Div([html.H5(html.Div(id='StockName_Tab1'))], className="twelve columns padded")],
                                              className="row gs-header gs-text-header"),
                                    
                                    html.Br([]),
                                    get_menu()
                                    ]),    #End #Header
                            
                            
                            # Row 1
                            html.Div([
                                html.Div([ #Left Column
                                    html.H6(['Risk Measures'],
                                            className="gs-header gs-text-header padded"),
                                            html.Div(id='Tab_Risk_Measures1'),
                                            ], className="six columns"),  #End Left Column
                
                                html.Div([ #Right Column
                                    html.H6("Risk Measures",
                                            className="gs-header gs-table-header padded"),
                                            html.Div(id='Tab_Risk_Measures2'),
                                         ], className="six columns"), #End right Column
                
                                ], className="row "), #End of Row 1
                                    
                            
                            # Row 2
                            html.Div([
                                    html.H6(['Value at Risk (VaR)'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_Value_at_risk")
                                ] , className="row "), #End Row 2 
                                    
                                    
                            # Row 3
                            html.Div([
                                    html.H6(['Expected Shortfall (ES)'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_Expected_Shortfall")
                                ] , className="row "), #End Row 3 
                                    

                            #Row 4  
                            html.Div([
                                    html.H6(['Drawdown'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_Drawdown")
                                ] , className="row "), #End Row 3 
                                                      
        ], className="subpage")
    ], className="page")
              
                                   
#------------------------------------------------------------------------------------------------------------------------------------  
technicalAnalysis = html.Div([  #page 4
            print_button(),
                        
            html.Div([ #subpage
                            #Header
                            html.Div([     
                                    get_logo(app),         
                                    html.Div([html.Div([html.H5(html.Div(id='StockName_Tab1'))], className="twelve columns padded")],
                                              className="row gs-header gs-text-header"),
                                    
                                    html.Br([]),
                                    get_menu()
                                    ]),    #End #Header
                            
                            # Row 1
                            html.Div([
                                    html.H6(['Technical Analysis'],
                                            className="gs-header gs-text-header padded"),
                                            html.Div(id='Tab_Technical_Analysis')
                                ] , className="row "), #End Row 1
                                    
                            # Row 2
                            html.Div([
                                    html.H6(['Bollinger Bands'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_Bollinger_Bands")
                                ] , className="row "), #End Row 2 
                                    
                                    
                            # Row 3
                            html.Div([
                                    html.H6(['RSI'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_RSI")
                                ] , className="row "), #End Row 3 
                                    

                            #Row 4  
                            html.Div([
                                    html.H6(['Aroon Indicator'],
                                            className="gs-header gs-text-header padded"),
                                            dcc.Graph("Fig_Aroon_Indicator")
                                ] , className="row "), #End Row 3 
                                                      
        ], className="subpage")
    ], className="page")
              

#------------------------------------------------------------------------------------------------------------------------------------                  
noPage = html.Div([  # 404

    html.P(["404 Page not found"])

    ], className="no-page")


#------------------------------------------------------------------------------------------------------------------------------------  
#layout / UI of the app (This defines how the app should look like when it is opened in the browser)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
   
    #Header
    html.Div([     
            get_logo(app), 
            html.Div([
                    html.P('Important Information: As the calculations are done ad hoc it can take one minute to load. After changing the Tab please press Submit again to load the data.')
                    ]),
            html.Div([
                     dcc.Loading(id="loading", children=[html.Div(id="loading-output")], type="default")
                    ]),
            dcc.Dropdown(id='input-dropdown-tab-1',
                         options=[dict(label = element, value = element) for element in DB_Dropdown["Reuters"]],
                         placeholder = "Select Company",
                         className="no-print", style={'width': '40%','display': 'inline-block'}), 
            html.Div([
                     html.Button('Submit', id='button'), 
                    ]),
            ]),    #End #Header
    html.Div(id='page-content')
])
#------------------------------------------------------------------------------------------------------------------------------------                                       

# # # # # # # # #
# Update page using callback functions
#This callback returns the page dependent on which Tab one has opened
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/dash-report/overview':
        return overview
    elif pathname == '/dash-report/pricePerformance':
        return pricePerformance
    elif pathname == '/dash-report/riskMeasures':
        return riskMeasures
    elif pathname == '/dash-report/technicalAnalysis':
        return technicalAnalysis
    elif pathname == '/dash-report/full-view':
        return overview,pricePerformance,riskMeasures, technicalAnalysis
    else:
        return noPage
    

#This callback function returns all the tables and figures based on the company chosen
@app.callback([Output('loading-output', 'children'),
               Output('StockName_Tab1', 'children'),
               Output('Description', 'children'),
               Output('Fig_Cumulative_Annual_Performance', 'figure'),
               Output('Tab_Price_Performance', 'children'),
               Output('Fig_Hypothetical_Growth', 'figure'),
               Output('Fig_Average_Performance', 'figure'),
               Output('Fig_Risk_Potential', 'figure'),
               Output('Tab_Current_Statistics', 'children'),
               Output('Tab_Historic_Prices', 'children'),
               Output('Fig_Price_Development', 'figure'),
               Output('Fig_Returns', 'figure'),
               Output('Tab_Key_Ratios', 'children'),
               Output('Tab_Risk_Measures1', 'children'),
               Output('Tab_Risk_Measures2', 'children'),
               Output('Fig_Value_at_risk', 'figure'),
               Output('Fig_Expected_Shortfall', 'figure'),
               Output('Fig_Drawdown', 'figure'),
               Output('Tab_Technical_Analysis', 'children'),
               Output('Fig_Bollinger_Bands', 'figure'),
               Output('Fig_RSI', 'figure'),
               Output('Fig_Aroon_Indicator', 'figure')],

              [Input('input-dropdown-tab-1', 'value'),
               Input('button', 'n_clicks')])
def update_output(input, button):
    Loading = u'Loading Finished'
    StockName = u'Stock Analysis of {}'.format(input)
    Description = DB_Stock_Info["Company Description"][DB_Stock_Info["Reuters"]==input].get_values()[0]  
    
    #Download Data
    #The following lines of code download the Data from our Web API and assign them to variables to use them later
    #Overview: Stock
    Performance_Stock = Performance(Reuters = input)
    Cumulative_Annual_Performance =  Performance_Stock.df_annual_perf
    Price_Performance =  Performance_Stock.df_Price_Performance
    Hypothetical_growth =  Performance_Stock.df_hypothetical_growth
    Average_Annual_Performance =  Performance_Stock.df_annual_perf_average
    Risk_Potential =  Performance_Stock.SR_q
    
    #Price Performance: Stock
    Current_Statistics =  Performance_Stock.df_Current_Statistic
    Historic_Prices =  Performance_Stock.df_Historic_Prices
    Price_Development = Performance_Stock.df_Performance_Graph 
    Returns = Performance_Stock.df_Return_Graph
    Key_Ratios = Performance_Stock.df_Key_Ratios
    
    #Risk Measures: Stock
    Risk_Measures1 = Performance_Stock.df_Risk_Measure1
    Risk_Measures2 = Performance_Stock.df_Risk_Measure2
    VaR = Performance_Stock.df_VaR
    ES = Performance_Stock.df_ES
    Drawdown = Performance_Stock.df_Max_Daily_Drawdown
    
    #Technical Analysis: Stock
    TechnicalAnalysis = Performance_Stock.df_TechnicalAnalysis
    BollingerBands = Performance_Stock.df_BollingerBands
    RSI = Performance_Stock.df_RSI
    AroonIndicator = Performance_Stock.df_AroonIndicator
         
    #Overview: SSMI
    Performance_SMI = Performance(Reuters = "SSMI")
    Cumulative_Annual_Performance_SMI =  Performance_SMI.df_annual_perf
    Price_Performance_SMI =  Performance_SMI.df_Price_Performance
    Hypothetical_growth_SMI =  Performance_SMI.df_hypothetical_growth
    Average_Annual_Performance_SMI =  Performance_SMI.df_annual_perf_average
    #Risk_Potential_SMI =  Performance_SMI.SR_q
    
    #Price Performance: SSMI
    #Current_Statistics_SMI =  Performance_SMI.df_Current_Statistic
    #Historic_Prices_SMI =  Performance_SMI.df_Historic_Prices
    #Price_Development_SMI = Performance_SMI.df_Performance_Graph 
    Returns_SMI = Performance_SMI.df_Return_Graph
    
    #Risk Measures: SSMI
    #Risk_Measures1_SMI = Performance_SMI.df_Risk_Measure1
    #Risk_Measures2_SMI = Performance_SMI.df_Risk_Measure2
    VaR_SMI = Performance_SMI.df_VaR
    ES_SMI = Performance_SMI.df_ES
    Drawdown_SMI = Performance_SMI.df_Max_Daily_Drawdown
    
    #Technical Analysis: SSMI
    #TechnicalAnalysis_SMI = Performance_Stock.df_TechnicalAnalysis
    #BollingerBands_SMI = Performance_Stock.df_BollingerBands
    #SI_SMI = Performance_Stock.df_RSI
    #AroonIndicator_SMI = Performance_Stock.df_AroonIndicator
    
    #----------------------------------------------------------------------------------------------------
    #Overview: Create Figure Cumulative Annual Performance
    Fig_Cumulative_Annual_Performance = {
                        'data': [
                                go.Bar(
                                    x = ["1 Month", "1 Year", "3 Year", "5 Year", "10 Year"],
                                    y = Cumulative_Annual_Performance["Price"],
                                    marker = {
                                      "color": "rgb(53, 83, 225)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                      }
                                    },
                                    name = str(input)
                                ),
                                go.Bar(
                                    x = ["1 Month", "1 Year", "3 Year", "5 Year", "10 Year"],
                                    y = Cumulative_Annual_Performance_SMI["Price"],
                                    marker = {
                                      "color": "rgb(192, 192, 192)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                      }
                                    },
                                    name = "SSMI"
                                ),
                            ],
                        'layout': go.Layout(
                                autosize = False,
                                bargap = 0.35,
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                hovermode = "closest",
                                legend = {
                                  "x": -0.0228945952895,
                                  "y": -0.189563896463,
                                  "orientation": "h",
                                  "yanchor": "top"
                                },
                                margin = {
                                  "r": 0,
                                  "t": 20,
                                  "b": 10,
                                  "l": 30
                                },
                                showlegend = True,
                                title = "",
                                width = 320,
                                xaxis = {
                                  "autorange": True,
                                  #"range": [-0.5, 4.5],
                                  "showline": True,
                                  "title": "",
                                  "type": "category"
                                },
                                yaxis = {
                                  "autorange": True,
                                  #"range": [0, 22.9789473684],
                                  "showgrid": True,
                                  "showline": True,
                                  "title": "Return",
                                  "type": "linear",
                                  "zeroline": False
                                }
                            )
            }
    
    
    #Overview: Create Table Price Performance
    Months = {
        'Name':  ["Placeholder"],
        '1 month':  ['1 month'],
        '1 Years': ['1 Year'],
        '3 Years': ['3 Years'],
        '5 Years': ['5 Years'],
        '10 Years': ['10 Years'],
        'Since Inception': ['Since Inception'],
        }
    Text = pd.DataFrame(Months, columns = ['1 month','1 Years', '3 Years', '5 Years', '10 Years', 'Since Inception'])
    Tab_Price_Performance = Price_Performance.append(Price_Performance_SMI)
    Tab_Price_Performance = round(Tab_Price_Performance*100,2).astype(str) + '%'
    
    Tab_Price_Performance = pd.concat([Text, Tab_Price_Performance], ignore_index=True)
    
    new_col = ["", str(input), "SSMI"]
    Tab_Price_Performance.insert(loc=0, column='Names', value=new_col)
                       
    Tab_Price_Performance = html.Table(make_dash_table(Tab_Price_Performance))
    
    
    #Overview: Create Figure Hypothetical Growth
    Fig_Hypothetical_Portfolio = {
                            'data': [
                                go.Scatter(
                                    x = Hypothetical_growth["Date"],
                                    y = Hypothetical_growth["Value"], 
                                    line = {"color": "rgb(53, 83, 255)"},
                                    mode = "lines",
                                    name = str(input)
                                ),
                                go.Scatter(
                                    x = Hypothetical_growth_SMI["Date"],
                                    y = Hypothetical_growth_SMI["Value"], 
                                    line = {"color": "rgb(192, 192, 192)"},
                                    mode = "lines",
                                    name = "SSMI"
                                )
                            ],
                            'layout': go.Layout(
                                autosize = False,
                                title = "",
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                width = 320,
                                hovermode = "closest",
                                legend = {
                                  "x": -0.0277108433735,
                                  "y": -0.142606516291,
                                  "orientation": "h"
                                },
                                margin = {
                                  "r": 20,
                                  "t": 20,
                                  "b": 20,
                                  "l": 50
                                },
                                showlegend = True,
                                xaxis = {
                                  "autorange": False,
                                  "linecolor": "rgb(0, 0, 0)",
                                  "linewidth": 1,
                                  "range": [2006, 2019],
                                  "showgrid": False,
                                  "showline": True,
                                  "title": "",
                                  "type": "linear"
                                },
                                yaxis = {
                                  "autorange": True,
                                  "gridcolor": "rgba(127, 127, 127, 0.2)",
                                  "mirror": False,
                                  "nticks": 4,
                                  #"range": [0, 30000],
                                  "showgrid": True,
                                  "showline": True,
                                  "ticklen": 10,
                                  "ticks": "outside",
                                  "title": "$",
                                  "type": "linear",
                                  "zeroline": False,
                                  "zerolinewidth": 4
                                }
                            )
                        }
                            
       
    #Overview: Create Figure Average Annual Performance
    Fig_Average_Annual_Performance = {
                        'data': [
                                go.Bar(
                                    x = ["1 Month", "1 Year", "3 Year", "5 Year", "10 Year"],
                                    y = Average_Annual_Performance["Price"],
                                    marker = {
                                      "color": "rgb(53, 83, 225)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                      }
                                    },
                                    name = str(input)
                                ),
                                go.Bar(
                                    x = ["1 Month", "1 Year", "3 Year", "5 Year", "10 Year"],
                                    y = Average_Annual_Performance_SMI["Price"],
                                    marker = {
                                      "color": "rgb(192, 192, 192)",
                                      "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2
                                      }
                                    },
                                    name = "SSMI"
                                ),
                            ],
                        'layout': go.Layout(
                                autosize = False,
                                bargap = 0.35,
                                font = {
                                  "family": "Raleway",
                                  "size": 10
                                },
                                height = 200,
                                hovermode = "closest",
                                legend = {
                                  "x": -0.0228945952895,
                                  "y": -0.189563896463,
                                  "orientation": "h",
                                  "yanchor": "top"
                                },
                                margin = {
                                  "r": 30,
                                  "t": 20,
                                  "b": 10,
                                  "l": 30
                                },
                                showlegend = True,
                                title = "",
                                width = 320,
                                xaxis = {
                                  "autorange": True,
                                  #"range": [-0.5, 4.5],
                                  "showline": True,
                                  "title": "",
                                  "type": "category"
                                },
                                yaxis = {
                                  "autorange": True,
                                  #"range": [0, 22.9789473684],
                                  "showgrid": True,
                                  "showline": True,
                                  "title": "Return",
                                  "type": "linear",
                                  "zeroline": False
                                }
                            )
            }    
                        
    #Overview: Create Figure Risk Potential
    Fig_Risk_Potential = {
                            'data': [
                                go.Scatter(
                                    x = ["0", "0.18", "0.18", "0"],
                                    y = ["0.2", "0.2", "0.4", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.2)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "B",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.2", "0.38", "0.38", "0.2", "0.2"],
                                    y = ["0.2", "0.2", "0.6", "0.4", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.4)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "D",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.4", "0.58", "0.58", "0.4", "0.4"],
                                    y = ["0.2", "0.2", "0.8", "0.6", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.6)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "F",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.6", "0.78", "0.78", "0.6", "0.6"],
                                    y = ["0.2", "0.2", "1", "0.8", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgba(31, 119, 180, 0.8)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "H",
                                    showlegend = False
                                ),
                                go.Scatter(
                                    x = ["0.8", "0.98", "0.98", "0.8", "0.8"],
                                    y = ["0.2", "0.2", "1.2", "1", "0.2"],
                                    fill = "tozerox",
                                    fillcolor = "rgb(31, 119, 180)",
                                    hoverinfo = "none",
                                    line = {"width": 0},
                                    mode = "lines",
                                    name = "J",
                                    showlegend = False
                                ),
                            ],
                            'layout': go.Layout(
                                title = "",
                                annotations = [
                                    {
                                      "x": Risk_Potential, 
                                      "y": 0.58,
                                      "font": {
                                        "color": "rgb(153, 0, 0)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": str(input),
                                      "xref": "x",
                                      "yref": "y"
                                    },
                                    {
                                      "x": 0.09,
                                      "y": -0.15,
                                      "align": "left",
                                      "font": {
                                        "color": "rgb(44, 160, 44)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": "<b>Low Sharpe<br>Ratio</b>",
                                      "xref": "x",
                                      "yref": "y"
                                    },
                                    {
                                      "x": 0.89,
                                      "y": -0.15,
                                      "align": "right",
                                      "font": {
                                        "color": "rgb(214, 39, 40)",
                                        "family": "Raleway",
                                        "size": 10
                                      },
                                      "showarrow": False,
                                      "text": "<b>High Sharpe<br>Ratio</b>",
                                      "xref": "x",
                                      "yref": "y"
                                    }
                                  ],
                                  autosize = False,
                                  height = 200,
                                  width = 340,
                                  hovermode = "closest",
                                  margin = {
                                    "r": 10,
                                    "t": 20,
                                    "b": 80,
                                    "l": 10
                                  },
                                  shapes = [
                                    {
                                      "fillcolor": "rgb(255, 255, 255)",
                                      "line": {
                                        "color": "rgb(153, 0, 0)",
                                        "width": 4
                                      },
                                      "opacity": 1,
                                      "type": "circle",
                                      "x0": Risk_Potential-0.0715,#0.621
                                      "x1": Risk_Potential+0.0715, #0.764
                                      "xref": "x",
                                      "y0": 0.135238095238,
                                      "y1": 0.98619047619,
                                      "yref": "y"
                                    }
                                  ],
                                  showlegend = True,
                                  xaxis = {
                                    "autorange": False,
                                    "fixedrange": True,
                                    "range": [-0.05, 1.05],
                                    "showgrid": False,
                                    "showticklabels": False,
                                    "title": "<br>",
                                    "type": "linear",
                                    "zeroline": False
                                  },
                                  yaxis = {
                                    "autorange": False,
                                    "fixedrange": True,
                                    "range": [-0.3, 1.6],
                                    "showgrid": False,
                                    "showticklabels": False,
                                    "title": "<br>",
                                    "type": "linear",
                                    "zeroline": False
                                }
                            )
                        }                
    
    #----------------------------------------------------------------------------------------------------
    #PricePerformance: Table Current Statistics
    Tab_Current_Statistics = html.Table(make_dash_table(Current_Statistics))
    
    #PricePerformance: Table Historic Prices 
    Tab_Historic_Prices = html.Table(make_dash_table(Historic_Prices))
    
    Fig_Price_Performance = {'data': [go.Scatter(
                                              x=Price_Development.Date, 
                                              y=Price_Development['Prices'],
                                              mode = "lines",
                                              name = str(input)
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 200,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }
                         
    
    Fig_Returns = {'data': [go.Scatter(
                                              x=Returns.Date, 
                                              y=Returns['Returns'],
                                              mode = "lines",
                                              name = str(input)
                                              ),
                            go.Scatter(
                                              x=Returns_SMI.Date, 
                                              y=Returns_SMI['Returns'],
                                              mode = "lines",
                                              name = "SSMI",
                                              line = {"color": "rgba(0, 152, 0, 0.4)"},
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 200,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }
                         
    

    #PricePerformance: Key Ratios
    Tab_Key_Ratios = html.Table(make_dash_table(Key_Ratios))
    
    #----------------------------------------------------------------------------------------------------
    #Risk Measures: Table Risk Measures 1
    Tab_Risk_Measures_1 = html.Table(make_dash_table(Risk_Measures1))
    
    #Risk Measures: Table Risk Measures 2
    Tab_Risk_Measures_2 = html.Table(make_dash_table(Risk_Measures2))
    
    #Risk Measures: Value at Risk
    Fig_Value_at_Risk = {'data': [go.Scatter(
                                              x=VaR.Date, 
                                              y=VaR['Price'],
                                              mode = "lines",
                                              name = str(input)
                                              ),
                            go.Scatter(
                                              x=VaR_SMI.Date, 
                                              y=VaR_SMI['Price'],
                                              mode = "lines",
                                              name = "SSMI",
                                              line = {"color": "rgba(0, 152, 0, 0.4)"},
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 145,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }    
    
    
    #Risk Measures: Expected Shortfall
    Fig_Expected_Shortfall = {'data': [go.Scatter(
                                              x=ES.Date, 
                                              y=ES['Price'],
                                              mode = "lines",
                                              name = str(input)
                                              ),
                            go.Scatter(
                                              x=ES_SMI.Date, 
                                              y=ES_SMI['Price'],
                                              mode = "lines",
                                              name = "SSMI",
                                              line = {"color": "rgba(0, 152, 0, 0.4)"},
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 145,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }    
    
    #Risk Measures: Drawdown
    Fig_Max_Drawdown = {'data': [go.Scatter(
                                              x=Drawdown.Date, 
                                              y=Drawdown['DD'],
                                              mode = "lines",
                                              name = "Drawdown " + str(input)
                                              ),
                            go.Scatter(
                                              x=Drawdown.Date, 
                                              y=Drawdown['Max_DD'],
                                              mode = "lines",
                                              name = "Max Drawdown " + str(input),
                                              ),
                            go.Scatter(
                                              x=Drawdown_SMI.Date, 
                                              y=Drawdown_SMI['DD'],
                                              mode = "lines",
                                              name = "Drawdown SSMI" 
                                              ),
                            go.Scatter(
                                              x=Drawdown_SMI.Date, 
                                              y=Drawdown_SMI['Max_DD'],
                                              mode = "lines",
                                              name = "Max Drawdown SSMI",
                                              line = {"color": "rgba(0, 152, 0, 0.4)"},
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 180,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }    
    
    #----------------------------------------------------------------------------------------------------
    #Technical Analysis: Table Technical Analysis
    Tab_Technical_Analysis = html.Table(make_dash_table(TechnicalAnalysis)) 
    
    #Technical Analysis: Figure Bollinger Bands
    Fig_BollingerBands = {'data': [go.Scatter(
                                              x=BollingerBands.Date, 
                                              y=BollingerBands['mavg'],
                                              mode = "lines",
                                              name = "mavg " + str(input)
                                              ),
                                   go.Scatter(
                                              x=BollingerBands.Date, 
                                              y=BollingerBands['hband'],
                                              mode = "lines",
                                              name = "hband " + str(input)
                                              ),
                                   go.Scatter(
                                              x=BollingerBands.Date, 
                                              y=BollingerBands['lband'],
                                              mode = "lines",
                                              name = "lband " + str(input)
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 145,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }    
 
    #Technical Analysis: RSI
    Fig_RSI = {'data': [go.Scatter(
                                              x=RSI.Date, 
                                              y=RSI['RSI'],
                                              mode = "lines",
                                              name = "RSI " + str(input)
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 180,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }      
    
    #Technical Analysis: Figure Aroon Indicator  Fig_AroonIndicator
    Fig_AroonIndicator = {'data': [go.Scatter(
                                              x=AroonIndicator.Date, 
                                              y=AroonIndicator['aroon_up'],
                                              mode = "lines",
                                              name = "Aroon Up " + str(input)
                                              ),
                                    go.Scatter(
                                              x=AroonIndicator.Date, 
                                              y=AroonIndicator['aroon_down'],
                                              mode = "lines",
                                              name = "Aroon Down " + str(input),
                                              )], 
                                                     
                         'layout': go.Layout(
                                            autosize = False,
                                            width = 700,
                                            height = 180,
                                            font = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                             margin = {
                                                "r": 40,
                                                "t": 40,
                                                "b": 30,
                                                "l": 40
                                              },
                                              showlegend = True,
                                              titlefont = {
                                                "family": "Raleway",
                                                "size": 10
                                              },
                                              xaxis = {
                                                "autorange": True,
                                                "range": ["2007-12-31", "2018-03-06"],
                                                "rangeselector": {"buttons": [
                                                    {
                                                      "count": 1,
                                                      "label": "1Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 3,
                                                      "label": "3Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "count": 5,
                                                      "label": "5Y",
                                                      "step": "year"
                                                    },
                                                    {
                                                      "count": 10,
                                                      "label": "10Y",
                                                      "step": "year",
                                                      "stepmode": "backward"
                                                    },
                                                    {
                                                      "label": "All",
                                                      "step": "all"
                                                    }
                                                  ]},
                                                "showline": True,
                                                "type": "date",
                                                "zeroline": False
                                              },
                                              yaxis = {
                                                "autorange": True,
                                                "range": [18.6880162434, 278.431996757],
                                                "showline": True,
                                                "type": "linear",
                                                "zeroline": False
                                              }
                                        )
                                 }      
    
    #Here all the Figures and Tables are returned such that they can be shown in the webpage
    return Loading, StockName, Description, Fig_Cumulative_Annual_Performance,Tab_Price_Performance, Fig_Hypothetical_Portfolio, \
           Fig_Average_Annual_Performance, Fig_Risk_Potential, Tab_Current_Statistics, Tab_Historic_Prices, Fig_Price_Performance, \
           Fig_Returns, Tab_Key_Ratios, Tab_Risk_Measures_1, Tab_Risk_Measures_2, Fig_Value_at_Risk, Fig_Expected_Shortfall, \
           Fig_Max_Drawdown, Tab_Technical_Analysis, Fig_BollingerBands, Fig_RSI, Fig_AroonIndicator

  

# # # # # # # # #
#external_css and external_js work are loaded
# # # # # # # # #
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})
    
external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://codepen.io/bcd/pen/YaXojL.js", #Button Click
               "https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.3.3/jspdf.min.js"] 

for js in external_js:
    app.scripts.append_script({"external_url": js})


if __name__ == '__main__':
    app.run_server(debug=False)
