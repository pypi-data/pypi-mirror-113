import argparse
import logging
import os
import time
from configparser import ConfigParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List
from urllib.parse import quote_plus, unquote_plus

import multivolumefile
import py7zr

from . import __app_name__, __version__
from .client import ToDusClient

formatter = logging.Formatter("%(levelname)s-%(name)s-%(asctime)s-%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler_default = logging.StreamHandler()
handler_default.setFormatter(formatter)
handler_error = logging.FileHandler("logs", encoding="utf-8")
handler_error.setLevel(logging.ERROR)
handler_error.setFormatter(formatter)
logger.addHandler(handler_default)
logger.addHandler(handler_error)

client = ToDusClient()
config = ConfigParser()
MAX_RETRY = 3
DOWN_TIMEOUT = 60 * 20  # 20 MINS


def write_txt(filename: str, urls: List[str], parts: List[str]) -> str:
    txt = "\n".join(f"{down_url}\t{name}" for down_url, name in zip(urls, parts))
    path = Path(f"{filename}.txt").resolve()
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    return str(path)


def split_upload(
    token: str, path: str, part_size: int, max_retry: int = MAX_RETRY
) -> str:
    global client

    with open(path, "rb") as file:
        data = file.read()

    filename = Path(path).name

    logger.info("Compressing parts...")

    with TemporaryDirectory() as tempdir:
        with multivolumefile.open(
            Path(f"{tempdir}/{filename}.7z"),
            "wb",
            volume=part_size,
        ) as vol:
            with py7zr.SevenZipFile(vol, "w") as archive:  # type: ignore
                archive.writestr(data, filename)
        del data
        parts = sorted(_file.name for _file in Path(tempdir).iterdir())
        parts_count = len(parts)

        urls = []

        for i, name in enumerate(parts, 1):
            retry = 0
            up_done = False
            logger.info(f"Uploading {i}/{parts_count}: {name}")

            temp_path = Path(f"{tempdir}/{name}")

            while not up_done and retry < max_retry:
                try:
                    urls.append(client.upload_file(token, temp_path, index=i))
                except Exception as ex:
                    logger.error(ex)
                    retry += 1
                    if retry == max_retry:
                        raise ValueError(
                            f"Failed to upload part {i} ({temp_path.stat().st_size:,}B): {ex}"
                        )
                    logger.info(f"Retrying: {retry}...")
                    time.sleep(15)
                else:
                    up_done = True

        path = write_txt(filename, urls, parts)
    return path


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description="ToDus Client for S3",
    )
    parser.add_argument(
        "-n",
        "--number",
        dest="number",
        metavar="PHONE-NUMBER",
        help="account's phone number",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--config-folder",
        dest="folder",
        type=str,
        default=".",
        help="folder where account configuration will be saved/loaded",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="show program's version number and exit.",
    )

    subparsers = parser.add_subparsers(dest="command")

    _ = subparsers.add_parser(name="login", help="authenticate in server")

    up_parser = subparsers.add_parser(name="upload", help="upload file")
    up_parser.add_argument(
        "-p",
        "--part-size",
        dest="part_size",
        type=int,
        default=0,
        help="if given, the file will be split in parts of the given size in bytes",
    )
    up_parser.add_argument("file", nargs="+", help="file to upload")

    down_parser = subparsers.add_parser(name="download", help="download file")
    down_parser.add_argument("url", nargs="+", help="url to download or txt file path")

    return parser


def register(client: ToDusClient, phone: str) -> str:
    client.request_code(phone)
    pin = input("Enter PIN:").strip()
    password = client.validate_code(phone, pin)
    logger.debug("PASSWORD: %s", password)
    return password


def read_config(phone: str, folder: str = ".") -> ConfigParser:
    config_path = Path(folder) / Path(f"{phone}.ini")
    config.read(config_path)
    return config


