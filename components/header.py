#Python Script---------------------------------------------------------------------------------------------------------------------------
#Title: Header
# coding: utf-8
#----------------------------------------------------------------------------------------------------------------------------------------
import dash_html_components as html
import dash_core_components as dcc

def Header(app):
    return html.Div([
        get_logo(app),
        get_header(),
        html.Br([]),
        get_menu()
    ])

def get_logo(app):
    logo = html.Div([

        html.Div([
            html.Img(src=app.get_asset_url('Logo.png'), height='40', width='160')
        ], className="ten columns padded"),

        html.Div([
            dcc.Link('Full View   ', href='/dash-report/full-view')
        ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H5("Stock")
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

         dcc.Link('Overview   ', href='/dash-report/overview', className="tab first"),
         dcc.Link('Price Performance', href='/dash-report/pricePerformance', className="tab first"),
         dcc.Link('Risk Measures', href='/dash-report/riskMeasures', className="tab first"),
         dcc.Link('Technical Analysis', href='/dash-report/technicalAnalysis', className="tab first")
        
    ], className="row ")
    return menu
