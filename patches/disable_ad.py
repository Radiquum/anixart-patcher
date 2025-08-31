"""Disable ad banners"""

priority = 0
from typing import TypedDict

from scripts.smali_parser import (
    find_smali_method_end,
    find_smali_method_start,
    get_smali_lines,
    replace_smali_method_body,
)


class PatchConfig_DisableAdBanner(TypedDict):
    src: str


replace = """    .locals 0

    const/4 p0, 0x1

    return p0    
"""


def apply(config: PatchConfig_DisableAdBanner) -> bool:
    path = f"{config['src']}/smali_classes2/com/swiftsoft/anixartd/Prefs.smali"
    lines = get_smali_lines(path)
    for index, line in enumerate(lines):
        if line.find("IS_SPONSOR") >= 0:
            method_start = find_smali_method_start(lines, index)
            method_end = find_smali_method_end(lines, index)
            new_content = replace_smali_method_body(
                lines, method_start, method_end, replace
            )

            with open(path, "w", encoding="utf-8") as file:
                file.writelines(new_content)
    return True
