"""Set background to full black (amoled)"""

priority = -90

from typing import TypedDict
from lxml import etree
from tqdm import tqdm


class PatchConfig_ColorMUI(TypedDict):
    src: str


def apply(config: PatchConfig_ColorMUI) -> bool:
    xml_ns = {
        "android": "http://schemas.android.com/apk/res/android",
        "app": "http://schemas.android.com/apk/res-auto",
    }
    res_xmls = [
        "res/color/fab_efab_foreground_color_selector.xml",
        "res/drawable/bg_badge_square_regular.xml",
        "res/drawable/bg_custom_radio_buttons_selected_state.xml",
        "res/drawable/bg_imp_message.xml",
        "res/drawable/bg_notification_episode_indicator.xml",
        "res/drawable/bg_search_bar.xml",
        "res/drawable/button_release_announcement.xml",
        "res/drawable/sort_asc.xml",
        "res/drawable/sort_desc.xml",
        "res/drawable/tab_indicator.xml",
        "res/drawable-night/bg_badge_square_regular.xml",
        "res/drawable-night/bg_custom_radio_button_card_unselected_state.xml",
        "res/drawable-night/bg_custom_radio_buttons_selected_state.xml",
        "res/drawable-night/bg_custom_radio_buttons_unselected_state.xml",
        "res/drawable-night/button_release_announcement.xml",
        "res/layout/comments.xml",
        "res/layout/fragment_comments.xml",
        "res/layout/fragment_replies.xml",
        "res/layout/item_release_history.xml",
        "res/layout-night/item_radio_notification_status_all_selected.xml",
        "res/layout-night/item_radio_notification_status_release.xml",
        "res/values/colors.xml",
        "res/values/styles.xml",
        "res/values-night/colors.xml",
        "res/values-night/styles.xml",
        "res/values-v31/styles.xml",
        "res/values-night-v29/styles.xml",
        "res/values-night-v31/styles.xml",
    ]

    for xml in res_xmls:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(f"{config['src']}/{xml}", parser)
        root = tree.getroot()

        if xml == "res/color/fab_efab_foreground_color_selector.xml":
            for child in root:
                if child.get(f"{{{xml_ns['android']}}}color") == "?colorAccent":
                    child.set(f"{{{xml_ns['android']}}}color", "?colorPrimary")
                    break
        elif xml == "res/drawable/bg_badge_square_regular.xml":
            for child in root:
                if child.tag == "solid":
                    child.set(f"{{{xml_ns['android']}}}color", "#00000000")
                    break
        elif xml == "res/drawable/bg_custom_radio_buttons_selected_state.xml":
            for child in root:
                if child.tag == "solid":
                    child.set(f"{{{xml_ns['android']}}}color", "#15101010")
                    break
        elif xml == "res/drawable/bg_imp_message.xml":
            root[0][0][0].set(f"{{{xml_ns['android']}}}topRightRadius", "16.0dip")
            root[0][0][0].set(f"{{{xml_ns['android']}}}bottomRightRadius", "16.0dip")
            root[0][0][1].set(
                f"{{{xml_ns['android']}}}endColor", "@color/blue_secondary"
            )
        elif xml == "res/drawable/bg_notification_episode_indicator.xml":
            root[1][0][0].set(
                f"{{{xml_ns['android']}}}fillColor", "@android:color/system_neutral2_50"
            )
        elif xml == "res/drawable/bg_search_bar.xml":
            root[0][0][2].set(
                f"{{{xml_ns['android']}}}color", "@android:color/system_neutral1_100"
            )
        elif xml == "res/drawable/button_release_announcement.xml":
            root[1][0][1].set(
                f"{{{xml_ns['android']}}}startColor",
                "@android:color/system_neutral2_500",
            )
            root[1][0][1].set(
                f"{{{xml_ns['android']}}}endColor", "@android:color/system_accent3_600"
            )
        elif xml == "res/drawable/sort_asc.xml":
            root[0].set(f"{{{xml_ns['android']}}}fillColor", "?tertiaryTextColor")
        elif xml == "res/drawable/sort_desc.xml":
            root[0].set(f"{{{xml_ns['android']}}}fillColor", "?tertiaryTextColor")
        elif xml == "res/drawable/tab_indicator.xml":
            root[1].set(f"{{{xml_ns['android']}}}color", "?iconTintColor")
        elif xml == "res/drawable-night/bg_badge_square_regular.xml":
            root[0][0][1].set(f"{{{xml_ns['android']}}}color", "#00000000")
        elif (
            xml == "res/drawable-night/bg_custom_radio_button_card_unselected_state.xml"
        ):
            root[0][0][1].set(
                f"{{{xml_ns['android']}}}color", "@android:color/system_neutral2_500"
            )
        elif xml == "res/drawable-night/bg_custom_radio_buttons_selected_state.xml":
            root[0][0][1].set(f"{{{xml_ns['android']}}}color", "@color/md_grey_800")
            root[0][0][2].set(f"{{{xml_ns['android']}}}color", "#30909090")
        elif xml == "res/drawable-night/bg_custom_radio_buttons_unselected_state.xml":
            root[0][0][1].set(
                f"{{{xml_ns['android']}}}color", "@android:color/system_neutral2_600"
            )
        elif xml == "res/drawable-night/button_release_announcement.xml":
            root[1][0][1].set(
                f"{{{xml_ns['android']}}}startColor",
                "@android:color/system_accent3_500",
            )
            root[1][0][1].set(
                f"{{{xml_ns['android']}}}endColor", "@android:color/system_accent1_600"
            )
        elif xml == "res/layout/comments.xml":
            elem = root.find("RelativeLayout")
            elem = elem[0]
            elem.set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
            elem[0].set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
            elem[1].set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
            elem[1][1][1].set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
        elif xml == "res/layout/fragment_comments.xml":
            elem = root.find("RelativeLayout")
            elem[0].set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
            elem[0][0].set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
            elem[0][1].set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
            elem[0][1][1][1].set(
                f"{{{xml_ns['android']}}}background", "?android:colorBackground"
            )
        elif xml == "res/layout/fragment_replies.xml":
            elem = root.find("RelativeLayout")
            elem = elem.find("LinearLayout")
            elem[0][2].set(
                f"{{{xml_ns['app']}}}tint", "@android:color/system_accent3_400"
            )
            elem[2][1][1].set(
                f"{{{xml_ns['app']}}}tint", "@android:color/system_accent3_400"
            )
        elif xml == "res/layout-night/item_radio_notification_status_all_selected.xml":
            root[1].set(
                f"{{{xml_ns['android']}}}backgroundTint",
                "@android:color/system_neutral2_700",
            )
            root[3].set(
                f"{{{xml_ns['android']}}}backgroundTint",
                "@android:color/system_neutral2_700",
            )
        elif xml == "res/layout-night/item_radio_notification_status_release.xml":
            root[0][1].set(
                f"{{{xml_ns['android']}}}backgroundTint",
                "@android:color/system_neutral2_700",
            )
            root[1][0].set(
                f"{{{xml_ns['android']}}}backgroundTint",
                "@android:color/system_neutral2_700",
            )
        elif xml == "res/values/colors.xml":
            attributes = [
                {
                    "item": "accent_alpha_10",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "accent_alpha_70",
                    "value": "@android:color/system_neutral1_500",
                },
                {"item": "blue_alpha", "value": "@android:color/system_accent3_700"},
                {"item": "blue_primary", "value": "@android:color/system_accent1_10"},
                {
                    "item": "blue_secondary",
                    "value": "@android:color/system_accent1_300",
                },
                {
                    "item": "bottom_nav_background",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "bottom_nav_indicator_active",
                    "value": "@android:color/system_accent2_200",
                },
                {
                    "item": "bottom_nav_indicator_icon",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "bottom_nav_indicator_icon_checked",
                    "value": "@android:color/system_neutral2_900",
                },
                {
                    "item": "bottom_nav_indicator_label",
                    "value": "@android:color/system_neutral2_700",
                },
                {
                    "item": "bottom_nav_indicator_label_checked",
                    "value": "@android:color/system_neutral2_900",
                },
                {"item": "bright_sun", "value": "@android:color/system_accent2_200"},
                {
                    "item": "cardview_dark_background",
                    "value": "@android:color/system_neutral2_200",
                },
                {"item": "carmine", "value": "@android:color/system_neutral2_600"},
                {"item": "carmine_alpha_10", "value": "#15202020"},
                {
                    "item": "collection_card_header",
                    "value": "@android:color/system_neutral2_200",
                },
                {"item": "colorAccent", "value": "@android:color/system_neutral2_600"},
                {"item": "dash_red", "value": "@android:color/system_accent1_200"},
                {
                    "item": "design_dark_default_color_background",
                    "value": "@android:color/system_neutral1_900",
                },
                # {"item": "discord_color_static", "value": "@android:color/system_neutral1_500"},
                {
                    "item": "fab_background",
                    "value": "@android:color/system_neutral1_900",
                },
                {"item": "green", "value": "#ff4caf50"},
                {"item": "green_alpha", "value": "#ff6fbc5a"},
                {
                    "item": "green_light_border",
                    "value": "@android:color/system_accent2_300",
                },
                {"item": "green_regular", "value": "@android:color/system_accent2_300"},
                # {"item": "instagram_color", "value": "@android:color/system_neutral2_500"},
                {"item": "lavender", "value": "@android:color/system_accent1_100"},
                {"item": "light_grey", "value": "@android:color/system_neutral2_800"},
                {
                    "item": "light_md_blue_50",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "light_md_blue_500",
                    "value": "@android:color/system_neutral1_600",
                },
                {
                    "item": "light_md_deep_orange_50",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "light_md_deep_orange_500",
                    "value": "@android:color/system_neutral1_600",
                },
                {
                    "item": "light_md_green_50",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "light_md_green_500",
                    "value": "@android:color/system_neutral1_600",
                },
                {
                    "item": "light_md_pink_50",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "light_md_pink_500",
                    "value": "@android:color/system_neutral1_600",
                },
                {
                    "item": "light_md_purple_400",
                    "value": "@android:color/system_neutral1_600",
                },
                {
                    "item": "light_md_purple_50",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "light_md_teal_50",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "light_md_teal_500",
                    "value": "@android:color/system_neutral1_600",
                },
                {"item": "link_color", "value": "@android:color/system_accent1_700"},
                {
                    "item": "m3_ref_palette_neutral90",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "m3_ref_palette_neutral_variant30",
                    "value": "@android:color/system_neutral1_500",
                },
                {
                    "item": "m3_ref_palette_neutral_variant50",
                    "value": "@android:color/system_neutral2_400",
                },
                {
                    "item": "m3_ref_palette_neutral_variant60",
                    "value": "@android:color/system_neutral2_400",
                },
                {
                    "item": "m3_ref_palette_neutral_variant80",
                    "value": "@android:color/system_neutral2_300",
                },
                {
                    "item": "m3_ref_palette_secondary90",
                    "value": "@android:color/system_accent1_50",
                },
                {
                    "item": "material_grey_800",
                    "value": "@android:color/system_neutral2_800",
                },
                {"item": "md_grey_100", "value": "@android:color/system_neutral1_100"},
                {"item": "md_grey_200", "value": "@android:color/system_neutral1_100"},
                {"item": "md_grey_300", "value": "@android:color/system_neutral1_500"},
                {"item": "md_grey_400", "value": "@android:color/system_neutral1_300"},
                {"item": "md_grey_500", "value": "@android:color/system_neutral1_500"},
                {"item": "md_grey_600", "value": "@android:color/system_neutral2_50"},
                {"item": "md_grey_700", "value": "@android:color/system_neutral2_400"},
                {"item": "md_grey_800", "value": "@android:color/system_neutral2_200"},
                {"item": "md_grey_900", "value": "@android:color/system_neutral1_800"},
                {"item": "md_white_1000", "value": "@android:color/system_neutral1_10"},
                {
                    "item": "notification_episode_color",
                    "value": "@android:color/system_accent3_500",
                },
                {
                    "item": "notification_material_background_media_default_color",
                    "value": "@android:color/system_neutral2_200",
                },
                {
                    "item": "red_light_border",
                    "value": "@android:color/system_accent1_500",
                },
                {"item": "red_regular", "value": "@android:color/system_accent1_500"},
                {
                    "item": "refresh_progress",
                    "value": "@android:color/system_accent1_200",
                },
                {
                    "item": "screen_background",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "search_bar_alt",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "separator_alpha_3",
                    "value": "@android:color/system_neutral1_100",
                },
                {"item": "shortcake", "value": "@android:color/system_neutral1_700"},
                {
                    "item": "switch_on_primary",
                    "value": "@android:color/system_accent1_10",
                },
                {
                    "item": "switch_on_surface_variant",
                    "value": "@android:color/system_neutral2_400",
                },
                {
                    "item": "switch_outline",
                    "value": "@android:color/system_neutral2_400",
                },
                {
                    "item": "switch_primary_container",
                    "value": "@android:color/system_accent2_100",
                },
                {
                    "item": "switch_surface",
                    "value": "@android:color/system_neutral1_10",
                },
                {
                    "item": "switch_track_checked",
                    "value": "@android:color/system_accent1_700",
                },
                # {
                #     "item": "tg_background_color",
                #     "value": "@android:color/system_neutral1_100",
                # },
                # {"item": "tg_color", "value": "@android:color/system_neutral2_600"},
                # {
                #     "item": "tg_color_static",
                #     "value": "@android:color/system_neutral2_500",
                # },
                # {"item": "tiktok_color", "value": "@android:color/system_neutral2_500"},
                {
                    "item": "tooltip_background",
                    "value": "@android:color/system_neutral1_700",
                },
                {
                    "item": "tooltip_background_dark",
                    "value": "@android:color/system_neutral1_800",
                },
                {
                    "item": "tooltip_background_light",
                    "value": "@android:color/system_neutral1_100",
                },
                # {
                #     "item": "vk_background_color",
                #     "value": "@android:color/system_neutral1_100",
                # },
                # {"item": "vk_color", "value": "@android:color/system_neutral2_600"},
                # {
                #     "item": "vk_color_static",
                #     "value": "@android:color/system_neutral1_500",
                # },
                {
                    "item": "yellow_primary",
                    "value": "@android:color/system_neutral2_600",
                },
                {
                    "item": "yellow_secondary",
                    "value": "@android:color/system_neutral2_100",
                },
            ]
            with tqdm(
                total=len(attributes), desc="res/values/colors.xml", unit_divisor=1
            ) as bar:
                for attr in attributes:
                    elem = root.find(f".//*[@name='{attr["item"]}']")
                    elem.text = attr["value"]
                    bar.update()
        elif xml == "res/values/styles.xml":
            for tag in root:
                if tag.get("name") == "AnixButton.Bottom":
                    tag.find(".//*[@name='android:textColor']").text = (
                        "@android:color/system_neutral2_800"
                    )
                    tag.find(".//*[@name='android:backgroundTint']").text = (
                        "@android:color/system_neutral2_200"
                    )
                elif tag.get("name") == "AnixButton.Unelevated":
                    tag.find(".//*[@name='android:textColor']").text = (
                        "@android:color/system_neutral2_50"
                    )
                    tag.find(".//*[@name='android:backgroundTint']").text = (
                        "@android:color/system_accent1_700"
                    )
                elif tag.get("name") == "AnixButton.Unelevated.Red":
                    tag.find(".//*[@name='android:textColor']").text = (
                        "@android:color/system_accent3_10"
                    )
                    tag.find(".//*[@name='android:backgroundTint']").text = (
                        "@android:color/system_neutral2_700"
                    )
                elif tag.get("name") == "AnixButton.Unelevated.Yellow.Small":
                    tag.find(".//*[@name='android:textColor']").text = (
                        "@android:color/system_neutral2_50"
                    )
                    tag.find(".//*[@name='android:backgroundTint']").text = (
                        "@android:color/system_neutral2_700"
                    )
                elif tag.get("name") == "BaseTheme":
                    tag.find(".//*[@name='android:colorBackground']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(".//*[@name='android:navigationBarColor']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(".//*[@name='backgroundColorSecondary']").text = (
                        "@android:color/system_neutral1_100"
                    )
                    tag.find(".//*[@name='backgroundColorTertiary']").text = (
                        "@android:color/system_neutral1_100"
                    )
                    tag.find(".//*[@name='colorOnBackground']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(".//*[@name='colorPrimaryDark']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(".//*[@name='colorSurface']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(".//*[@name='iconSecondaryTintColor']").text = (
                        "@android:color/system_neutral1_500"
                    )
                    tag.find(".//*[@name='iconTintColor']").text = (
                        "@android:color/system_neutral2_600"
                    )
                    tag.find(".//*[@name='primaryTextColor']").text = (
                        "@android:color/system_neutral1_900"
                    )
                    tag.find(".//*[@name='progressBackTint']").text = (
                        "@android:color/system_neutral1_100"
                    )
                    tag.find(".//*[@name='secondaryTextColor']").text = (
                        "@android:color/system_neutral1_500"
                    )
                    tag.find(".//*[@name='tertiaryTextColor']").text = (
                        "@android:color/system_neutral2_500"
                    )
        elif xml == "res/values-night/colors.xml":
            attributes = [
                {
                    "item": "accent_alpha_10",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "accent_alpha_70",
                    "value": "@android:color/system_accent2_50",
                },
                {"item": "blue_alpha", "value": "@android:color/system_accent3_300"},
                {"item": "blue_primary", "value": "@android:color/system_accent2_10"},
                {
                    "item": "blue_secondary",
                    "value": "@android:color/system_neutral2_700",
                },
                {
                    "item": "bottom_nav_background",
                    "value": "@android:color/system_neutral1_900",
                },
                {
                    "item": "bottom_nav_indicator_active",
                    "value": "@android:color/system_neutral2_700",
                },
                {
                    "item": "bottom_nav_indicator_icon",
                    "value": "@android:color/system_neutral2_200",
                },
                {
                    "item": "bottom_nav_indicator_icon_checked",
                    "value": "@android:color/system_neutral2_50",
                },
                {
                    "item": "bottom_nav_indicator_label",
                    "value": "@android:color/system_neutral1_200",
                },
                {
                    "item": "bottom_nav_indicator_label_checked",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "collection_card_header",
                    "value": "@android:color/system_neutral2_700",
                },
                {"item": "colorAccent", "value": "@android:color/system_accent2_50"},
                {"item": "colorPrimary", "value": "@android:color/system_neutral1_50"},
                {"item": "dash_green", "value": "@android:color/system_neutral2_200"},
                # {
                #     "item": "discord_color_static",
                #     "value": "@android:color/system_neutral2_200",
                # },
                {
                    "item": "fab_background",
                    "value": "@android:color/system_accent1_700",
                },
                {
                    "item": "green_light_border",
                    "value": "@android:color/system_accent2_300",
                },
                {
                    "item": "icon_orange_icon",
                    "value": "@android:color/system_accent3_400",
                },
                # {
                #     "item": "instagram_color",
                #     "value": "@android:color/system_neutral2_200",
                # },
                {"item": "light_grey", "value": "@android:color/system_neutral2_200"},
                {
                    "item": "light_md_blue_50",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "light_md_blue_500",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "light_md_deep_orange_50",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "light_md_deep_orange_500",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "light_md_green_50",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "light_md_green_500",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "light_md_pink_50",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "light_md_pink_500",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "light_md_purple_400",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "light_md_purple_50",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "light_md_teal_50",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "light_md_teal_500",
                    "value": "@android:color/system_neutral1_50",
                },
                {"item": "link_color", "value": "@android:color/system_accent1_300"},
                {
                    "item": "refresh_background",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "refresh_progress",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "screen_background",
                    "value": "@android:color/system_neutral1_900",
                },
                {
                    "item": "search_bar_alt",
                    "value": "@android:color/system_neutral1_900",
                },
                {
                    "item": "separator_alpha_3",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "switch_on_primary",
                    "value": "@android:color/system_accent2_700",
                },
                {
                    "item": "switch_on_surface_variant",
                    "value": "@android:color/system_neutral2_400",
                },
                {
                    "item": "switch_primary_container",
                    "value": "@android:color/system_accent2_700",
                },
                {
                    "item": "switch_surface",
                    "value": "@android:color/system_neutral2_700",
                },
                # {
                #     "item": "tg_background_color",
                #     "value": "@android:color/system_neutral2_800",
                # },
                # {"item": "tg_color", "value": "@android:color/system_neutral2_200"},
                # {
                #     "item": "tg_color_static",
                #     "value": "@android:color/system_neutral2_200",
                # },
                # {"item": "tiktok_color", "value": "@android:color/system_neutral2_200"},
                {
                    "item": "tooltip_background",
                    "value": "@android:color/system_neutral2_700",
                },
                {
                    "item": "torlook_background",
                    "value": "@android:color/system_neutral2_800",
                },
                # {
                #     "item": "vk_background_color",
                #     "value": "@android:color/system_neutral2_800",
                # },
                # {"item": "vk_color", "value": "@android:color/system_neutral2_200"},
                # {
                #     "item": "vk_color_static",
                #     "value": "@android:color/system_neutral2_200",
                # },
                {
                    "item": "yellow_primary",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "yellow_secondary",
                    "value": "@android:color/system_neutral1_800",
                },
            ]
            with tqdm(
                total=len(attributes),
                desc="res/values-night/colors.xml",
                unit_divisor=1,
            ) as bar:
                for attr in attributes:
                    elem = root.find(f".//*[@name='{attr["item"]}']")
                    elem.text = attr["value"]
                    bar.update()
            md_gray_800 = etree.Element("color", name="md_gray_800")
            md_gray_800.text = "@android:color/system_neutral2_300"
            root.append(md_gray_800)
        elif xml == "res/values-night/styles.xml":
            for tag in root:
                if tag.get("name") == "AnixButton.Bottom":
                    tag.find(".//*[@name='android:textColor']").text = (
                        "@android:color/system_neutral1_200"
                    )
                    tag.find(".//*[@name='android:backgroundTint']").text = (
                        "@android:color/system_neutral2_700"
                    )
                elif tag.get("name") == "AnixButton.Unelevated":
                    tag.find(".//*[@name='android:backgroundTint']").text = (
                        "@android:color/system_neutral1_100"
                    )
                elif tag.get("name") == "AnixButton.Unelevated.Small":
                    tag.find(".//*[@name='android:backgroundTint']").text = (
                        "@android:color/system_neutral1_100"
                    )
        elif xml == "res/values-v31/styles.xml":
            for tag in root:
                if tag.get("name") == "AppTheme":
                    tag.find(".//*[@name='android:navigationBarColor']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(
                        ".//*[@name='android:windowSplashScreenBackground']"
                    ).text = "@android:color/system_neutral1_50"
                elif tag.get("name") == "AppTheme.Start":
                    tag.find(".//*[@name='android:navigationBarColor']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(
                        ".//*[@name='android:windowSplashScreenBackground']"
                    ).text = "@android:color/system_neutral1_50"
                    tag.find(".//*[@name='colorOnBackground']").text = (
                        "@android:color/system_neutral1_50"
                    )
                    tag.find(".//*[@name='primaryTextColor']").text = (
                        "@android:color/system_neutral1_900"
                    )
                    tag.find(".//*[@name='secondaryTextColor']").text = (
                        "@android:color/system_neutral1_500"
                    )
                    tag.find(".//*[@name='tertiaryTextColor']").text = (
                        "@android:color/system_neutral2_500"
                    )
        elif xml == "res/values-night-v29/styles.xml":
            AppThemeAuth = [
                {
                    "item": "backgroundColorSecondary",
                    "value": "@android:color/system_neutral1_900",
                },
                {"item": "colorAccent", "value": "@android:color/system_neutral1_50"},
                {"item": "colorPrimary", "value": "@android:color/system_accent1_100"},
                {
                    "item": "primaryTextColor",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "secondaryTextColor",
                    "value": "@android:color/system_neutral2_200",
                },
                {
                    "item": "tertiaryTextColor",
                    "value": "@android:color/system_neutral1_200",
                },
            ]
            BaseTheme = [
                {
                    "item": "android:colorBackground",
                    "value": "@android:color/system_neutral1_900",
                },
                {
                    "item": "android:statusBarColor",
                    "value": "@android:color/system_neutral1_900",
                },
                {
                    "item": "android:navigationBarColor",
                    "value": "@android:color/system_neutral1_900",
                },
                {
                    "item": "backgroundColorSecondary",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "backgroundColorTertiary",
                    "value": "@android:color/system_neutral2_800",
                },
                {"item": "colorAccent", "value": "@android:color/system_accent1_10"},
                {
                    "item": "colorOnBackground",
                    "value": "@android:color/system_neutral1_900",
                },
                {"item": "colorPrimary", "value": "@android:color/system_accent1_100"},
                {"item": "colorSurface", "value": "@android:color/system_neutral1_900"},
                {
                    "item": "deleteButtonColor",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "editButtonColor",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "iconAltTintColor",
                    "value": "@android:color/system_neutral1_100",
                },
                {
                    "item": "iconLightDarkColor",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "iconSecondaryTintColor",
                    "value": "@android:color/system_neutral2_600",
                },
                {"item": "iconTintColor", "value": "@android:color/system_accent1_50"},
                {
                    "item": "invertBlackWhiteColor",
                    "value": "@android:color/system_accent2_10",
                },
                {"item": "invertColor", "value": "@android:color/system_neutral2_800"},
                {"item": "placeholderEnd", "value": "@android:color/system_accent2_10"},
                {
                    "item": "placeholderStart",
                    "value": "@android:color/system_neutral1_800",
                },
                {
                    "item": "primaryTextColor",
                    "value": "@android:color/system_neutral1_50",
                },
                {
                    "item": "progressBackTint",
                    "value": "@android:color/system_neutral1_800",
                },
                {"item": "progressTint", "value": "@android:color/system_neutral1_50"},
                {
                    "item": "secondaryButtonColor",
                    "value": "@android:color/system_neutral2_800",
                },
                {
                    "item": "secondaryTextColor",
                    "value": "@android:color/system_neutral2_200",
                },
                {
                    "item": "tertiaryTextColor",
                    "value": "@android:color/system_neutral1_200",
                },
            ]
            for child in root:
                if child.get("name") == "AppTheme.Auth":
                    for item in AppThemeAuth:
                        child.find(f".//*[@name='{item["item"]}']").text = item["value"]
                if child.get("name") == "BaseTheme":
                    for item in BaseTheme:
                        child.find(f".//*[@name='{item["item"]}']").text = item["value"]
        elif xml == "res/values-night-v31/styles.xml":
            with open(f"{config['src']}/{xml}", "w", encoding="utf-8") as file:
                file.write(
                    """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="@style/Theme.Material3.DayNight.NoActionBar">
        <item name="android:colorBackground">@color/m3_sys_color_dynamic_dark_background</item>
        <item name="android:textColorSecondary">@color/m3_sys_color_dynamic_dark_on_surface_variant</item>
        <item name="android:statusBarColor">@color/m3_sys_color_dynamic_dark_background</item>
        <item name="android:navigationBarColor">@color/m3_sys_color_dynamic_dark_surface</item>
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowSplashScreenBackground">@color/m3_sys_color_dynamic_dark_background</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/logo_splash_anim</item>
        <item name="android:windowSplashScreenAnimationDuration">1000</item>
        <item name="actionBarSize">56.0dip</item>
        <item name="addFavButtonColor">@color/m3_sys_color_dynamic_dark_surface</item>
        <item name="addFavButtonTextColor">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="alertDialogTheme">@style/DialogTheme</item>
        <item name="backgroundAdItem">@color/white_alpha_5</item>
        <item name="backgroundColorSecondary">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="backgroundColorTertiary">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="bottomSheetDialogTheme">@style/AppBottomSheetDialogTheme</item>
        <item name="colorAccent">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="colorOnBackground">@color/m3_sys_color_dynamic_dark_background</item>
        <item name="colorPrimary">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="colorPrimaryDark">@android:color/transparent</item>
        <item name="colorSurface">@color/m3_sys_color_dynamic_dark_background</item>
        <item name="deleteButtonColor">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="deleteButtonTextColor">@color/md_grey_300</item>
        <item name="dialogBackgroundAccent">@color/accent_alpha_20</item>
        <item name="dialogPreferenceStyle">@style/CustomDialogPreferenceStyle</item>
        <item name="editButtonColor">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="editButtonTextColor">@color/md_grey_300</item>
        <item name="iconAccentTintColor">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="iconAltTintColor">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="iconLightDarkColor">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="iconSecondaryTintColor">@android:color/system_neutral2_600</item>
        <item name="iconTintColor">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="invertColor">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="placeholderStart">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="popupMenuBackground">@drawable/custom_m3_popupmenu_background_overlay</item>
        <item name="preferenceCategoryTitleTextColor">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="preferenceStyle">@style/CustomPreferenceStyle</item>
        <item name="primaryTextColor">@android:color/white</item>
        <item name="progressBackTint">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="progressTint">@color/m3_sys_color_dynamic_dark_primary</item>
        <item name="secondaryButtonColor">@color/m3_sys_color_dynamic_dark_inverse_on_surface</item>
        <item name="secondaryButtonTextColor">@color/md_grey_300</item>
        <item name="secondaryTextColor">@color/m3_sys_color_dynamic_dark_on_surface_variant</item>
        <item name="sectionBadgeColor">@color/md_grey_900</item>
        <item name="separatorColor">#1affffff</item>
        <item name="switchPreferenceStyle">@style/CustomSwitchPreferenceStyle</item>
        <item name="tertiaryTextColor">@color/m3_sys_color_dynamic_dark_on_surface_variant</item>
        <item name="warningTextColor">#ff745c21</item>
    </style>
    <style name="AppTheme.Start" parent="@style/AppTheme">
        <item name="android:forceDarkAllowed">false</item>
        <item name="android:windowSplashScreenBackground">@color/m3_sys_color_dynamic_dark_background</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/logo_splash_anim</item>
        <item name="android:windowSplashScreenAnimationDuration">1000</item>
    </style>
    <style name="BottomNavigationView" parent="@style/Widget.Material3.BottomNavigationView">
        <item name="android:background">@color/m3_sys_color_dynamic_dark_surface</item>
        <item name="itemActiveIndicatorStyle">@style/BottomNavigationView.ActiveIndicator</item>
        <item name="itemIconTint">@color/m3_sys_color_dynamic_dark_on_secondary_container</item>
        <item name="itemTextColor">@color/m3_sys_color_dynamic_dark_on_surface</item>
    </style>
    <style name="BottomNavigationView.ActiveIndicator" parent="@style/Widget.Material3.BottomNavigationView.ActiveIndicator">
        <item name="android:color">@color/m3_sys_color_dynamic_dark_secondary_container</item>
    </style>
</resources>"""
                )

        if xml != "res/values-night-v31/styles.xml":
            tree.write(
                f"{config['src']}/{xml}",
                pretty_print=True,
                xml_declaration=True,
                encoding="utf-8",
            )
        tqdm.write(f"changed color values: {config['src']}/{xml}")

    return True


if __name__ == "__main__":
    apply({"src": "./decompiled"})
