import logging

from expressvpn import wrapper


class BannedException(Exception):
    pass


def change_ip(logger):
    max_attempts = 10
    attempts = 0
    while True:
        attempts += 1
        try:
            logger.info("GETTING NEW IP")
            wrapper.random_connect()
            logger.info("SUCCESS")
            return
        except Exception as e:
            if attempts > max_attempts:
                logger.error("Max attempts reached for VPN. Check its configuration.")
                logger.error(
                    "Browse https://github.com/philipperemy/expressvpn-python."
                )
                logger.error("Program will exit.")
                exit(1)
            logger.error(e)
            logger.error("Skipping exception.")
