from dash import Dash
from flask import send_from_directory
import os
import dash_bootstrap_components as dbc

app = Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "style.css"],
    use_pages=True,
)

server = app.server

@app.server.route("/assets/<path:path>")
def static_file(path):
    static_folder = os.path.join(os.getcwd(), "assets")
    return send_from_directory(static_folder, path)


if __name__ == "__main__":
    app.run_server(debug=True)
