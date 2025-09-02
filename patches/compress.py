"""Remove unnecessary resources"""

# patch settings
# priority, default: 0
priority = 0

# imports
## bundled
import os
import shutil
from typing import TypedDict

## installed
from rich.progress import track

## custom
from config import config, log, console


# Patch

class PatchConfig_Compress(TypedDict):
    keep_dirs: list[str]

def apply(patch_config: PatchConfig_Compress) -> bool:
    path = f"{config['folders']['decompiled']}/unknown"
    items = os.listdir(path)

    for item in track(
        items,
        console=console,
        description="[COMPRESS]",
        total=len(items),
    ):
        item_path = f"{path}/{item}"
        if os.path.isfile(item_path):
            os.remove(item_path)
            log.debug(f"[COMPRESS] removed file: {item_path}")
        elif os.path.isdir(item_path):
            if item not in patch_config["keep_dirs"]:
                shutil.rmtree(item_path)
                log.debug(f"[COMPRESS] removed directory: {item_path}")

    log.debug(f"[COMPRESS] resources have been removed")
    return True
