import requests
import os
from tqdm import tqdm
from config import config, log


def check_if_tool_exists(tool: str) -> bool:
    if not os.path.exists(config["folders"]["tools"]):
        log.info(f"creating `tools` folder: {config['folders']['tools']}")
        os.mkdir(config["folders"]["tools"])

    if not os.path.exists(f"{config['folders']['tools']}/{tool}"):
        return False
    elif os.path.exists(f"{config['folders']['tools']}/{tool}") and os.path.isdir(
        f"{config['folders']['tools']}/{tool}"
    ):
        log.warning(f"`{config['folders']['tools']}/{tool}` is a folder")
        return True
    else:
        return True


def download_tool(url: str, tool: str):
    if not check_if_tool_exists(tool):
        log.info(f"downloading a tool: `{tool}`")
        try:
            response = requests.get(url, stream=True)
            total = int(response.headers.get("content-length", 0))
            with open(f"{config['folders']['tools']}/{tool}", "wb") as file, tqdm(
                desc=tool,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for bytes in response.iter_content(chunk_size=8192):
                    size = file.write(bytes)
                    bar.update(size)
            log.info(f"`{tool}` downloaded")
        except Exception as e:
            log.error(f"error while downloading `{tool}`: {e}")


def check_and_download_all_tools():
    for tool in config["tools"]:
        download_tool(tool["url"], tool["tool"])
