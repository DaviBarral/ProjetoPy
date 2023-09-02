from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO
max_value = 10
df = pd.read_csv('.vscode/Largest_Companies.csv') #diretorio do csv

# a coluna da conversão 
df['Revenue growth'] = pd.to_numeric(df['Revenue growth'], errors='coerce')

fig = px.scatter(data_frame=df, x="Revenue (USD millions)", y="Name",
                 color="Rank", log_x=True, size_max=10,
                 range_y=[0, 10], animation_frame='Revenue growth')

# primeiras linhas de crescimento
for _, row in df.iterrows():
    if row['Revenue growth'] > 0:
        fig.add_shape(
            type="line",
            x0=row["Revenue (USD millions)"],
            x1=row["Revenue (USD millions)"] + 2e9,  # Ajuste o valor para o comprimento da linha
            y0=row["Name"],
            y1=row["Name"],
            line=dict(color="green", width=1)
        )
    elif row['Revenue growth'] < 0:
        fig.add_shape(
            type="line",
            x0=row["Revenue (USD millions)"],
            x1=row["Revenue (USD millions)"] - 2e9,  # aqui onde ajusta o valor das linhas se não estou enganado
            y0=row["Name"],
            y1=row["Name"],
            line=dict(color="red", width=1)
        )

# Configuração do layout
app.layout = dbc.Container([
    dbc.Row([
        html.H1("Crescimento da receita das Empresas", style={'textAlign': 'center'})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='our-plot', figure=fig)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Filtrar Por Classificação (Rank):"),
            dcc.RangeSlider(
                id='rank-slider',
                min=df['Rank'].min(),
                max=max_value,
                step=1,
                marks={i: str(i) for i in range(df['Rank'].min(), max_value + 1)},
                value=[df['Rank'].min(), max_value]
            )
        ], width=6, className="mx-auto")
    ])
])

@app.callback(
    Output('our-plot', 'figure'),
    Input('rank-slider', 'value')
)
def update_graph(selected_rank_range):
    filtered_df = df[(df['Rank'] >= selected_rank_range[0]) & (df['Rank'] <= selected_rank_range[1])]
    updated_fig = px.scatter(data_frame=filtered_df, x="Revenue (USD millions)", y="Name",
                             color="Rank", log_x=True,
                             size_max=10, range_y=[0, 10], animation_frame='Revenue growth')
 
    # linhas de crescimento aqui
    for _, row in filtered_df.iterrows():
        if row['Revenue growth'] > 0:
            updated_fig.add_shape(
                type="line",
                x0=row["Revenue (USD millions)"],
                x1=row["Revenue (USD millions)"] + 2e9,
                y0=row["Name"],
                y1=row["Name"],
                line=dict(color="green", width=1)
            )
        elif row['Revenue growth'] < 0:
            updated_fig.add_shape(
                type="line",
                x0=row["Revenue (USD millions)"],
                x1=row["Revenue (USD millions)"] - 2e9,
                y0=row["Name"],
                y1=row["Name"],
                line=dict(color="red", width=1)
            )
 
 
    return updated_fig

if __name__ == '__main__':
    app.run_server(debug=True, port='8051')