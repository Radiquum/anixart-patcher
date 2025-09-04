"""Adds a patch and other infos to app settings"""

# patch settings
# priority, default: -95
priority = -95

# imports
## bundled
import os
import random
import string
from typing import TypedDict

## installed
from lxml import etree

## custom
from config import config, log


# Patch
class PatchConfig_AddSettingsMenuItems(TypedDict):
    _internal_all_patch_statuses: list
    add_patch_info: bool


def random_key():
    return "".join(random.choices(string.ascii_letters, k=8))


def add_separator():
    ns = config["xml_ns"]
    item = etree.Element("Preference", nsmap=ns)
    item.set(f"{{{ns['android']}}}layout", "@layout/preference_separator")
    item.set(f"{{{ns['android']}}}selectable", "false")
    item.set(f"{{{ns['android']}}}key", f"separator_{random_key()}")


def create_intent(
    action: str = "android.intent.action.VIEW",
    data: str | None = None,
):
    ns = config["xml_ns"]
    item = etree.Element("intent", nsmap=ns)
    item.set(f"{{{ns['android']}}}action", action)
    item.set(f"{{{ns['android']}}}data", data or "")
    item.set(f"{{{ns['app']}}}iconSpaceReserved", "false")
    item.set(f"{{{ns['android']}}}key", f"intent_{random_key()}")
    return item


def create_Preference(
    title: str,
    description: str | None = None,
    icon: str | None = None,
    icon_space_reserved: bool = False,
):
    ns = config["xml_ns"]
    item = etree.Element("Preference", nsmap=ns)
    item.set(f"{{{ns['android']}}}title", title)
    item.set(f"{{{ns['android']}}}summary", description or "")
    if icon:
        item.set(f"{{{ns['app']}}}icon", icon)
    item.set(f"{{{ns['app']}}}iconSpaceReserved", str(icon_space_reserved).lower())
    item.set(f"{{{ns['android']}}}key", f"preference_{random_key()}")
    return item


def create_PreferenceCategory(title: str):
    ns = config["xml_ns"]
    category = etree.Element("PreferenceCategory", nsmap=ns)
    category.set(f"{{{ns['android']}}}title", title)
    category.set(f"{{{ns['app']}}}iconSpaceReserved", "false")
    category.set(f"{{{ns['android']}}}key", f"category_{random_key()}")
    return category


def add_patch_info(patch_statuses: list):
    category = create_PreferenceCategory("Использованные патчи")
    for patch in patch_statuses:
        if patch["status"] is True:
            description = []
            url = None
            if os.path.exists(f"{config['folders']['patches']}/{patch['name']}.py"):
                with open(
                    f"{config['folders']['patches']}/{patch['name']}.py",
                    "r",
                    encoding="utf-8",
                ) as f:
                    line = f.readline()
                    if line.startswith('"""'):
                        description.append(line.strip().removeprefix('"""').removesuffix('"""').strip())
                    line = f.readline()
                    if line.startswith("# Developer:"):
                        description.append("by")
                        description.append(line.strip().removeprefix("# Developer:").strip())
                    line = f.readline()
                    if line.startswith("# URL:"):
                        url = line.strip().removeprefix("# URL:").strip()

            item = create_Preference(patch["name"].replace("_", " ").strip().title(), description=" ".join(description))
            if url:
                item.append(create_intent(data = url))
            category.append(item)
    return category


def apply(patch_conf: PatchConfig_AddSettingsMenuItems) -> bool:
    preference_main_xml = (
        f"{config['folders']['decompiled']}/res/xml/preference_main.xml"
    )
    preference_additional_xml = (
        f"{config['folders']['decompiled']}/res/xml/preference_additional.xml"
    )

    parser = etree.XMLParser(remove_blank_text=True)

    if os.path.exists(preference_additional_xml):
        tree = etree.parse(preference_additional_xml, parser)
        root = tree.getroot()

        if patch_conf["add_patch_info"]:
            root.append(add_patch_info(patch_conf["_internal_all_patch_statuses"]))

        tree.write(
            preference_additional_xml,
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )

    return True


if __name__ == "__main__":
    apply({})
