"""Change package name"""

priority = -100

import os
from typing import TypedDict

class PatchConfig_ChangePackageName(TypedDict):
    src: str
    new_package_name: str

def rename_dir(src, dst):
    os.makedirs(dst, exist_ok=True)
    os.rename(src, dst)

def apply(config: dict) -> bool:
    assert config["new_package_name"] is not None, "new_package_name is not configured"

    for root, dirs, files in os.walk(f"{config['src']}"):
        for filename in files:
            file_path = os.path.join(root, filename)

            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        file_contents = file.read()

                    new_contents = file_contents.replace(
                        "com.swiftsoft.anixartd", config["new_package_name"]
                    )
                    new_contents = new_contents.replace(
                        "com/swiftsoft/anixartd",
                        config["new_package_name"].replace(".", "/"),
                    )

                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(new_contents)
                except:
                    pass

    if os.path.exists(f"{config['src']}/smali/com/swiftsoft/anixartd"):
        rename_dir(
            f"{config['src']}/smali/com/swiftsoft/anixartd",
            os.path.join(
                f"{config['src']}", "smali", config["new_package_name"].replace(".", "/")
            ),
        )

    if os.path.exists(f"{config['src']}/smali_classes2/com/swiftsoft/anixartd"):
        rename_dir(
            f"{config['src']}/smali_classes2/com/swiftsoft/anixartd",
            os.path.join(
                f"{config['src']}",
                "smali_classes2",
                config["new_package_name"].replace(".", "/"),
            ),
        )

    return True