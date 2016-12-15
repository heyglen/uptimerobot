# -*- coding: utf-8 -*-

import base64
import datetime
import os
import ijson
import logging
from StringIO import StringIO

import click
import requests
import pandas as pnd
import matplotlib.pyplot as plt


plt.style.use('fivethirtyeight')


logger = logging.getLogger(__name__)


class UpTimeRobot(object):
    _url = 'https://api.uptimerobot.com'
    _methods = {
        'get': 'getMonitors',
    }
    _credentials = None

    def __init__(self, api_key=None):
        self._api_key = api_key or self._get_api_key()

    def _get_api_key(self):
        class_name = self.__class__.__name__
        environment_variable = '{}_API_KEY'.format(class_name.upper())
        api_key = None
        try:
            api_key = os.environ.get(environment_variable)
        except AttributeError:
            logger.debug('Username not stored in environment variable {}.'.format(
                environment_variable
            ))
        if api_key is None:
            api_key = click.prompt(
                '{} API Key'.format(class_name.lower()),
                type=unicode,
            )
        else:
            api_key = base64.b64decode(api_key).strip()
        return api_key

    def _clean_response_data(self, data):
        return data.replace(u'jsonUptimeRobotApi(', u'').rstrip(u')')

    def _get_params(self, monitor_id=None):
        params = {
            'apiKey': self._api_key,
            'responseTimes': 1,
            'showTimezone': 1,
            'format': 'json',
            'offset': 0,
        }
        if monitor_id:
            params['monitors'] = monitor_id
        return params

    def _get_session(self):
        if not hasattr(self, '_session'):
            self._session = requests.Session()
        return self._session

    def _get_response(self, monitor_id):
        params = self._get_params(monitor_id)
        response = self._get_session().get(
            '{}/{}'.format(self._url, self._methods.get('get')),
            params=params,
        )
        return response

    def _list_monitors(self):
        url = '{}/{}'.format(self._url, self._methods.get('get'))
        params = self._get_params()
        response = self._get_session().get(
            url,
            params=params,
        )
        data = self._clean_response_data(response.text)
        data = StringIO(data)
        for monitor in ijson.items(data, 'monitors.monitor.item'):
            yield monitor

    def _get_monitor_id(self, monitor):
        monitor_id = None
        friendly_name = None
        for monitor_object in self._list_monitors():
            if monitor_object.get('friendlyname') == monitor or monitor_object.get('id') == monitor:
                monitor_id = monitor_object.get('id')
                friendly_name = monitor_object.get('friendlyname')
                break
        return monitor_id, friendly_name

    def _get_series(self, monitor_id):
        response = self._get_response(monitor_id)
        data = self._clean_response_data(response.text)
        data = StringIO(data)

        dates = list()
        values = list()
        for measure in ijson.items(data, 'monitors.monitor.item.responsetime.item'):
            dates.append(measure.get('datetime'))
            values.append(int(measure.get('value')))

        index = pnd.to_datetime(dates, dayfirst=False)
        return pnd.Series(values, index=index)

    @classmethod
    def _save_graph(cls, figure, friendly_name):
        file_name = u'{}-{}'.format(
            friendly_name,
            unicode(datetime.datetime.now()).replace(u' ', u'-')
        )
        figure.savefig(u'{}.png'.format(file_name))
        logger.debug('Saved file to {}'.format(
            os.path.abspath(file_name)
        ))

    @classmethod
    def _display_graph(cls, figure):
        figure.show()
        plt.show()  # Wait for exit

    def graph(self, monitor, file_name=None):
        monitor_id, friendly_name = self._get_monitor_id(monitor)
        series = self._get_series(monitor_id)
        ax = series.plot()
        ax.set_title('Response Time: {}'.format(friendly_name))
        figure = ax.get_figure()
        if file_name is None:
            self._display_graph(figure)
        else:
            self._save_graph(figure, friendly_name)

    def monitors(self, name=None):
        """ List available monitors """
        identifiers = ('friendlyname', 'id', 'url')
        for monitor in self._list_monitors():
            if name is not None:
                for identifier in identifiers:
                    if monitor.get(identifier) == name:
                        yield monitor
            else:
                yield monitor
