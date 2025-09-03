from scripts.download_tools import check_and_download_all_tools
from scripts.select_apk import get_apks, select_apk
from scripts.select_patches import apply_patches, get_patches, select_patches
from scripts.utils import check_java_version, compile_apk, decompile_apk, sign_apk, init_patch
from config import args, config, log, console

from time import time
import math
import yaml


def patch():
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
    return patches, statuses_ok, statuses_err


if __name__ == "__main__":
    check_and_download_all_tools()
    check_java_version()

    if args.init:
        init_patch()
        exit(0)

    if not args.patch and not args.sign:
        apks = get_apks()
        if not apks:
            log.fatal(f"apks folder is empty")
            exit(1)
        apk = select_apk(apks)
        if not apk:
            log.info("cancelled")
            exit(0)
    elif args.patch:
        patch()
        exit(0)
    elif args.sign:
        apkFileName = None
        with open(
            f"{config["folders"]["decompiled"]}/apktool.yml", "r", encoding="utf-8"
        ) as f:
            data = yaml.load(f.read(), Loader=yaml.Loader)
            apkFileName = data.get("apkFileName", None)
        if not apkFileName:
            log.fatal(
                f"can't find apk file name in {config['folders']['decompiled']}/apktool.yml"
            )
            exit(1)
        sign_apk(f"{apkFileName.removesuffix('.apk')}-patched.apk")
        exit(0)

    start_time = time()
    if not args.no_decompile:
        decompile_apk(apk)
    patches, statuses_ok, statuses_err = patch()
    if not args.no_compile:
        compile_apk(f"{apk.removesuffix(".apk")}-patched.apk")
    end_time = time()
    if not args.no_compile:
        sign_apk(f"{apk.removesuffix(".apk")}-patched.apk")

    log.info("Finished")
    log.info(
        f"install this apk file: `{config["folders"]["dist"]}/{apk.removesuffix(".apk")}-patched-aligned-signed.apk`"
    )
    log.info(f"used and successful patches: {", ".join(statuses_ok)}")
    log.info(f"used and unsuccessful patches: {", ".join(statuses_err)}")
    log.info(f"time taken: {math.floor(end_time - start_time)}s")
