from authentication import client, szovegek, edges
import pandas as pd

RAJK_ZORK_edges_from_AWS_server = client.get_object(Bucket=szovegek, Key=edges)

edge_data_session_state = pd.read_csv(
    RAJK_ZORK_edges_from_AWS_server["Body"]
).set_index(["FROM", "OPTION_NUM"])


class SessionState:
    def __init__(self) -> None:
        self.initial_state = "T_I_1"
        self.current_state = self.initial_state
        self.onzo_pleaser = 0
        self.bika_nyuszi = 0
        self.szutykos_guru = 0
        self.naplopo_hajcsar = 0
        self.elszivott_cigik = 0

    def decide(self, option_num):
        self.current_state = edge_data_session_state.loc[
            (self.current_state, option_num), "TO"
        ]

    def move_on_scale_onzo_pleaser(self, option_num):
        self.onzo_pleaser += edge_data_session_state.loc[
            (self.current_state, option_num), "ONZO_PLEASER"
        ]

    def move_on_scale_bika_nyuszi(self, option_num):
        self.bika_nyuszi += edge_data_session_state.loc[
            (self.current_state, option_num), "BIKA_NYUSZI"
        ]

    def move_on_scale_szutykos_guru(self, option_num):
        self.szutykos_guru += edge_data_session_state.loc[
            (self.current_state, option_num), "SZUTYKOS_GURU"
        ]

    def move_on_scale_naplopo_hajcsar(self, option_num):
        self.naplopo_hajcsar += edge_data_session_state.loc[
            (self.current_state, option_num), "NAPLOPO_HAJCSAR"
        ]

    def move_on_scale_elszivott_cigik(self, option_num):
        self.elszivott_cigik += edge_data_session_state.loc[
            (self.current_state, option_num), "ELSZIVOTT_CIGIK"
        ]
