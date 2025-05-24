import argparse
from pathlib import Path

import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

from osmnx_plots.location_lists.germany import brandenburg_10, germany_100
from osmnx_plots.plot_templates import plot_transport_network
from osmnx_plots.utils.tools import list_to_random_number_dict

templates = dict(germany_100=germany_100, brandenburg_10=brandenburg_10)


def main():
    parser = argparse.ArgumentParser(description="Save a dictionary as a TSV file.")
    parser.add_argument(
        "--output_dir",
        type=Path,
        required=True,
        help="Directory where the file will be saved",
        default="figures/v1_roads_dict",
    )
    parser.add_argument(
        "--encoded", action="store_true", help="If set, the encoded flag will be True"
    )
    parser.add_argument(
        "--place_names",
        nargs="+",
        type=str,
        default=None,  # Explicitly set default to None
        help='List of place names, each in double quotes if containing spaces (e.g. --place_names "Paris, France" "Berlin, Germany")',
    )
    parser.add_argument(
        "--template",
        type=str,
        choices=list(templates.keys()),
        default=None,
        help=f"Choose a template from: {list(templates.keys())} (default: brandenburg_10)",
    )
    parser.add_argument(
    "--n_jobs",
    type=int,
    default=1,
    help="Number of parallel jobs to use (default: 1)",
    )
    args = parser.parse_args()

    # setup location names
    if args.place_names:
        places_list = args.place_names
    else:
        places_list = templates[args.template]

    places_dict = list_to_random_number_dict(places_list)

    # Directory to save figure
    save_dir = args.output_dir
    save_dir.mkdir(exist_ok=True)
    print(f"Saving outputs to {save_dir}")
    print(f"Running process with {args.n_jobs} parallel job(s)")
    
    if args.encoded:
        print(
            "File names will be encoded to a random id. Please check the location_ids.tab file"
        )
        # Create output legend
        df = pd.DataFrame(list(places_dict.items()), columns=["place", "random_number"])
        df = df[["random_number", "place"]].sort_values(
            by="random_number", ascending=True
        )
        df.to_csv(save_dir / "location_ids.tab", sep="\t", index=False)

        Parallel(n_jobs=args.n_jobs)(
            delayed(plot_transport_network)(
                place_name=place,
                save_dir=save_dir,
                layers=[],
                identifier=places_dict[place],
            )
            for place in tqdm(places_dict.keys())
        )
    else:
        Parallel(n_jobs=args.n_jobs)(
            delayed(plot_transport_network)(
                place_name=place, save_dir=save_dir, layers=[]
            )
            for place in tqdm(places_dict.keys())
        )


if __name__ == "__main__":
    main()
