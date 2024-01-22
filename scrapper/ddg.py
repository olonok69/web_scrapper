from duckduckgo_search import DDGS
import logging
import sys
import os
import datetime
import pandas as pd
import time
from typing_extensions import List, Dict

# install tor in linux https://itsfoss.com/install-tar-browser-linux/ or https://linuxconfig.org/install-tor-proxy-on-ubuntu-22-04-linux
# tor command line https://manpages.ubuntu.com/manpages/jammy/man1/tor.1.html
# python library https://pypi.org/project/duckduckgo-search/ # https://github.com/deedy5/duckduckgo_search
# tor password --> tor --hash-password mypassword
# request new identity tor https://stackoverflow.com/questions/31758946/request-new-tor-identity-from-windows-command-line


def star_tor(ROOT_DIR):
    command = f"{ROOT_DIR}/call_tor.sh"
    os.system(f"{command} &")
    return


def stop_tor(ROOT_DIR):
    command = f"{ROOT_DIR}/kill_tor.sh"
    os.system(f"{command} &")
    return


def get_urls(
    proxies: Dict,
    query: str,
    cat: str,
    urls: List,
    query_objects: List,
    logger: logging.getLoggerClass,
    type_file: str = "filetype:pdf",
    number_of_doc: int = 200,
    n: int = 30,
):
    with DDGS(proxies=proxies) as ddgs:
        results = [
            r for r in ddgs.text(f"{query} {type_file}", max_results=number_of_doc)
        ]

        for r in results:
            urls.append(r.get("href"))
            query_objects.append(cat)
            logger.info(r.get("href"))

    return urls, query_objects


def main(logger, ROOT_DIR):
    proxies = {"http": "socks5://localhost:9050", "https": "socks5://localhost:9050"}

    querys = pd.read_csv(
        os.path.join(ROOT_DIR, "data", "Microsoft Purview Classifiers.csv")
    )

    finish = False
    number_of_doc = 200
    while finish == False:
        # open files
        data = pd.DataFrame(data=[], columns=["query", "url"])
        filetypes = ["filetype:html", "filetype:docx", "filetype:pdf"]
        try:
            for filetype in filetypes:
                for i, row in querys.iterrows():
                    # print column
                    logger.info(f"row number {i} file type: {filetype}")
                    urls = []
                    query_objects = []
                    classe = querys.at[i, "Classifier"]
                    description = querys.at[i, "Description"]
                    file_type = querys.at[i, "File Types"]
                    cat = classe.replace(" ", "_")
                    ft = filetype.split(":")[-1]
                    if os.path.isfile(
                        os.path.join(ROOT_DIR, "output", f"{cat}_{ft}.csv")
                    ):
                        logger.warning(f"file {cat}_{ft}.csv already found")
                        continue

                    if not ("doc" in file_type):
                        logger.warning(f"class {classe} filetype not found")
                        continue
                    else:
                        logger.warning(f"working on class {classe}")
                    query = classe + " " + description.replace('"', "")

                    urls, query_objects = get_urls(
                        proxies,
                        query,
                        cat,
                        urls,
                        query_objects,
                        logger,
                        type_file=filetype,
                        number_of_doc=number_of_doc,
                        n=30,
                    )

                    data["query"] = query_objects
                    data["url"] = urls

                    cat = classe.replace(" ", "_")
                    data.to_csv(
                        os.path.join(ROOT_DIR, "output", f"{cat}_{ft}.csv"),
                        index=False,
                    )

                    logger.warning("Stopping Tor")
                    stop_tor(ROOT_DIR)
                    logger.warning("Starting Tor")
                    star_tor(ROOT_DIR)
                    time.sleep(60)
            finish = True
        except Exception as e:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            logger.error(f"Expection cath {ex_type}")
            logger.warning("Stopping Tor")
            stop_tor(ROOT_DIR)
            logger.warning("Starting Tor")
            star_tor(ROOT_DIR)
            time.sleep(60)


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    now = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    file_handler = logging.FileHandler(
        os.path.join(ROOT_DIR, "logs", f"logs_{now}.log")
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    logger.warning("Stopping Tor")
    stop_tor(ROOT_DIR)
    logger.warning("Starting Tor")
    star_tor(ROOT_DIR)
    time.sleep(30)
    logger.info("sleeping 30 seconds")

    main(logger, ROOT_DIR)
