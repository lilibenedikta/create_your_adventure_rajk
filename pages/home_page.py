from dash import dcc, html, callback
from dash.dependencies import Input, Output
from botocore.exceptions import ClientError
from authentication import client, bucket
import dash_bootstrap_components as dbc
import dash
import pickle


dash.register_page(__name__, path="/")

layout = html.Div(
    children=[
        html.Link(href="/assets/style.css", rel="stylesheet"),
        html.H1("Sose lesz vége!", className="centre_text_main"),
        html.H3(
            "Üsd be a neved egy új játékhoz. \
            Ha már rendelkezel mentéssel, akkor pedig folytasd ugyanonnan.",
            className="centre_text_secondary",
        ),
        dcc.Input(id="text_input_small", type="text", placeholder="Enter user ID"),
        dbc.Button("Mehet!", id="start_gomb", className="centre_button"),
        dcc.Store(id="loaded_id"),
        dcc.Store(id="store_current_user_data"),
        dcc.Store(id="store_current_user_id"),
    ]
)


@callback(
    [
        Output("start_gomb", "href"),
        Output("loaded_id", "data"),
        Output("store_current_user_data", "data"),
        Output("store_current_user_id", "data"),
    ],
    [Input("text_input_small", "value"), Input("start_gomb", "n_clicks")],
)
def start_game(input_text, n_clicks):
    if input_text is None:
        user_id_to_be = "Newgame"
    elif len(input_text) == 0:
        user_id_to_be = "Newgame"
    else:
        user_id_to_be = input_text

    try:
        client.head_object(Bucket=bucket, Key=user_id_to_be)
        current_user_data = pickle.loads(
            client.get_object(Bucket=bucket, Key=user_id_to_be)["Body"].read()
        )
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            current_user_data_keys = [
                "user_id",
                "current_state",
                "onzo_pleaser",
                "bika_nyuszi",
                "szutykos_guru",
                "naplopo_hajcsar",
                "elszivott_cigik",
            ]
            current_user_data_values = [user_id_to_be, "T_I_1", 0, 0, 0, 0, 0]
            current_user_data = {
                k: v for k, v in zip(current_user_data_keys, current_user_data_values)
            }

    if current_user_data["current_state"] == "T_I_1":
        href = "/gameon"
        loaded_id = 1
    elif current_user_data["current_state"] in {
        "T_II_1_jo",
        "T_II_1_kozepes",
        "T_II_1_rossz",
    }:
        href = "/chapter_two"
        loaded_id = 2
    elif current_user_data["current_state"] in {"T_III_1", "T_III_2"}:
        href = "/chapter_three"
        loaded_id = 3

    if n_clicks:
        serialized_current_user_data = pickle.dumps(current_user_data)
        client.put_object(
            Bucket=bucket,
            Key=current_user_data["user_id"],
            Body=serialized_current_user_data,
        )

    return href, loaded_id, current_user_data, current_user_data["user_id"]
