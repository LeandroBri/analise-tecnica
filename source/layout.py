from dash import dcc, html
import dash_bootstrap_components as dbc
from data import crypto_options, timeframes, update_intervals

layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Análise Técnica - Multi Gráficos", className="text-center text-primary"), width=12)], className="mb-4"),

    dbc.Row([
        *[
            dbc.Col([
                html.Label(f"Par {i+1}:", className="fw-bold text-left d-block", style={'color': '#FFF', 'font-size': '18px'}),
                dcc.Dropdown(id=f"dropdown-pair-{i}", options=crypto_options, value=crypto_options[0]['value'], clearable=False,style={'color' : '#222', 'background-color' : '#090909', 'border' : 'none'}),
                html.Label("Timeframe:", className="fw-bold text-left d-block mt-2", style={'color': '#FFF', 'font-size': '18px'}),
                dcc.Dropdown(id=f"dropdown-timeframe-{i}", options=timeframes, value=timeframes[i]['value'], clearable=False,style={'color' : '#222', 'background-color' : '#090909', 'border' : 'none'}),
                
                # Opções de indicadores
                html.Label("Indicadores:", className="fw-bold text-left d-block mt-2", style={'color': '#333', 'font-size': '18px', 'font-size': '18px'}),
                dcc.Checklist(
                    id=f"indicators-{i}",
                    options=[
                        {"label": "RSI", "value": "RSI"},
                        {"label": "EMA", "value": "EMA"},
                        {"label": "SMA", "value": "SMA"},
                        {"label": "Bandas de Bollinger", "value": "BB"},
                    ],
                    value=[],labelStyle={ 'padding' : '0.5em', 'background-color' : '#030303'},  # Nenhum indicador ativado por padrão
                    inline=True,
                    style={'color': '#555', 'padding' : '0', 'margin' : '0'}
                ),
            ], width=3) for i in range(4)
        ]
    ], className="mb-3"),

    dbc.Row([
        dbc.Col([
            html.Label("Tempo de atualização:", className="fw-bold text-left d-block", style={'color': '#FFF', 'font-size': '18px'}),
            dcc.Dropdown(id="update-interval", options=update_intervals, value=10000, clearable=False, 
                         style={'margin' : '0' , 'width': '150px', 'float': 'left', 'background-color' : '#090909' ,'color': '#333', 'font-size': '18px', 'border' : 'none'}),            
            dcc.Interval(id="interval-component", interval=10000, n_intervals=0)
        ], width=4)
    ], className="mb-3"),

    dbc.Row([
        *[
            dbc.Col([
                html.Div(id=f"macd-alert-{i}", className="text-center fw-bold m-3"),
                dcc.Graph(id=f"crypto-chart-{i}"),
            ], width=6) for i in range(4)
        ]
    ], style={ 'margin-bottom' : '20px'})
], fluid=True)

