"""Set background to full black (amoled)"""

priority = -91

from typing import TypedDict
from lxml import etree
from tqdm import tqdm


class PatchConfig_ColorAmoled(TypedDict):
    src: str
    patches: list[str]


def apply(config: PatchConfig_ColorAmoled) -> bool:
    xml_ns = {
        "android": "http://schemas.android.com/apk/res/android",
        "app": "http://schemas.android.com/apk/res-auto",
    }
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

        if xml == "res/values/colors.xml":
            attributes = [
                "design_dark_default_color_background",
                "design_dark_default_color_surface",
            ]

            for child in root:
                if child.get("name") in attributes:
                    child.text = "#ff000000"
                    tqdm.write(f'set color in {xml} - {child.get("name")} to #ff000000')

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

    if "color_material_ui" in config["patches"]:
        res_xmls = [
            "res/layout-night/item_radio_notification_status_all_selected.xml",
            "res/layout-night/item_radio_notification_status_release.xml",
            "res/values-night/colors.xml",
            "res/values-night/styles.xml",
            "res/values-night-v29/styles.xml",
        ]
        for xml in res_xmls:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(f"{config['src']}/{xml}", parser)
            root = tree.getroot()
            
            if xml == "res/layout-night/item_radio_notification_status_all_selected.xml":
                root[1].set(f"{{{xml_ns['android']}}}backgroundTint", "@android:color/system_neutral2_800")
                root[3].set(f"{{{xml_ns['android']}}}backgroundTint", "@android:color/system_neutral2_800")
            elif xml == "res/layout-night/item_radio_notification_status_release.xml":
                root[0][1].set(f"{{{xml_ns['android']}}}backgroundTint", "@android:color/system_neutral2_800")
                root[1][0].set(f"{{{xml_ns['android']}}}backgroundTint", "@android:color/system_neutral2_800")
            elif xml == "res/values-night/colors.xml":
                attributes = [
                    {"item": "accent_alpha_10", "value": "@android:color/system_neutral2_900"},
                    {"item": "blue_secondary", "value": "@android:color/system_neutral2_800"},
                    {"item": "bottom_nav_background", "value": "#ff000000"},
                    {"item": "bottom_nav_indicator_active", "value": "@android:color/system_neutral2_800"},
                    {"item": "collection_card_header", "value": "@android:color/system_neutral2_800"},
                    {"item": "light_md_blue_50", "value": "@android:color/system_neutral2_900"},
                    {"item": "light_md_deep_orange_50", "value": "@android:color/system_neutral2_900"},
                    {"item": "light_md_green_50", "value": "@android:color/system_neutral2_900"},
                    {"item": "light_md_pink_50", "value": "@android:color/system_neutral2_900"},
                    {"item": "light_md_purple_50", "value": "@android:color/system_neutral2_900"},
                    {"item": "light_md_teal_50", "value": "@android:color/system_neutral2_900"},
                    {"item": "refresh_background", "value": "@android:color/system_neutral2_900"},
                    {"item": "screen_background", "value": "#ff000000"},
                    {"item": "search_bar_alt", "value": "#ff000000"},
                    {"item": "separator_alpha_3", "value": "@android:color/system_neutral2_900"},
                    {"item": "switch_surface", "value": "@android:color/system_neutral2_800"},
                    {"item": "tg_background_color", "value": "@android:color/system_neutral2_900"},
                    {"item": "tooltip_background", "value": "@android:color/system_neutral2_800"},
                    {"item": "torlook_background", "value": "@android:color/system_neutral2_900"},
                    {"item": "vk_background_color", "value": "@android:color/system_neutral2_900"},
                    {"item": "yellow_secondary", "value": "@android:color/system_neutral1_900"}
                ]
                with tqdm(
                    total=len(attributes), desc="res/values-night/colors.xml", unit_divisor=1
                ) as bar:
                    for attr in attributes:
                        elem = root.find(f".//*[@name='{attr["item"]}']")
                        elem.text = attr["value"]
                        bar.update()
            elif xml == "res/values-night/styles.xml":
                for child in root:
                    if child.get("name") == "AnixButton.Bottom":
                        child.find(".//*[@name='android:backgroundTint']").text = "@android:color/system_neutral2_800"
            elif xml == "res/values-night-v29/styles.xml":
                attributes = [
                    {"item": "android:colorBackground", "value": "#ff000000"},
                    {"item": "android:statusBarColor", "value": "#ff000000"},
                    {"item": "android:navigationBarColor", "value": "#ff000000"},
                    {"item": "backgroundColorSecondary", "value": "#ff000000"},
                    {"item": "backgroundColorTertiary", "value": "@android:color/system_neutral2_900"},
                    {"item": "colorOnBackground", "value": "#ff000000"},
                    {"item": "colorSurface", "value": "#ff000000"},
                    {"item": "deleteButtonColor", "value": "@android:color/system_neutral2_900"},
                    {"item": "editButtonColor", "value": "@android:color/system_neutral2_900"},
                    {"item": "invertColor", "value": "@android:color/system_neutral2_900"},
                    {"item": "placeholderStart", "value": "@android:color/system_neutral1_900"},
                    {"item": "progressBackTint", "value": "@android:color/system_neutral1_900"},
                    {"item": "secondaryButtonColor", "value": "@android:color/system_neutral2_900"}
                ]
                for attr in attributes:
                    elem = root.find(f".//*[@name='{attr["item"]}']")
                    elem.text = attr["value"]
                    tqdm.write(
                        f'set color in {xml} - {elem.get("name")} to {attr["value"]}'
                    )
            elif xml == "res/values-night-v31/styles.xml":
                with open(f"{config['src']}/{xml}", "w", encoding="utf-8") as file:
                    file.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="@style/BaseTheme">
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowSplashScreenBackground">#ff000000</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/logo_splash_anim</item>
        <item name="android:windowSplashScreenAnimationDuration">500</item>
    </style>
    <style name="AppTheme.Start" parent="@style/AppTheme">
        <item name="android:navigationBarColor">#ff000000</item>
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowSplashScreenBackground">#ff000000</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/logo_splash_anim</item>
        <item name="android:windowSplashScreenAnimationDuration">500</item>
        <item name="colorOnBackground">#ff000000</item>
        <item name="primaryTextColor">@android:color/system_neutral1_50</item>
        <item name="secondaryTextColor">@android:color/system_neutral2_200</item>
        <item name="tertiaryTextColor">@android:color/system_neutral1_200</item>
    </style>
</resources>""")

            tree.write(
                f"{config['src']}/{xml}",
                pretty_print=True,
                xml_declaration=True,
                encoding="utf-8",
            )
            tqdm.write(f"changed color values: {config['src']}/{xml}")

    return True

## TODO! Fix or Rewrite for compatibility with color_material_ui!
## Right now Bottom bar and Tab bar is not colored to black properly