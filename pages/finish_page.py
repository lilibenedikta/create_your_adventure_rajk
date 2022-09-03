from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import dash

import plotly.graph_objects as go


dash.register_page(__name__, path="/finish")

layout = html.Div(
    children=[
        html.Link(href="/assets/style.css", rel="stylesheet"),
        html.H1(
            "Gratulálunk, véget ért számodra a kaland!",
            className="centre_text_main_finish",
        ),
        html.H1("A statisztikáid:", className="centre_text_secondary_finish"),
        html.H1("Önző Geci - People Pleaser", className="centre_graph_title_left_1st"),
        html.H1("Falu Bikája - Nyuszimuszi", className="centre_graph_title_1st"),
        html.H1(
            "Kaland alatt elszívott cigeratták",
            className="centre_graph_title_right_1st",
        ),
        html.H1(
            "Szutykos Alkesz - Judgy Health Guru",
            className="centre_graph_title_left_2nd",
        ),
        html.H1(
            "Közveszélyes Naplopó - Pozihalmozó Szakmahajcsár",
            className="centre_graph_title_2nd",
        ),
        dcc.Graph(id="graph_onzo_pleaser", className="centre_graph_left_1st"),
        dcc.Graph(id="graph_bika_nyuszi", className="centre_graph_1st"),
        dcc.Graph(id="graph_elszivott_cigik", className="centre_graph_right_1st"),
        dcc.Graph(id="graph_szutykos_guru", className="centre_graph_left_2nd"),
        dcc.Graph(id="graph_naplopo_hajcsar", className="centre_graph_2nd"),
        dbc.Button(
            "Újrakezdem!", id="ujra", href="/", className="centre_button_right_2nd"
        ),
        dcc.Store(id="store_current_user_data_ch_3"),
    ]
)


@callback(
    [
        Output("graph_onzo_pleaser", "figure"),
        Output("graph_bika_nyuszi", "figure"),
        Output("graph_elszivott_cigik", "figure"),
        Output("graph_szutykos_guru", "figure"),
        Output("graph_naplopo_hajcsar", "figure"),
    ],
    Input("ujra", "n_clicks"),
    State("store_current_user_data_ch_3", "data"),
)
def onzo_abra(n_clicks, finished_user_data):

    # onzo_pleaser
    fig = go.Figure(
        go.Bar(
            x=[finished_user_data["onzo_pleaser"]],
            orientation="h",
            marker_color="#39FF14",
        )
    )
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(
        range=[-60, 60],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 40, "b": 40, "t": 10, "r": 0},
        hovermode="closest",
    )

    # bika_nyuszi
    fig_2 = go.Figure(
        go.Bar(
            x=[finished_user_data["bika_nyuszi"]],
            orientation="h",
            marker_color="#39FF14",
        )
    )
    fig_2.update_yaxes(visible=False, showticklabels=False)
    fig_2.update_xaxes(
        range=[-60, 60],
    )
    fig_2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 40, "b": 40, "t": 10, "r": 0},
        hovermode="closest",
    )

    # elszivott_cigik
    fig_3 = go.Figure(
        go.Bar(
            x=[finished_user_data["elszivott_cigik"]],
            orientation="h",
            marker_color="#39FF14",
        )
    )
    fig_3.update_yaxes(visible=False, showticklabels=False)
    fig_3.update_xaxes(
        range=[0, 5],
    )
    fig_3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 40, "b": 40, "t": 10, "r": 0},
        hovermode="closest",
    )

    # szutykos_guru
    fig_4 = go.Figure(
        go.Bar(
            x=[finished_user_data["szutykos_guru"]],
            orientation="h",
            marker_color="#39FF14",
        )
    )
    fig_4.update_yaxes(visible=False, showticklabels=False)
    fig_4.update_xaxes(
        range=[-60, 60],
    )
    fig_4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 40, "b": 40, "t": 10, "r": 0},
        hovermode="closest",
    )

    # naplopo_hajcsar
    fig_5 = go.Figure(
        go.Bar(
            x=[finished_user_data["naplopo_hajcsar"]],
            orientation="h",
            marker_color="#39FF14",
        )
    )
    fig_5.update_yaxes(visible=False, showticklabels=False)
    fig_5.update_xaxes(
        range=[-60, 60],
    )
    fig_5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 40, "b": 40, "t": 10, "r": 0},
        hovermode="closest",
    )

    return fig, fig_2, fig_3, fig_4, fig_5
