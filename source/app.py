import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Inicializa o app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.layout = layout

# Registra os callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)