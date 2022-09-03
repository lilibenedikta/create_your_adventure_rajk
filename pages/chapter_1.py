from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from collections import defaultdict
from session_state import SessionState
from authentication import edge_data, node_data
import dash_bootstrap_components as dbc
import dash

dash.register_page(__name__, path="/gameon")

STATES = defaultdict(SessionState)

layout = html.Div(
    children=[
        dcc.Markdown(id="situation", className="good_text"),
        dcc.RadioItems(id="option_selector", className="good_radio", inline=False),
        dbc.Button("Tovább", id="submit_gomb", n_clicks=0),
        dbc.Button("Befejezés", id="finish_gomb", href="/finish"),
        dbc.Button("2. fejezet", id="chapter_2_gomb", href="/chapter_two_divider"),
        dbc.Button("3. fejezet", id="chapter_3_gomb", href="/chapter_three_divider"),
        dcc.Store(id="store_current_user_data_ch_1"),
        dcc.Store(id="store_current_user_id"),
    ]
)


@callback(
    [
        Output("situation", "children"),
        Output("option_selector", "options"),
        Output("submit_gomb", "style"),
        Output("chapter_2_gomb", "style"),
        Output("chapter_3_gomb", "style"),
        Output("finish_gomb", "style"),
        Output("store_current_user_data_ch_1", "data"),
    ],
    Input("submit_gomb", "n_clicks"),
    [State("option_selector", "value"), State("store_current_user_id", "data")],
)
def continue_game(n_clicks, selector_value, current_user_id):
    if n_clicks is None:
        raise PreventUpdate

    sesh = STATES[current_user_id]
    current_user_data_ch_1 = {}

    if n_clicks:
        if selector_value is None:
            raise PreventUpdate
        else:
            sesh.move_on_scale_onzo_pleaser(selector_value)
            sesh.move_on_scale_bika_nyuszi(selector_value)
            sesh.move_on_scale_szutykos_guru(selector_value)
            sesh.move_on_scale_naplopo_hajcsar(selector_value)
            sesh.move_on_scale_elszivott_cigik(selector_value)
            sesh.decide(selector_value)

    next_text = node_data.loc[sesh.current_state, "TEXT_N"]

    if sesh.current_state in {
        "T_I_11111_11",
        "T_I_11112_212",
        "T_I_11112_214",
        "T_I_11112_2113",
        "T_I_11112_2111",
        "T_I_11112_22",
        "T_I_11111_422",
        "T_I_11112_2112",
        "T_I_11111_423",
        "T_I_11111_421",
    }:
        next_radio = []
        submit_button_style = {"visibility": "hidden"}
        chapter_2_gomb = {"visibility": "visible"}
        chapter_3_gomb = {"visibility": "hidden"}
        finish_button_style = {"visibility": "hidden"}

        current_user_data_keys_ch_1 = [
            "user_id",
            "current_state",
            "onzo_pleaser",
            "bika_nyuszi",
            "szutykos_guru",
            "naplopo_hajcsar",
            "elszivott_cigik",
        ]
        current_user_data_values_ch_1 = [
            current_user_id,
            sesh.current_state,
            sesh.onzo_pleaser,
            sesh.bika_nyuszi,
            sesh.szutykos_guru,
            sesh.naplopo_hajcsar,
            sesh.elszivott_cigik,
        ]
        current_user_data_ch_1 = {
            k: v
            for k, v in zip(current_user_data_keys_ch_1, current_user_data_values_ch_1)
        }

    else:
        next_radio = edge_data.loc[sesh.current_state].apply(
            lambda r: dict(label=r["TEXT_E"], value=r["OPTION_NUM"]), axis=1
        )
        submit_button_style = {"visibility": "visible"}
        chapter_2_gomb = {"visibility": "hidden"}
        chapter_3_gomb = {"visibility": "hidden"}
        finish_button_style = {"visibility": "hidden"}

    return (
        next_text,
        next_radio,
        submit_button_style,
        chapter_2_gomb,
        chapter_3_gomb,
        finish_button_style,
        current_user_data_ch_1,
    )
