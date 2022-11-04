from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import yaml
from typing import Dict,Optional
from from_root import from_root

def get_tif_files(image_path):
    
    """
    Get all the .tif files in the image folder.
    Parameters
    ----------
    image_path: pathlib Path
        Directory to search for tif files
    Returns:
        A list of .tif filenames
    """
    files = []
    for dir_file in image_path.iterdir():
        if str(dir_file).endswith("tif"):
            files.append(str(dir_file.name))
    return files


def read_config(file_name: str) -> Dict:
    """
    This Function reads the config.yaml from root directory and
    return configuration in dictionary.
    Returns: Dict of config
    """
    #  config_path = os.path.join(from_root(), file_name)
    config_path = file_name
    with open(config_path) as config_file:
        content = yaml.safe_load(config_file)

    return content

def check_for_tif_file(filepath: Path, prefix: str) -> Optional[Path]:
    """
    Returns a filepath if one exists, else returns None. This is useful
    because sometimes, Earth Engine exports files with characters added
    to the end of the filename, e.g. {intended_filename}{-more stuff}.tif
    """
    # if (filepath / f"{prefix}.tif").exists():
    #     return filepath / f"{prefix}.tif"

    files_with_prefix = list(filepath.glob(f"*_{prefix}_*.tif"))
    if len(files_with_prefix) == 1:
        return files_with_prefix[0]
    elif len(files_with_prefix) == 0:
        return None
    elif len(files_with_prefix) > 1:
        print(f"Multiple files with prefix for {filepath /  prefix}.tif")
        return None



def create_dir(path):
    os.makedirs(path, exist_ok=True)