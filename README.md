# OSMnx Plots Batch Script

This script automates the generation and saving of OSMnx transport network plots for a list of places. You can use predefined templates (e.g., `germany_100`, `brandenburg_10`) or provide your own list of places via the command line. Optionally, filenames can be anonymized and a mapping table can be exported.

## Features

- Parallel processing of multiple locations for fast results
- Selection from predefined place templates (`germany_100`, `brandenburg_10`)
- Add custom places via command line arguments
- Optional anonymized filenames (random IDs)
- Export of the mapping table as a TSV file

## Requirements

- Python 3.11 or newer
- All dependencies installed (see `pyproject.toml` or install via `pip install -r requirements.txt`)

## Usage

### Basic usage

```
python your_script.py --output_dir ./output_directory
```

### Use a place template

```
python your_script.py --output_dir ./output_directory --template germany_100
```

### Provide your own list of places

```
python your_script.py --output_dir ./output_directory --place_names "Paris, France" "Berlin, Germany"
```

### Anonymize filenames and export the mapping table

```
python your_script.py --output_dir ./output_directory --encoded
```

### Combine all options

```
python your_script.py --output_dir ./output_directory --template germany_100 --encoded --place_names "Paris, France" "London, UK"
```

## Arguments

| Argument         | Type     | Description                                                                                          |
|------------------|----------|------------------------------------------------------------------------------------------------------|
| `--output_dir`   | Path     | **Required.** Directory where plots and the mapping table will be saved.                             |
| `--template`     | String   | Place template to use, e.g., `germany_100` or `brandenburg_10`. Default: `brandenburg_10`.           |
| `--place_names`  | Strings  | Custom place names (each in double quotes if containing spaces). Overrides the template if provided.  |
| `--encoded`      | Flag     | If set, filenames will be anonymized and a mapping table will be saved.                              |

## Example Output

- Transport network plots in the specified output directory
- If `--encoded` is set: a `location_ids.tab` file mapping random IDs to place names

## Notes

- If `--place_names` is provided, only those places will be used (the template is ignored).
- Parallel processing uses 3 jobs by default (adjustable in the script).
- Each place name with spaces must be wrapped in double quotes.

---

**Happy plotting!** 🚀
