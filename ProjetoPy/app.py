import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}
server = app.server