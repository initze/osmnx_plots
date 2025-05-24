import os
import re
from pathlib import Path

import matplotlib.pyplot as plt
import osmnx as ox
import pandas as pd
from matplotlib_scalebar.scalebar import ScaleBar
from osmnx._errors import InsufficientResponseError
from osmnx_plots.utils.tools import sanitize_filename
from osmnx_plots.utils.download import download_and_project_graph

def plot_transport_network(
    place_name: str,
    save_dir: str,
    layers=["tram", "s-bahn"],
    identifier: str = None,
    quiet: bool = False,
    overwrite: bool = False,
):
    """
    Download and plot street network plus optional tram and/or S-Bahn networks for a place,
    save the figure to save_dir with a sanitized filename.

    Parameters:
    - place_name: str, e.g. 'Hannover, Germany'
    - save_dir: str, directory path to save the figure
    - layers: list of strings, any subset of ['tram', 's-bahn'] indicating which layers to include
    """

    if not identifier:
        filename_safe = sanitize_filename(place_name)
    else:
        filename_safe = identifier

    # Create output directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    save_path = Path(os.path.join(save_dir, f"{filename_safe}.png"))

    if save_path.exists() and not overwrite:
        return None

    

    # Download street network (mandatory)
    try:
        G_drive_proj = download_and_project_graph(place_name, network_type="drive")
    except:
        return
    
    if G_drive_proj is None:
        raise RuntimeError(
            f"Street network (drive) data is required but not found for '{place_name}'."
        )

    # Prepare containers for optional layers
    G_tram_proj = None
    G_sbahn_proj = None

    # Download optional layers based on 'layers' argument
    if "tram" in layers:
        G_tram_proj = download_and_project_graph(
            place_name, custom_filter='["railway"~"tram"]'
        )
    if "s-bahn" in layers:
        G_sbahn_proj = download_and_project_graph(
            place_name, custom_filter='["railway"~"light_rail|s-bahn"]'
        )

    # Collect all available nodes for bounding box calculation
    all_nodes_list = []
    nodes_drive = ox.graph_to_gdfs(G_drive_proj, edges=False)
    all_nodes_list.append(nodes_drive)

    if G_tram_proj:
        nodes_tram = ox.graph_to_gdfs(G_tram_proj, edges=False)
        all_nodes_list.append(nodes_tram)

    if G_sbahn_proj:
        nodes_sbahn = ox.graph_to_gdfs(G_sbahn_proj, edges=False)
        all_nodes_list.append(nodes_sbahn)

    all_nodes = pd.concat(all_nodes_list)
    minx, miny, maxx, maxy = all_nodes.total_bounds

    # Plot base street network
    fig, ax = ox.plot_graph(
        G_drive_proj,
        figsize=(12, 12),
        node_size=0,
        edge_color=(0.5, 0.5, 0.5),
        edge_linewidth=1,
        bgcolor=(0.98, 0.98, 0.98),
        show=False,
        close=False,
    )

    # Overlay tram lines if requested and available
    if G_tram_proj:
        ox.plot_graph(
            G_tram_proj,
            ax=ax,
            node_size=0,
            edge_color=(0.5, 0, 0),  # dark red
            edge_linewidth=2,
            show=False,
            close=False,
        )

    # Overlay S-Bahn lines if requested and available
    if G_sbahn_proj:
        ox.plot_graph(
            G_sbahn_proj,
            ax=ax,
            node_size=0,
            edge_color=(0, 0.4, 0),  # dark green
            edge_linewidth=2,
            show=False,
            close=False,
        )

    # Set plot limits with margin
    margin = 500  # meters
    ax.set_xlim(minx - margin, maxx + margin)
    ax.set_ylim(miny - margin, maxy + margin)

    # Add scale bar
    scalebar = ScaleBar(
        dx=1,
        units="m",
        location="lower right",
        length_fraction=0.25,
        box_alpha=0.3,
        color="black",
        pad=0.5,
    )
    ax.add_artist(scalebar)

    # Save the figure

    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    if not quiet:
        print(f"Figure saved to: {save_path}")


# Example usage:
if __name__ == "__main__":
    plot_transport_network("Hannover, Germany", "../figures/v1_roads_trams_sbahn")
