"""Move and replace navigation bar tabs"""

# patch settings
# priority, default: 0
priority = 0

# imports
## bundled
from typing import TypedDict

## installed
from lxml import etree

## custom
from config import config, log


# Patch
class PatchConfig_ChangeNavigationBar(TypedDict):
    portrait: list[str]
    landscape: list[str]


allowed_items = ["home", "discover", "feed", "bookmarks", "profile"]


def modify_menu(menu: list[str], path: str) -> None:
    for item in menu:
        if item not in allowed_items:
            log.warning(f"menu item `{item}` is not allowed, removing from list")
            menu.remove(item)

    root = etree.Element("menu", nsmap={"android": config['xml_ns']['android']})
    for item in menu:
        element = etree.SubElement(root, "item")
        element.set(f"{{{config['xml_ns']['android']}}}icon", f"@drawable/nav_{item}")
        element.set(f"{{{config['xml_ns']['android']}}}id", f"@id/tab_{item}")
        element.set(f"{{{config['xml_ns']['android']}}}title", f"@string/{item}")

    tree = etree.ElementTree(root)
    tree.write(
        path,
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    )


def apply(patch_conf: PatchConfig_ChangeNavigationBar) -> bool:
    modify_menu(patch_conf["portrait"], f"{config['folders']['decompiled']}/res/menu/bottom.xml")
    modify_menu(patch_conf["landscape"], f"{config['folders']['decompiled']}/res/menu/navigation_rail_menu.xml")
    return True
