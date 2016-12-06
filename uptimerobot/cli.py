# -*- coding: utf-8 -*-

import base64
import os
import logging

import click
import colorlog

from uptimerobot import UpTimeRobot
from .decorators import log

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_api_key():
    app = UpTimeRobot.__name__.upper()
    environment_variable = '{}_API_KEY'.format(app)
    api_key = None
    try:
        api_key = os.environ.get(environment_variable)
    except AttributeError:
        logger.debug('Username not stored in environment variable {}.'.format(
            environment_variable
        ))
    if api_key is None:
        api_key = click.prompt(
            '{} API Key'.format(app),
            type=unicode,
        )
    else:
        api_key = base64.b64decode(api_key).strip()
    return api_key

CONTEXT_SETTINGS = dict(
    help_option_names=['-h'],
    obj=UpTimeRobot(get_api_key()),
)
cli = click.Group('uptimerobot', context_settings=CONTEXT_SETTINGS, no_args_is_help=True)



@cli.command()
@click.pass_context
@log
def monitors(ctx):
    uptimerobot = ctx.obj
    for monitor in uptimerobot.monitors():
        logger.info(u'\t{}'.format(monitor.get('friendlyname')))


@cli.command()
@click.argument('monitor_names', nargs=-1)
@click.option('-o', '--output', help='File name to save graph to',
              type=click.Path(exists=True), default=None)
@click.pass_context
@log
def graph(ctx, monitor_names, output):
    uptimerobot = ctx.obj
    uptimerobot.graph(monitor_names, file_name=output)
