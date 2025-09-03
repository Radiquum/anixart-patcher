"""Change app color theme"""

# patch settings
# priority, default: -99 (run before last)
priority = -99

# imports
## bundled
from typing import TypedDict
from beaupy import select

## installed
from lxml import etree

## custom
from config import config, log, console


class PatchConfig_ChangeColorThemeValue(TypedDict):
    attributes: list[dict[str, str]]
    text: list[dict[str, str]]
    files: list[dict[str, str]]


class PatchConfig_ChangeColorTheme(TypedDict):
    themes: list[str]
    key: PatchConfig_ChangeColorThemeValue


def apply(patch_config: PatchConfig_ChangeColorTheme) -> bool:

    console.print("select color theme to apply (press [bold]enter[/bold] to confirm)")
    theme = select(patch_config["themes"], cursor="->", cursor_style="cyan")
    if not theme:
        console.print(f"theme: default")
        return False
    console.print(f"theme: {theme}")

    theme_attr = patch_config[theme]["attributes"]
    theme_text = patch_config[theme]["text"]
    theme_files = patch_config[theme]["files"]

    for item in theme_attr:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(
            f"{config['folders']['decompiled']}/{item['file_path']}", parser
        )
        root = tree.getroot()
        root.find(item["tag_path"]).set(item["attr_name"], item["attr_value"]["to"])
        tree.write(
            f"{config['folders']['decompiled']}/{item['file_path']}",
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )
        log.debug(
            f"[CHANGE_COLOR_THEME/ATTRIBUTES] set attribute `{item['attr_name']}` from `{item['attr_value']['from']}` to `{item['attr_value']['to']}`"
        )

    for item in theme_text:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(
            f"{config['folders']['decompiled']}/{item['file_path']}", parser
        )
        root = tree.getroot()
        root.find(item["tag_path"]).text = item["text"]["to"]
        tree.write(
            f"{config['folders']['decompiled']}/{item['file_path']}",
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )
        log.debug(
            f"[CHANGE_COLOR_THEME/VALUES] set text from `{item['text']['from']}` to `{item['text']['to']}`"
        )

    if len(theme_files) > 0:
        for item in theme_files:
            with open(
                f"{config['folders']['decompiled']}/{item['file_path']}",
                "w",
                encoding="utf-8",
            ) as f:
                f.write("\n".join(item["file_content"]))
            log.debug(f"[CHANGE_COLOR_THEME/FILES] replaced file {item['file_path']}")

    log.debug(f"[CHANGE_COLOR_THEME] color theme `{theme}` has been applied")
    return True
