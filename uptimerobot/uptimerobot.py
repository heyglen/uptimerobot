# -*- coding: utf-8 -*-

import datetime
import os
import ijson
import logging
from collections import namedtuple
from StringIO import StringIO

import requests
import pandas as pnd
import matplotlib.pyplot as plt


plt.style.use('fivethirtyeight')


logger = logging.getLogger(__name__)

ApiMethod = namedtuple('ApiMethod', ['get'])
api_method = ApiMethod(get='getMonitors')


class UpTimeRobot(object):
    _url = 'https://api.uptimerobot.com'
    _methods = api_method

    def __init__(self, api_key=None):
        self._api_key = api_key or self._get_api_key()

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

    def _list_monitors(self):
        url = '{}/{}'.format(self._url, self._methods.get)
        params = self._get_params()
        response = requests.get(
            url,
            params=params,
        )
        data = self._clean_response_data(response.text)
        data = StringIO(data)
        monitors = list()
        for monitor in ijson.items(data, 'monitors.monitor.item'):
            monitors.append(monitor)
        return monitors

    def _get_monitor_id(self, monitor):
        monitor_id = None
        friendly_name = None
        for monitor_object in self._list_monitors():
            if monitor_object.get('friendlyname') == monitor or monitor_object.get('id') == monitor:
                monitor_id = monitor_object.get('id')
                friendly_name = monitor_object.get('friendlyname')
                return monitor_id, friendly_name
        raise ValueError('Unknown monitor "{}"'.format(monitor))

    def _get_series(self, monitor_ids):
        if not isinstance(monitor_ids, list):
            monitor_ids = [monitor_ids]
        
        monitor_ids = u'-'.join(monitor_ids)
        response = requests.get(
            '{}/{}'.format(self._url, self._methods.get),
            params=self._get_params(monitor_ids),
        )
        data = self._clean_response_data(response.text)

        df = pnd.read_json(data, typ='series', orient='columns')

        all_series = list()        
        for monitor in df['monitors']['monitor']:
            index = pnd.to_datetime(
                [e['datetime'] for e in monitor['responsetime']],
                dayfirst=False,
            )
            series = pnd.Series(
                name=monitor['friendlyname'],
                data=[int(e['value']) for e in monitor['responsetime']],
                index=index
            )
            yield series

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

    def graph(self, monitors, file_name=None):
        if not isinstance(monitors, tuple):
            monitors = (monitors, )
        monitors = [self._get_monitor_id(m)[0] for m in monitors]

        for series in self._get_series(monitors):
            ax = series.plot()
            ax.set_title('Response Time: {}'.format(series.name))
            figure = ax.get_figure()
            if file_name is None:
                self._display_graph(figure)
            else:
                self._save_graph(figure, series.name)

    def monitors(self):
        """ List available monitors """
        for monitor in self._list_monitors():
            yield monitor
