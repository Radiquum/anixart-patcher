import os
import shutil
import subprocess
from config import log, config


def check_java_version():
    try:
        result = subprocess.run(
            ["java", "-version"], capture_output=True, text=True, check=True
        )
        version_line = result.stderr.splitlines()[0]
        if not any(f"{i}." in version_line for i in range(9, 100)):
            log.error(f"java 8+ is not installed")
            exit(1)
    except subprocess.CalledProcessError:
        log.error(f"java 8+ is not found")
        exit(1)
    log.info(f"found java: {version_line}")


def decompile_apk(apk: str):
    if not os.path.exists(config["folders"]["decompiled"]):
        log.info(f"creating `decompiled` folder: {config['folders']['decompiled']}")
        os.mkdir(config["folders"]["decompiled"])
    else:
        log.info(f"resetting `decompiled` folder: {config['folders']['decompiled']}")
        shutil.rmtree(config["folders"]["decompiled"])
        os.mkdir(config["folders"]["decompiled"])

    log.info(f"decompile apk: `{apk}`")
    try:
        result = subprocess.run(
            f"java -jar {config['folders']['tools']}/apktool.jar d -f -o {config['folders']['decompiled']} {config['folders']['apks']}/{apk}",
            shell=True,
            check=True,
            text=True,
            # stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        log.fatal(
            f"error of running a command: %s :: %s",
            f"java -jar {config['folders']['tools']}/apktool.jar d -f -o {config['folders']['decompiled']} {config['folders']['apks']}/{apk}",
            e.stderr,
            exc_info=True,
        )
        exit(1)


def compile_apk(apk: str):
    if not os.path.exists(config["folders"]["dist"]):
        log.info(f"creating `dist` folder: {config['folders']['dist']}")
        os.mkdir(config["folders"]["dist"])
    else:
        log.info(f"resetting `dist` folder: {config['folders']['dist']}")
        shutil.rmtree(config["folders"]["dist"])
        os.mkdir(config["folders"]["dist"])

    log.info(f"compile apk: `{apk}`")
    try:
        result = subprocess.run(
            f"java -jar {config['folders']['tools']}/apktool.jar b -f -o {config['folders']['dist']}/{apk} {config['folders']['decompiled']}",
            shell=True,
            check=True,
            text=True,
            # stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        log.fatal(
            f"error of running a command: %s :: %s",
            f"java -jar {config['folders']['tools']}/apktool.jar b -f -o {config['folders']['dist']}/{apk} {config['folders']['decompiled']}",
            e.stderr,
            exc_info=True,
        )
        exit(1)


def sign_apk(apk: str):
    log.info(f"sign and align apk: `{apk}`")

    if os.path.exists(f"{config['folders']['dist']}/{apk.removesuffix('.apk')}-aligned.apk"):
        os.remove(f"{config['folders']['dist']}/{apk.removesuffix('.apk')}-aligned.apk")
    if os.path.exists(f"{config['folders']['dist']}/{apk.removesuffix('.apk')}-aligned-signed.apk"):
        os.remove(f"{config['folders']['dist']}/{apk.removesuffix('.apk')}-aligned-signed.apk")

    command = ""
    try:
        command = (
            f"zipalign -p 4 {config['folders']['dist']}/{apk} {config['folders']['dist']}/{apk.removesuffix(".apk")}-aligned.apk",
        )
        result = subprocess.run(
            f"zipalign -p 4 {config['folders']['dist']}/{apk} {config['folders']['dist']}/{apk.removesuffix(".apk")}-aligned.apk",
            shell=True,
            check=True,
            text=True,
            # stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        command = (
            f"apksigner sign --ks ./keystore.jks --out {config['folders']['dist']}/{apk.removesuffix(".apk")}-aligned-signed.apk {config['folders']['dist']}/{apk.removesuffix(".apk")}-aligned.apk",
        )
        result = subprocess.run(
            f"apksigner sign --ks ./keystore.jks --out {config['folders']['dist']}/{apk.removesuffix(".apk")}-aligned-signed.apk {config['folders']['dist']}/{apk.removesuffix(".apk")}-aligned.apk",
            shell=True,
            check=True,
            text=True,
            # stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        log.fatal(f"error of running a command: %s :: %s", command, e.stderr, exc_info=True)
        exit(1)
