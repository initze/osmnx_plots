import osmnx as ox
from osmnx._errors import InsufficientResponseError


def download_and_project_graph(place, network_type=None, custom_filter=None):
    try:
        if network_type:
            G = ox.graph_from_place(place, network_type=network_type)
        elif custom_filter:
            G = ox.graph_from_place(place, custom_filter=custom_filter)
        else:
            raise ValueError("Either network_type or custom_filter must be provided.")
        G_proj = ox.project_graph(G)
        return G_proj
    except InsufficientResponseError:
        print(f"No data found for filter/network_type: {network_type or custom_filter}")
        return None
