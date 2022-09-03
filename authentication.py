import boto3
import pandas as pd
import os

region_name = "us-east-1"
saves_bucket = "create-your-adventure"
story_bucket = "szovegek"
edges = "RAJK_ZORK_edges.csv"
nodes = "RAJK_ZORK_nodes.csv"
initial_state = "T_I_1"
finish_nodes = {
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
}

client = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=region_name,
)

RAJK_ZORK_edges_from_AWS_server = client.get_object(
    Bucket=story_bucket, Key=edges
)
RAJK_ZORK_nodes_from_AWS_server = client.get_object(
    Bucket=story_bucket, Key=nodes
)
edge_data = pd.read_csv(RAJK_ZORK_edges_from_AWS_server["Body"]).set_index(
    "FROM"
)
node_data = pd.read_csv(RAJK_ZORK_nodes_from_AWS_server["Body"]).set_index(
    "NODE_ID"
)
