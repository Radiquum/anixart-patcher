"""Changes the version string and build number"""
# Developer: Radiquum

# patch settings
# priority, default: -98
priority = -98

# imports
## bundled
import os
from typing import TypedDict

## installed
import yaml

## custom
from config import config, log


# Patch
class PatchConfig_ChangeAppVersion(TypedDict):
    _internal_app_version: str
    _internal_app_build: int
    version_name: str
    version_code: int


def apply(patch_conf: PatchConfig_ChangeAppVersion) -> bool:
    apktool_yaml = None
    with open(
        f"{config['folders']['decompiled']}/apktool.yml", "r", encoding="utf-8"
    ) as f:
        apktool_yaml = yaml.load(f.read(), Loader=yaml.Loader)

    apktool_yaml.update(
        {
            "versionInfo": {
                "versionName": patch_conf["version_name"]
                or patch_conf["_internal_app_version"],
                "versionCode": patch_conf["version_code"]
                or patch_conf["_internal_app_build"],
            }
        }
    )

    with open(
        f"{config['folders']['decompiled']}/apktool.yml", "w", encoding="utf-8"
    ) as f:
        apktool_yaml = yaml.dump(apktool_yaml, f, indent=2, Dumper=yaml.Dumper)

    for root, dirs, files in os.walk(f"{config['folders']['decompiled']}"):
        if len(files) < 0:
            continue

        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path) and filename.endswith(".smali"):
                file_contents = None
                with open(file_path, "r", encoding="utf-8") as file:
                    file_contents = file.read()

                if file_contents.find(str(patch_conf["_internal_app_build"])) >= 0 or file_contents.find(
                    hex(patch_conf["_internal_app_build"])
                ) >= 0:
                    file_contents = file_contents.replace(
                        str(patch_conf["_internal_app_build"]),
                        str(patch_conf["version_code"]) or str(patch_conf["_internal_app_build"]),
                    )
                    file_contents = file_contents.replace(
                        hex(patch_conf["_internal_app_build"]),
                        hex(patch_conf["version_code"]) or hex(patch_conf["_internal_app_build"]),
                    )
                    log.debug(f"replaced build number in file: {file_path}")
                    log.debug(f"previous: {patch_conf["_internal_app_build"]} ({hex(patch_conf['_internal_app_build'])})")
                    log.debug(f"replaced: {patch_conf["version_code"]} ({hex(patch_conf['version_code'])})")

                if file_contents.find(patch_conf["_internal_app_version"]) >= 0:
                    file_contents = file_contents.replace(
                        patch_conf["_internal_app_version"],
                        patch_conf["version_name"] or patch_conf["_internal_app_version"],
                    )
                    log.debug(f"replaced version name in file: {file_path}")
                    log.debug(f"previous: {patch_conf["_internal_app_build"]}")
                    log.debug(f"replaced: {patch_conf["version_code"]}")

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(file_contents)

    return True
