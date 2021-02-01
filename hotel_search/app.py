import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

hotels_df = pd.read_csv("./hotels.csv")
tour_att_df = pd.read_csv("./tourist_attractions.csv")

tour_att_names = tour_att_df["PAGETITLE"]

app.layout = html.Div([
    html.Div(
        className='header',
        children=[
            html.H1("Hotel Hunting", className='recommendation')
        ],
    ),
    html.Div(children=[
        html.P("Select the tourist attractions which you are interested to visit", className='input'),
        html.Div(
            dcc.Dropdown(
                id='tour-att',
                options=[{'label': t, 'value': t} for t in tour_att_names],
                value=["Gardens by the Bay"],
                multi=True
            ),
            style={'width': '50%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='display-map')
])

@app.callback(
    Output('display-map', 'figure'),
    [Input('tour-att', 'value')]
)
def update_figure(attractions):

    filtered_tour_att = tour_att_df[tour_att_df["PAGETITLE"].isin(attractions)]

    fig = go.Figure(go.Scattermapbox(
        mode = "markers",
        lon = hotels_df["Longitude"],
        lat = hotels_df["Latitude"],
        text = hotels_df["Name"],
        name = "Hotels",
        marker = {'size': 10, 'color': 'cyan'}
    ))

    fig.add_trace(go.Scattermapbox(
        fill = "toself",
        lon = filtered_tour_att["LONGTITUDE"],
        lat = filtered_tour_att["LATITUDE"],
        text = filtered_tour_att["PAGETITLE"],
        name = "Tourist attractions",
        marker = {'size': 11, 'color': 'darkgoldenrod'}
    ))

    fig.update_layout(
        mapbox = {
            'style': "stamen-terrain",
            'center': {'lon': 103.8, 'lat': 1.35},
            'zoom': 10
        },
        showlegend = True
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)