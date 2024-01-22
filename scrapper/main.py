from src.connect_vpn import change_ip, BannedException
from expressvpn import wrapper
import logging
import sys
import os
import datetime
import pandas as pd
from googlesearch import search

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

now = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
file_handler = logging.FileHandler(os.path.join(ROOT_DIR, "logs", f"logs_{now}.log"))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
from googlesearch import search

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def main():
    query = "agreement"

    data = pd.DataFrame(data=[], columns=["query", "url"])
    while True:
        try:
            logger.info("GETTING NEW IP")
            wrapper.random_connect()
            logger.info("SUCCESS")

            results = search(
                query,
                lang="en",
                num_results=100,
                advanced=True,
            )
            url_objects = []
            query_objects = []
            print("here")
            for r in results:
                url_objects.append(r.url)
                query_objects.append[query]
                print(r.url)
            data["query"] = query_objects
            data["url"] = url_objects
            cat = query.replace(" ", "_")
            data.to_csv(os.path.join(ROOT_DIR, "output", f"{cat}.csv"), index=False)
            exit(0)
        except BannedException as be:
            logger.info("BANNED EXCEPTION in __MAIN__")
            logger.info(be)
            logger.info("Lets change our PUBLIC IP GUYS!")
            change_ip(logger)
        except Exception as e:
            logger.error("Exception raised.")
            logger.error(e)


if __name__ == "__main__":
    main()
