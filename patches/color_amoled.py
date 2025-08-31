"""Set background to full black (amoled)"""

priority = -90

from typing import TypedDict
from lxml import etree
from tqdm import tqdm


class PatchConfig_ColorAmoled(TypedDict):
    src: str


def apply(config: dict) -> bool:
    res_xmls = [
        "res/values/colors.xml",
        "res/values/styles.xml",
        "res/values-night/colors.xml",
        "res/values-night-v29/styles.xml",
        "res/values-night-v31/styles.xml",
    ]

    for xml in res_xmls:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(f"{config['src']}/{xml}", parser)
        root = tree.getroot()

        if xml == "res/values/styles.xml":
            attributes = [
                "android:colorBackground",
                "android:statusBarColor",
                "colorOnBackground",
            ]

            for tag in root:
                if tag.get("name") == "AppTheme.SwiftPlayer":
                    for child in tag:
                        if child.get("name") in attributes:
                            child.text = "#ff000000"
                            tqdm.write(
                                f'set color in {xml} - {child.get("name")} to #ff000000'
                            )

        if xml == "res/values/colors.xml":
            attributes = [
                "design_dark_default_color_background",
                "design_dark_default_color_surface",
            ]

            for child in root:
                if child.get("name") in attributes:
                    child.text = "#ff000000"
                    tqdm.write(f'set color in {xml} - {child.get("name")} to #ff000000')

        if xml == "res/values-night/colors.xml":
            attributes = [
                {"item": "bottom_nav_background", "value": "#ff000000"},
                {"item": "collection_card_header", "value": "#ff252525"},
                {"item": "light_md_blue_50", "value": "#ff121212"},
                {"item": "light_md_deep_orange_50", "value": "#ff121212"},
                {"item": "light_md_green_50", "value": "#ff121212"},
                {"item": "light_md_pink_50", "value": "#ff121212"},
                {"item": "light_md_purple_50", "value": "#ff121212"},
                {"item": "light_md_teal_50", "value": "#ff121212"},
                {"item": "refresh_background", "value": "#ff121212"},
                {"item": "screen_background", "value": "#ff000000"},
                {"item": "screen_background_alpha_50", "value": "#80000000"},
                {"item": "screen_background_alpha_80", "value": "#cb000000"},
                {"item": "screen_background_transparent", "value": "#00000000"},
                {"item": "search_bar_alt", "value": "#ff121212"},
                {"item": "switch_surface", "value": "#ff000000"},
                {"item": "tg_background_color", "value": "#ff121212"},
                {"item": "vk_background_color", "value": "#ff121212"},
            ]

            for attr in attributes:
                elem = root.find(f".//*[@name='{attr["item"]}']")
                elem.text = attr["value"]
                tqdm.write(
                    f'set color in {xml} - {elem.get("name")} to {attr["value"]}'
                )
        
        if xml == "res/values-night-v29/styles.xml":
            attributes = [
                {"item": "backgroundColorSecondary", "value": "#ff121212"},
                {"item": "android:colorBackground", "value": "#ff000000"},
                {"item": "android:statusBarColor", "value": "#ff000000"},
                {"item": "android:navigationBarColor", "value": "#ff000000"},
                {"item": "backgroundColorSecondary", "value": "#ff121212"},
                {"item": "colorOnBackground", "value": "#ff000000"},
                {"item": "colorSurface", "value": "#ff000000"},
                {"item": "deleteButtonColor", "value": "#ff121212"},
                {"item": "editButtonColor", "value": "#ff121212"},
                {"item": "placeholderStart", "value": "#ff252525"},
                {"item": "progressBackTint", "value": "#ff252525"},
                {"item": "secondaryButtonColor", "value": "#ff121212"},
            ]

            for attr in attributes:
                elem = root.find(f".//*[@name='{attr["item"]}']")
                elem.text = attr["value"]
                tqdm.write(
                    f'set color in {xml} - {elem.get("name")} to {attr["value"]}'
                )

        if xml == "res/values-night-v31/styles.xml":
            attributes = [
                "android:windowSplashScreenBackground",
                "android:navigationBarColor",
                "android:windowSplashScreenBackground",
                "colorOnBackground",
            ]

            for tag in root:
                for child in tag:
                    if child.get("name") in attributes:
                        child.text = "#ff000000"
                        tqdm.write(
                            f'set color in {xml} - {child.get("name")} to #ff000000'
                        )

        tree.write(
            f"{config['src']}/{xml}",
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )
        tqdm.write(f"changed color values: {config['src']}/{xml}")

    return True
