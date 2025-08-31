from scripts.download_tools import check_and_download_all_tools
from scripts.select_apk import get_apks, select_apk
from scripts.select_patches import apply_patches, get_patches, select_patches
from scripts.utils import check_java_version, compile_apk, decompile_apk, sign_apk
from config import log, console

from time import time
import math

import argparse
parser = argparse.ArgumentParser(prog='anixart patcher')
parser.add_argument("--no-decompile", action='store_true')
parser.add_argument("--no-compile", action='store_true')

if __name__ == "__main__":
    args = parser.parse_args()
    
    check_and_download_all_tools()
    check_java_version()

    apks = get_apks()
    if not apks:
        log.fatal(f"apks folder is empty")
        exit(1)
    apk = select_apk(apks)
    if not apk:
        log.info('cancelled')
        exit(0)

    start_time = time()

    if not args.no_decompile:
        decompile_apk(apk)

    patches = get_patches()
    patches = select_patches(patches)
    statuses = apply_patches(patches)
    statuses_ok = []
    statuses_err = []

    for status in statuses:
        if status["status"]:
            console.print(f"{status['name']}: ✔", style="bold green")
            statuses_ok.append(status["name"])
        else:
            console.print(f"{status['name']}: ✘", style="bold red")
            statuses_err.append(status["name"])

    if not args.no_compile:
        compile_apk(f"{apk.removesuffix(".apk")}-patched.apk")
        sign_apk(f"{apk.removesuffix(".apk")}-patched.apk")

    end_time = time()

    log.info("Finished")
    log.info(f"install this apk file: {apk.removesuffix(".apk")}-patched-aligned-signed.apk")
    log.info(f"used and successful patches: {", ".join(statuses_ok)}")
    log.info(f"used and unsuccessful patches: {", ".join(statuses_err)}")
    log.info(f"time taken: {math.floor(end_time - start_time)}s")
