import os, json
import importlib
from typing import TypedDict
from beaupy import select_multiple
from tqdm import tqdm
from config import config, log, console


class Patch:
    def __init__(self, name, pkg):
        self.name = name
        self.package = pkg
        self.applied = False
        try:
            self.priority = pkg.priority
        except AttributeError:
            self.priority = 0

    def apply(self, conf: dict) -> bool:
        try:
            self.applied = self.package.apply(conf)
            return True
        except Exception as e:
            log.error(
                f"error while applying a patch {self.name}: %s, with args: %s",
                e,
                e.args,
                exc_info=True,
            )
            return False


def get_patches() -> list[str]:
    patches = []
    if not os.path.exists(config["folders"]["patches"]):
        log.info(f"creating `patches` folder: {config['folders']['patches']}")
        os.mkdir(config["folders"]["patches"])
        return patches

    for file in os.listdir(config["folders"]["patches"]):
        if (
            file.endswith(".py")
            and os.path.isfile(f"{config['folders']['patches']}/{file}")
            and file != "__init__.py"
        ):
            patches.append(file[:-3])

    return patches


def select_patches(patches: list[str]) -> list[str]:
    console.print("select patches to apply")
    applied = select_multiple(patches, tick_character="X")
    return applied


class PatchStatus(TypedDict):
    name: str
    status: bool


def apply_patches(patches: list[str]) -> list[PatchStatus]:
    modules = []
    statuses = []

    for name in patches:
        module = importlib.import_module(
            f"{config['folders']['patches'].removeprefix("./")}.{name}"
        )
        modules.append(Patch(name, module))
    modules.sort(key=lambda x: x.package.priority, reverse=True)

    for patch in tqdm(modules, colour="green", desc="patching apk"):
        tqdm.write(f"patch apply: {patch.name}")
        conf = {}
        if os.path.exists(f"{config['folders']['patches']}/{patch.name}.config.json"):
            with open(
                f"{config['folders']['patches']}/{patch.name}.config.json",
                "r",
                encoding="utf-8",
            ) as conf:
                conf = json.loads(conf.read())
        conf["src"] = config["folders"]["decompiled"]
        status = patch.apply(conf)
        statuses.append({"name": patch.name, "status": status})

    return statuses
