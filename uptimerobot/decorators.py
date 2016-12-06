# -*- coding: utf-8 -*-


import functools
import logging

import click
import colorlog


formatter = colorlog.ColoredFormatter(
    "%(white)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

verbose_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-2s%(reset)s %(name)-3s %(white)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)


def log(fn):
    logger = logging.getLogger(fn.__module__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    @click.option('-d', '--debug', is_flag=True, default=False)
    def logger_decorator(*args, **kwargs):
        try:
            # import ipdb; ipdb.set_trace()
            if kwargs.get('debug'):
                logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler()
                handler.setFormatter(verbose_formatter)
                logger.handlers = list()
                logger.addHandler(handler)
            kwargs.pop('debug')
            return fn(*args, **kwargs)
        except Exception as e:
            logger.error(e, exc_info=True)
    return functools.update_wrapper(logger_decorator, fn)