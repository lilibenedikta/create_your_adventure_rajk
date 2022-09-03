from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from collections import defaultdict
from session_state import SessionState
from authentication import (
    client,
    edge_data,
    node_data,
    saves_bucket,
    finish_nodes,
)
import dash_bootstrap_components as dbc
import dash
import pickle

dash.register_page(__name__, path="/gameon")

STATES = defaultdict(SessionState)

layout = html.Div(
    children=[
        dcc.Markdown(
            id="situation",
            className="good_text",
        ),
        dcc.RadioItems(
            id="option_selector",
            className="good_radio",
            inline=False,
        ),
        dbc.Button(
            "Tovább",
            id="submit_gomb",
            n_clicks=0,
            className="stylish_button",
        ),
        dbc.Button(
            "Mentés & Kilépés",
            id="mentes_kilepes_gomb",
            href="/",
            className="stylish_button",
        ),
        dbc.Button(
            "Befejezés",
            id="finish_gomb",
            href="/finish",
            className="stylish_button",
        ),
        dcc.Store(
            id="store_current_user_id",
        ),
        dcc.Store(
            id="last_user_id",
        ),
        dcc.Store(
            id="last_state",
        ),
        dcc.Store(
            id="store_current_state",
        ),
    ]
)


@callback(
    [
        Output("situation", "children"),
        Output("option_selector", "options"),
        Output("option_selector", "value"),
        Output("submit_gomb", "style"),
        Output("finish_gomb", "style"),
        Output("last_state", "data"),
    ],
    [
        Input("submit_gomb", "n_clicks"),
        Input("mentes_kilepes_gomb", "n_clicks"),
    ],
    [
        State("option_selector", "value"),
        State("store_current_user_id", "data"),
        State("store_current_state", "data"),
    ],
)
def continue_game(
    n_clicks,
    n_clicks_mentes,
    selector_value,
    user_id,
    laoded_current_state,
):
    sesh = STATES[user_id]
    current_user_data_ch_2_div_save = {}
    if n_clicks == 0:
        sesh.current_state = laoded_current_state
    if n_clicks:
        if selector_value is None:
            raise PreventUpdate
        else:
            sesh.decide(selector_value)

    next_text = node_data.loc[sesh.current_state, "TEXT_N"]

    if sesh.current_state in finish_nodes:
        next_radio = []
        submit_button_style = {"visibility": "hidden"}
        finish_button_style = {"visibility": "visible"}

    else:
        next_radio = edge_data.loc[sesh.current_state].apply(
            lambda r: dict(label=r["TEXT_E"], value=r["OPTION_NUM"]), axis=1
        )
        submit_button_style = {"visibility": "visible"}
        finish_button_style = {"visibility": "hidden"}

    if n_clicks_mentes:
        current_user_data_ch_2_div_save["user_id"] = user_id
        current_user_data_ch_2_div_save["current_state"] = sesh.current_state

        serialized_current_user_data_ch_2_div_save = pickle.dumps(
            current_user_data_ch_2_div_save
        )
        client.put_object(
            Bucket=saves_bucket,
            Key=user_id,
            Body=serialized_current_user_data_ch_2_div_save,
        )

    return (
        next_text,
        next_radio,
        1,
        submit_button_style,
        finish_button_style,
        sesh.current_state,
    )
