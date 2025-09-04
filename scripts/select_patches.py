import os, json
import importlib
from typing import TypedDict

from beaupy import select_multiple
from rich.progress import BarColumn, Progress, TextColumn

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


progress = Progress(
    "[progress.description]{task.description}",
    TextColumn(text_format="{task.fields[patch]}"),
    BarColumn(bar_width=None),
    "[blue]{task.completed}/{task.total}",
)


def get_patch_config(
    patch_name: str,
    all_patch_statuses: list,
    app_version: str,
    app_build: int,
) -> dict:
    _config = {}
    if os.path.exists(f"{config['folders']['patches']}/{patch_name}.config.json"):
        with open(
            f"{config['folders']['patches']}/{patch_name}.config.json",
            "r",
            encoding="utf-8",
        ) as f:
            _config = json.loads(f.read())
    _config["_internal_all_patch_statuses"] = all_patch_statuses
    _config["_internal_app_version"] = app_version
    _config["_internal_app_build"] = app_build
    return _config


def apply_patches(
    patches: list[str], app_version: str, app_build: int
) -> list[PatchStatus]:
    modules = []
    statuses = []

    for name in patches:
        module = importlib.import_module(
            f"{config['folders']['patches'].removeprefix("./")}.{name}"
        )
        modules.append(Patch(name, module))
    modules.sort(key=lambda x: x.package.priority, reverse=True)

    with progress:
        task = progress.add_task("applying patch:", total=len(modules), patch="")
        for module in modules:
            progress.update(task, patch=module.name)
            status = module.apply(get_patch_config(module.name, statuses, app_version, app_build))
            statuses.append({"name": module.name, "status": status})
            progress.update(task, advance=1)

        progress.update(task, description="patches applied", patch="")

    return statuses
