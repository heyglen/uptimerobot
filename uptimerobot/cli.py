# -*- coding: utf-8 -*-

import logging

import click

from uptimerobot import UpTimeRobot

logger = logging.getLogger(__name__)


CONTEXT_SETTINGS = dict(
    help_option_names=['-h'],
    obj=UpTimeRobot(),
)
# cli = click.Group('uptimerobot', context_settings=CONTEXT_SETTINGS, no_args_is_help=True)


@click.group('uptimerobot', invoke_without_command=True)
@click.option('-d', '--debug', is_flag=True, default=False)
@click.pass_context
def monitors(ctx, debug):
    uptimerobot = ctx.obj
    for monitor in uptimerobot.monitors():
        click.echo(u'\t{}'.format(monitor.get('friendlyname')))


# @cli.command()
# @click.argument('monitor', nargs=1)
# @click.option('-o', '--output', help='File name to save graph to',
#               type=click.Path(exists=True), default=None)
# @click.option('-d', '--debug', is_flag=True, default=False)
# @click.pass_context
# def graph(ctx, monitor, output, debug):
#     uptimerobot = ctx.obj
#     uptimerobot.graph(monitor, file_name=output)

