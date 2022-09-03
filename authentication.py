import boto3
import pandas as pd
import os

client = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name="us-east-1",
)


bucket = "rajkzorksaves"
szovegek = "szovegek"
edges = "RAJK_ZORK_edges.csv"
nodes = "RAJK_ZORK_nodes.csv"

RAJK_ZORK_edges_from_AWS_server = client.get_object(Bucket=szovegek, Key=edges)
RAJK_ZORK_nodes_from_AWS_server = client.get_object(Bucket=szovegek, Key=nodes)
edge_data = pd.read_csv(RAJK_ZORK_edges_from_AWS_server["Body"]).set_index("FROM")
node_data = pd.read_csv(RAJK_ZORK_nodes_from_AWS_server["Body"]).set_index("NODE_ID")
