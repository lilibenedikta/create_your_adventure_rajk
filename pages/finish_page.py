import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/finish")

layout = html.Div(
    children=[
        html.Link(href="/assets/style.css", rel="stylesheet"),
        html.H1(
            "Gratulálunk, sikeresen végigvitted a kalandot!",
            className="centre_text_main_finish",
        ),
        dbc.Button("Újrakezdem!", id="ujra", href="/", className="centre_button"),
    ]
)
