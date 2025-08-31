"""Remove beta banner"""

priority = 0
import os
from tqdm import tqdm
from lxml import etree

from typing import TypedDict


class PatchConfig_DisableBetaBanner(TypedDict):
    src: str


def apply(config: PatchConfig_DisableBetaBanner) -> bool:
    xml_ns = {
        "android": "http://schemas.android.com/apk/res/android",
        "app": "http://schemas.android.com/apk/res-auto",
    }
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
        "layout_marginEnd"
    ]

    beta_banner_xml = f"{config['src']}/res/layout/item_beta.xml"
    if os.path.exists(beta_banner_xml):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(beta_banner_xml, parser)
        root = tree.getroot()
        
        for attr in attributes:
            tqdm.write(f"set {attr} = 0.0dip")
            root.set(f"{{{xml_ns['android']}}}{attr}", "0.0dip")

        tree.write(beta_banner_xml, pretty_print=True, xml_declaration=True, encoding="utf-8")

    return True
