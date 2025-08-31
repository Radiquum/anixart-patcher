"""Remove unnecessary resources"""

priority = 0
from tqdm import tqdm

import os
import shutil
from typing import TypedDict

class PatchConfig_Compress(TypedDict):
    src: str
    keep_dirs: list[str]

def apply(config: PatchConfig_Compress) -> bool:
    for item in os.listdir(f"{config['src']}/unknown/"):
        item_path = os.path.join(f"{config['src']}/unknown/", item)

        if os.path.isfile(item_path):
            os.remove(item_path)
            tqdm.write(f"removed file: {item_path}")
        elif os.path.isdir(item_path):
            if item not in config["keep_dirs"]:
                shutil.rmtree(item_path)
                tqdm.write(f"removed directory: {item_path}")
    return True
