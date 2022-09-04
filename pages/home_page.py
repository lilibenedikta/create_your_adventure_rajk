from dash import dcc, html, callback
from dash.dependencies import Input, Output
from botocore.exceptions import ClientError
from authentication_and_parameters import client, saves_bucket, initial_state
import dash_bootstrap_components as dbc
import dash
import pickle


dash.register_page(__name__, path="/")

layout = html.Div(
    children=[
        html.Link(
            href="/assets/style.css",
            rel="stylesheet",
        ),
        html.H1(
            "Sose lesz vége!",
            className="centre_text_main",
        ),
        html.H3(
            "Üsd be a neved egy új játékhoz. \
            Ha már rendelkezel mentéssel, akkor pedig folytasd ugyanonnan.",
            className="centre_text_secondary",
        ),
        dcc.Input(
            id="text_input_small",
            type="text",
            placeholder="Enter user ID",
        ),
        dbc.Button(
            "Mehet!",
            id="start_gomb",
            href="/gameon",
            className="centre_button",
        ),
        dcc.Store(
            id="store_current_state",
        ),
        dcc.Store(
            id="store_current_user_id",
        ),
    ]
)


@callback(
    [
        Output("store_current_state", "data"),
        Output("store_current_user_id", "data"),
    ],
    [
        Input("text_input_small", "value"),
        Input("start_gomb", "n_clicks"),
    ],
)
def start_game(input_text, n_clicks):
    current_user_data = {}
    if input_text is None:
        user_id_to_be = "Newgame"
    elif len(input_text) == 0:
        user_id_to_be = "Newgame"
    else:
        user_id_to_be = input_text

    try:
        client.head_object(Bucket=saves_bucket, Key=user_id_to_be)
        current_user_data = pickle.loads(
            client.get_object(Bucket=saves_bucket, Key=user_id_to_be)[
                "Body"
            ].read()
        )
    except ClientError as e:
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            current_user_data["user_id"] = user_id_to_be
            current_user_data["current_state"] = initial_state

    if n_clicks:
        serialized_current_user_data = pickle.dumps(current_user_data)
        client.put_object(
            Bucket=saves_bucket,
            Key=current_user_data["user_id"],
            Body=serialized_current_user_data,
        )

    return current_user_data["current_state"], current_user_data["user_id"]
