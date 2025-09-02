"""Remove beta banner"""

# patch settings
# priority, default: 0
priority = 0

# imports
## bundled
import os

## installed
from lxml import etree

## custom
from config import config, log


def apply(__no_config__) -> bool:
    beta_banner_xml = f"{config['folders']['decompiled']}/res/layout/item_beta.xml"
    attributes = [
        "paddingTop",
        "paddingBottom",
        "paddingStart",
        "paddingEnd",
        "layout_width",
        "layout_height",
        "layout_marginTop",
        "layout_marginBottom",
        "layout_marginStart",
        "layout_marginEnd",
    ]

    if os.path.exists(beta_banner_xml):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(beta_banner_xml, parser)
        root = tree.getroot()

        for attr in attributes:
            log.debug(
                f"[DISABLE_BETA_BANNER] set attribute `{attr}` from `{root.get(attr)}` to `0.0dip`"
            )
            root.set(f"{{{config['xml_ns']['android']}}}{attr}", "0.0dip")

        tree.write(
            beta_banner_xml, pretty_print=True, xml_declaration=True, encoding="utf-8"
        )

    log.debug(f"[DISABLE_BETA_BANNER] file {beta_banner_xml} has been modified")
    return True
