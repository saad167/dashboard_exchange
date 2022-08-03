import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go




p=pd.read_csv("./ExportData.csv",sep=";")
p=p.drop('Unnamed: 7',axis=1)
p=p.dropna()

def entier(x):
    #if type(x)==float :
     #   return int(x)
    #else:
        l=""
        for i in x :
            if i == ",":
                l=l+'.'
            else :
                l=l+i
        return float(l) #int(l)

p["Valeur DHS 2019"]=[entier(x) for x in p["Valeur DHS 2019"] ]
p["Valeur DHS 2020"]=[entier(x) for x in p["Valeur DHS 2020"] ]
p["Valeur DHS 2021"]=[entier(x) for x in p["Valeur DHS 2021"] ]
p=p.rename(columns={"Valeur DHS 2019": "2019", "Valeur DHS 2020": "2020","Valeur DHS 2021":"2021"})


app = dash.Dash(__name__)


#################################################### APP COLOURS #####################################################

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


##################################################################################################################


app.layout = html.Div([
        html.Div([
            html.P("Continent:"),
            dcc.Dropdown(
                id='continent',
                options=[{'label': i, 'value': i} for i in set(p["Continent"])  ],
                value='EUROPE')
 
                ], style={'width': '48%', 'display': 'inline-block'}),           
        html.Div([
            html.P("Année:"),
            dcc.Dropdown(
                id='year',
                options=[{'label': i, 'value': i} for i in ['2019','2020','2021']  ],
                value='2019')
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        dcc.Graph(id='indicator-graphic'),

         html.Div([
             html.P("Flux:"),
             dcc.Dropdown(
                id='flux', 
                value='Exportations FAB', 
                options=[{'value': x, 'label': x} for x in ["Exportations FAB","Importations CAF"]])
               ], style={'width': '48%', 'display': 'inline-block'}),
            
        html.Div([
            html.P("Année:"),
            dcc.Dropdown(
                id='year1',
                options=[{'label': i, 'value': i} for i in ['2019','2020','2021']  ],
                value='2019')
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        
          dcc.Graph(id='pie-chart'),
            
    
    
        html.Div([
             html.P("Pays:"),
             dcc.Dropdown(
                id='pays', 
                value='NIGERIA', 
                options=[{'value': x, 'label': x} for x in set(p['Libellé du pays']) ] )]
               ),
            
      dcc.Graph(id='indicator-graphic1'),
    
      html.Div([
             html.P("Pays:"),
             dcc.Dropdown(
                id='pays1', 
                value='NIGERIA', 
                options=[{'value': x, 'label': x} for x in set(p['Libellé du pays']) ] )],
               style={'width': '48%', 'display': 'inline-block'}
               ),
    
        html.Div([
            html.P("Année:"),
            dcc.Dropdown(
                id='year2',
                options=[{'label': i, 'value': i} for i in ['2019','2020','2021']  ],
                value='2019')
            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    
         dcc.Graph(id='pie-chart1')   
    
    
])

#################################################################################################################
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('continent', 'value'),
    Input('year', 'value')])

def update_graph(continent_name,year_value):
    pmodifie =p[p["Continent"]==str(continent_name)]
    pmodifie=pmodifie.groupby(["Libellé du pays","Libellé du flux"])[str(year_value)].aggregate("sum").unstack()
    pmodifie=pmodifie.dropna()
    x=pmodifie.index
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=pmodifie["Exportations FAB"],
        name='Exportations FAB',
        marker_color='rgb(255, 255, 7)'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=pmodifie["Importations CAF"],
        name='Importations CAF',
        marker_color='rgb(255, 132, 7)'
    ))
    fig.update_layout(
        title='Expo/Impo '+continent_name+'  en '+str(year_value),
        xaxis_tickfont_size=10,
        yaxis_tickfont_size=10,
        xaxis_title='Pays',
        yaxis=dict(
            title='Valeur en DHS',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
    )
    return fig

@app.callback(
     Output('pie-chart', 'figure'),
    [Input('flux','value'),
    Input('year1', 'value')]
)
def generate_chart(flux_value,year_value):
    x=0
    if str(flux_value)=="Importations CAF":
        x=1
    pcontinent=p.groupby(["Continent","Libellé du flux"])[str(year_value)].aggregate("sum").unstack()
    fig = go.Figure(data=[go.Pie(labels=pcontinent.index, values=pcontinent.values[:,x], pull=[0, 0, 0,0, 0,0.2])])
    fig.update_layout(
        title=str(flux_value)+"  "+ str(year_value),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    return fig

@app.callback(
    Output('indicator-graphic1', 'figure'),
    [Input('pays', 'value')])
def update_graph_1(pays_value):
    ppays=p[p["Libellé du pays"]==pays_value]
    ppays=ppays.groupby(["Libellé du flux"])[["2019","2020","2021"]].aggregate("sum")
    ppays=ppays.dropna()
    
    x = ppays.columns

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=ppays.values[0],
        name='Exportation',
        marker_color='rgb(255, 255, 7)'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=ppays.values[1],
        name='Importation',
        marker_color='rgb(255, 132, 7)'
    ))

    fig.update_layout(
        title='Expo/Impo '+pays_value,
        xaxis=dict(
            title='Années',
            tickfont_size=14,
        ),
        yaxis=dict(
            title='Valeur en DHS',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    return fig

@app.callback(
     Output('pie-chart1', 'figure'),
    [Input('pays1','value'),
    Input('year2', 'value')]
)
def generate_chart_1(pays_value,year_value):
    pmod =p[p["Libellé du pays"]==str(pays_value)]
    pmod=pmod.groupby('Libellé du flux')[["2019","2020","2021"]].aggregate("sum")
    
    fig = go.Figure(data=[go.Pie(labels=pmod.index, values=pmod[str(year_value)], pull=[0,0.2])])
    fig.update_layout(
        title="les flux de "+ str(pays_value) + " en "+str(year_value),
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    return fig



    
    

####################################################################################################################
if __name__ == '__main__':
    app.run_server(debug=True)
