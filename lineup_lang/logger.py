import logging


def start_logging(log_level: str = "WARN") -> None:
    """
    Start logger for lineup_lang
    """
    logger = logging.getLogger("lineup_lang")
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
