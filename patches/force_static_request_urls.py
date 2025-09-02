"""Change `value="something/endpoint"` to `value="https://example.com/something/endpoint" """

# patch settings
# priority, default: 0
priority = 0

# imports
## bundled
import os
from typing import TypedDict

## custom
from config import config, log
from scripts.smali_parser import (
    get_smali_lines,
    save_smali_lines,
    find_and_replace_smali_line,
    find_smali_method_start,
    find_smali_method_end,
    replace_smali_method_body,
)


# Patch
class PatchConfig_ForceStaticRequestUrlsValue(TypedDict):
    file_path: str
    value: str


class PatchConfig_ForceStaticRequestUrlsConst(TypedDict):
    file_path: str
    _from: str
    _to: str


class PatchConfig_ForceStaticRequestUrls(TypedDict):
    base_url: str
    values: PatchConfig_ForceStaticRequestUrlsValue
    constants: PatchConfig_ForceStaticRequestUrlsConst


replace_should_use_mirror_urls = """    .locals 0

    const/4 p0, 0x0

    return p0    
"""


def apply(patch_config: PatchConfig_ForceStaticRequestUrls) -> bool:
    for value in patch_config["values"]:
        if os.path.exists(f"{config['folders']['decompiled']}/{value['file_path']}"):
            path = f"{config['folders']['decompiled']}/{value['file_path']}"
            lines = get_smali_lines(path)
            lines = find_and_replace_smali_line(
                lines, value["value"], f"{patch_config['base_url']}{value['value']}"
            )
            save_smali_lines(path, lines)
            log.debug(f"[FORCE_STATIC_REQUEST_URLS] file {path} has been modified")

    for const in patch_config["constants"]:
        if os.path.exists(f"{config['folders']['decompiled']}/{const['file_path']}"):
            path = f"{config['folders']['decompiled']}/{const['file_path']}"
            lines = get_smali_lines(path)
            replace_value = ""
            try:
                replace_value = const["to"]
            except:
                replace_value = patch_config["base_url"]
            lines = find_and_replace_smali_line(lines, const["from"], replace_value)
            save_smali_lines(path, lines)
            log.debug(f"[FORCE_STATIC_REQUEST_URLS] file {path} has been modified")

    # IDK If it is actually needed, will leave it for now, but seems like it should not be needed, since patch is working
    # path = f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd/Prefs.smali"
    # if os.path.exists(path):
    #     lines = get_smali_lines(path)
    #     new_content = []
    #     for index, line in enumerate(lines):
    #         if line.find("SHOULD_USE_MIRROR_URLS") >= 0:
    #             method_start = find_smali_method_start(lines, index)
    #             method_end = find_smali_method_end(lines, index)
    #             new_content = replace_smali_method_body(
    #                 lines, method_start, method_end, replace_should_use_mirror_urls
    #             )
    #     save_smali_lines(path, new_content)
    #     log.debug(f"[FORCE_STATIC_REQUEST_URLS] file {path} has been modified")

    path = f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd/DaggerApp_HiltComponents_SingletonC$SingletonCImpl$SwitchingProvider.smali"
    pathInterceptor = f"{config['folders']['decompiled']}/smali_classes2/com/swiftsoft/anixartd/dagger/module/ApiModule$provideRetrofit$lambda$2$$inlined$-addInterceptor$1.smali"
    if os.path.exists(path) and os.path.exists(pathInterceptor):
        lines = get_smali_lines(path)
        new_content = []
        for index, line in enumerate(lines):
            if line.find("addInterceptor") >= 0:
                    continue
            new_content.append(line)
        save_smali_lines(path, new_content)
        log.debug(f"[FORCE_STATIC_REQUEST_URLS] file {path} has been modified")


    return True
