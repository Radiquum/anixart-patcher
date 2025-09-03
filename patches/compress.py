"""Remove and compress resources"""

# patch settings
# priority, default: 0
priority = 100

# imports
## bundled
import os
import shutil
import subprocess
from typing import TypedDict

## custom
from config import config, log
from scripts.smali_parser import get_smali_lines, save_smali_lines


# Patch
class PatchConfig_Compress(TypedDict):
    keep_dirs: list[str]


def remove_files(patch_config: PatchConfig_Compress):
    path = f"{config['folders']['decompiled']}/unknown"

    items = os.listdir(path)
    for item in items:
        item_path = f"{path}/{item}"
        if os.path.isfile(item_path):
            os.remove(item_path)
            log.debug(f"[COMPRESS] removed file: {item_path}")
        elif os.path.isdir(item_path):
            if item not in patch_config["keep_dirs"]:
                shutil.rmtree(item_path)
                log.debug(f"[COMPRESS] removed directory: {item_path}")


def remove_debug_lines():
    for root, dirs, files in os.walk(f"{config['folders']['decompiled']}"):
        if len(files) < 0:
            continue

        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path) and filename.endswith(".smali"):
                file_content = get_smali_lines(file_path)
                new_content = []
                for line in file_content:
                    if line.find(".line") >= 0:
                        continue
                    new_content.append(line)
                save_smali_lines(file_path, new_content)

            log.debug(f"[COMPRESS] removed debug lines from: {file_path}")


def compress_png(png_path: str):
    try:
        subprocess.run(
            [
                "pngquant",
                "--force",
                "--ext",
                ".png",
                png_path,
            ],
            check=True,
            capture_output=True,
        )
        log.debug(f"[COMPRESS] compressed png: {png_path}")
    except subprocess.CalledProcessError as e:
        log.error(
            f"error of running a command: %s :: %s",
            " ".join(
                [
                    "pngquant",
                    "--force",
                    "--ext",
                    ".png",
                    png_path,
                ]
            ),
            e.stderr,
            exc_info=True,
        )
        exit(1)


def compress_pngs():
    compressed = []
    for root, _, files in os.walk(f"{config['folders']['decompiled']}"):
        if len(files) < 0:
            continue

        for file in files:
            if file.lower().endswith(".png"):
                compress_png(f"{root}/{file}")
                compressed.append(f"{root}/{file}")

    log.debug(f"[COMPRESS] {len(compressed)} pngs have been compressed")


def apply(patch_config: PatchConfig_Compress) -> bool:

    remove_files(patch_config)
    remove_debug_lines()
    # compress_pngs()

    return True
