import json
import logging
import os
from typing import TypedDict
from rich.logging import RichHandler
from rich.console import Console


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("rich")
console = Console()


class ConfigTools(TypedDict):
    tool: str
    url: str


class ConfigFolders(TypedDict):
    tools: str
    apks: str
    decompiled: str
    patches: str
    dist: str


class Config(TypedDict):
    tools: list[ConfigTools]
    folders: ConfigFolders


def load_config() -> Config:
    if not os.path.exists("config.json"):
        log.exception("file `config.json` is not found!")
        exit(1)

    with open("./config.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())


config = load_config()
