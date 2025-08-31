import os
from beaupy import select
from config import config, log, console

def get_apks() -> list[str]:
    apks = []
    if not os.path.exists(config["folders"]["apks"]):
        log.info(f"creating `apks` folder: {config['folders']['apks']}")
        os.mkdir(config["folders"]["apks"])
        return apks
    
    for file in os.listdir(config["folders"]["apks"]):
        if file.endswith(".apk") and os.path.isfile(f"{config['folders']['apks']}/{file}"):
            apks.append(file)

    return apks

def select_apk(apks: list[str]) -> str: 
    console.print("select apk file to patch")
    apks.append("cancel")
    
    apk = select(apks, cursor="->", cursor_style="cyan")
    if apk == "cancel":
        log.info("patching cancelled")
        exit(0)

    return apk