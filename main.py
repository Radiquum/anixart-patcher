from scripts.download_tools import check_and_download_all_tools
from scripts.select_apk import get_apks, select_apk
from scripts.select_patches import apply_patches, get_patches, select_patches
from scripts.utils import check_java_version, decompile_apk
from config import log, console


if __name__ == "__main__":
    check_and_download_all_tools()
    check_java_version()

    apks = get_apks()
    if not apks:
        log.fatal(f"apks folder is empty")
        exit(1)

    apk = select_apk(apks)
    decompile_apk(apk)
    
    patches = get_patches()
    patches = select_patches(patches)
    
    statuses = apply_patches(patches)

    for status in statuses:
        if status["status"]:
            console.print(f"{status['name']}: ✔", style="bold green")
        else:
            console.print(f"{status['name']}: ✘", style="bold red")
