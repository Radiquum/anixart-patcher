"""Change package name"""

# patch settings
# priority, default: -100 (run last)
priority = -100

# imports
## bundled
import os
from typing import TypedDict

## custom
from config import config, log


class PatchConfig_ChangePackageName(TypedDict):
    new_package_name: str


def rename_dir(src, dst):
    os.makedirs(dst, exist_ok=True)
    os.rename(src, dst)


def apply(patch_config: PatchConfig_ChangePackageName) -> bool:
    assert (
        patch_config["new_package_name"] is not None
    ), "new_package_name is not configured"

    for root, dirs, files in os.walk(f"{config['folders']['decompiled']}"):
        if len(files) < 0:
            continue

        dir_name = root.removeprefix(f"{config['folders']['decompiled']}/")

        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        file_contents = file.read()

                    new_contents = file_contents.replace(
                        "com.swiftsoft.anixartd", patch_config["new_package_name"]
                    )
                    new_contents = new_contents.replace(
                        "com/swiftsoft/anixartd",
                        patch_config["new_package_name"].replace(".", "/"),
                    )

                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(new_contents)
                except:
                    pass

    if os.path.exists(
        f"{config['folders']['decompiled']}/smali/com/swiftsoft/anixartd"
    ):
        rename_dir(
            f"{config['folders']['decompiled']}/smali/com/swiftsoft/anixartd",
            os.path.join(
                f"{config['folders']['decompiled']}",
                "smali",
                patch_config["new_package_name"].replace(".", "/"),
            ),
        )

    if os.path.exists(
        f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd"
    ):
        rename_dir(
            f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd",
            os.path.join(
                f"{config['folders']['decompiled']}",
                "smali_classes2",
                patch_config["new_package_name"].replace(".", "/"),
            ),
        )

    log.debug(
        f"[CHANGE_PACKAGE_NAME] package name has been changed to {patch_config['new_package_name']}"
    )
    return True
