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


class ConfigXmlNS(TypedDict):
    android: str
    app: str


class Config(TypedDict):
    log_level: str
    tools: list[ConfigTools]
    folders: ConfigFolders
    xml_ns: ConfigXmlNS


def load_config() -> Config:
    config = None

    if not os.path.exists("config.json"):
        log.exception("file `config.json` is not found!")
        exit(1)

    with open("./config.json", "r", encoding="utf-8") as file:
        config = json.loads(file.read())

    log.setLevel(config.get("log_level", "NOTSET").upper())

    return config


config = load_config()
