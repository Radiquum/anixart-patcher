"""Changes the version string and build number"""
# Developer: Radiquum

# patch settings
# priority, default: -98
priority = -98

# imports
## bundled
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

    return True
