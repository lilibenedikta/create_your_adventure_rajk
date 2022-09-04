from authentication_and_parameters import (
    client,
    story_bucket,
    edges,
    initial_state,
)
import pandas as pd

RAJK_ZORK_edges_from_AWS_server = client.get_object(
    Bucket=story_bucket, Key=edges
)

edge_data_session_state = pd.read_csv(
    RAJK_ZORK_edges_from_AWS_server["Body"]
).set_index(["FROM", "OPTION_NUM"])


class SessionState:
    def __init__(self) -> None:
        self.initial_state = initial_state
        self.current_state = self.initial_state

    def decide(self, option_num):
        self.current_state = edge_data_session_state.loc[
            (self.current_state, option_num), "TO"
        ]