def save_config(phone: str, folder: str = ".") -> None:
    with open(Path(folder) / Path(f"{phone}.ini"), "w") as configfile:
        config.write(configfile)


def get_default(dtype, dkey: str, phone: str, folder: str, dvalue: str = ""):
    return dtype(
        read_config(phone, folder)["DEFAULT"].get(dkey, str(dvalue))
        if "DEFAULT" in config
        else dvalue
    )


def _upload(token: str, args: argparse.Namespace, max_retry: int):
    for path in args.file:
        filename = Path(path).name
        logger.info(f"Uploading: {filename}")
        if args.part_size:
            txt = split_upload(token, path, args.part_size, max_retry=max_retry)
            logger.info(f"TXT: {txt}")
        else:
            # TODO: Retry for single file
            filename_path = Path(path)
            file_uri = client.upload_file(token, filename_path)
            down_url = f"{file_uri}?name={quote_plus(filename)}"
            logger.info(f"URL: {down_url}")
            txt = write_txt(filename, urls=[file_uri], parts=[filename])
            logger.info(f"TXT: {txt}")


def _download(
    token: str, args: argparse.Namespace, down_timeout: float, max_retry: int
):
    urls = []

    while args.url:
        retry = 0
        down_done = False
        file_uri = args.url.pop(0)

        # Extract URLS from current TXT
        if os.path.exists(file_uri):
            with open(file_uri) as fp:
                for line in fp.readlines():
                    line = line.strip()
                    if line:
                        _url, _filename = line.split(maxsplit=1)
                        urls.append(f"{_url}?name={_filename}")

                args.url = urls + args.url
                continue

        if urls:
            count_files = len(urls)
            plural = "" if count_files <= 1 else "s"
            logger.info(f"Downloading: {count_files} file{plural}")

        logger.info(
            f"Downloading: {file_uri}",
        )
        file_uri, name = file_uri.split("?name=", maxsplit=1)
        name = unquote_plus(name)
        size = 0

        while not down_done and retry < max_retry:
            try:
                size = client.download_file(token, file_uri, name, down_timeout)
            except Exception as ex:
                logger.error(ex)

            if size:
                logger.debug(
                    f"File: {name}, Size: {size // 1024}",
                )
                down_done = True

            if not down_done or not size:
                retry += 1
                if retry == max_retry:
                    break
                logger.info(f"Retrying: {retry}...")
                time.sleep(15)

        urls = []


def main() -> None:
    global client, config, logger

    parser = get_parser()
    args = parser.parse_args()
    folder: str = args.folder
    phone: str = f"535{args.number[-7:]}"  # Country Code + phone
    password: str = get_default(str, "password", phone, folder, "")
    max_retry: int = get_default(int, "max_retry", phone, folder, str(MAX_RETRY))
    config["DEFAULT"]["max_retry"] = str(max_retry)
    down_timeout: float = get_default(
        float, "down_timeout", phone, folder, str(DOWN_TIMEOUT)
    )
    config["DEFAULT"]["down_timeout"] = str(down_timeout)
    production: bool = get_default(bool, "production", phone, folder, "True")
    config["DEFAULT"]["production"] = str(production)

    if production:
        logging.raiseExceptions = False
    else:
        logger.setLevel(logging.DEBUG)

    if not password and args.command != "login":
        print("ERROR: account not authenticated, login first.")
        return

    if args.command == "upload":
        token = client.login(phone, password)
        logger.debug(f"Token: '{token}'")
        _upload(token, args, max_retry)
    elif args.command == "download":
        token = client.login(phone, password)
        logger.debug(f"Token: '{token}'")
        _download(token, args, down_timeout, max_retry)
    elif args.command == "login":
        password = register(client, phone)
        token = client.login(phone, password)
        logger.debug(f"Token: '{token}'")

        config["DEFAULT"]["password"] = password
        config["DEFAULT"]["token"] = token
    else:
        parser.print_usage()

    save_config(phone, folder)
