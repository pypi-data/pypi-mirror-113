import logging


LOG_LEVEL_DEFAULT = logging.CRITICAL


def _get_logger(name="shappack", level=LOG_LEVEL_DEFAULT):
    """Gets a default shappack logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(levelname)s %(asctime)s] %(filename)s: %(message)s",
        datefmt="%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = _get_logger()
