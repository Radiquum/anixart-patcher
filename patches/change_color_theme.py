"""Change app color theme"""

priority = -99

import os
from typing import TypedDict
from beaupy import select
from tqdm import tqdm
from lxml import etree

class PatchConfig_ChangeColorTheme(TypedDict):
    src: str
    themes: str

def apply(config: PatchConfig_ChangeColorTheme) -> bool:
    print("select color theme to apply")

    theme = select(config["themes"], cursor="->", cursor_style="cyan")
    theme_attr = config[theme]['attributes']
    theme_text  = config[theme]['text']
    theme_files  = config[theme]['files']
    
    with tqdm(
        total=len(theme_attr),
        unit="attr",
        unit_divisor=1,
        desc="color attributes"
    ) as bar:
        for attr in theme_attr:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(f"{config['src']}/{attr['file_path']}", parser)
            root = tree.getroot()
            root.find(attr['tag_path']).set(attr['attr_name'], attr['attr_value']['to'])
            tree.write(
                f"{config['src']}/{attr['file_path']}",
                pretty_print=True,
                xml_declaration=True,
                encoding="utf-8",
            )
            bar.update()

    with tqdm(
        total=len(theme_text),
        unit="attr",
        unit_divisor=1,
        desc="color values"
    ) as bar:
        for text in theme_text:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(f"{config['src']}/{text['file_path']}", parser)
            root = tree.getroot()
            root.find(text['tag_path']).text = text['text']['to']
            tree.write(
                f"{config['src']}/{text['file_path']}",
                pretty_print=True,
                xml_declaration=True,
                encoding="utf-8",
            )
            bar.update()
    
    if len(theme_files) > 0:
        with tqdm(
            total=len(theme_files),
            unit="files",
            unit_divisor=1,
            desc="color files"
        ) as bar:
            for file in theme_files:
                with open(f"{config['src']}/{file['file_path']}", "w", encoding="utf-8") as f:
                    f.write("\n".join(file['file_content']))
                bar.update()
    
    return True