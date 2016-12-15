# -*- coding: utf-8 -*-

import pytest


@pytest.mark.usefixtures('list_monitors')
def test_monitors(uptimerobot):
    monitors = [m.get('friendlyname') for m in uptimerobot.monitors()]
    for index in range(len(monitors)):
        assert 'www.example{}.com'.format(index) in monitors


@pytest.mark.usefixtures('list_monitors')
@pytest.mark.parametrize('key,value', [
    ('friendlyname', 'www.example2.com'),
    ('id', '59411727'),
    ('url', 'http://www.example2.com'),
])
def test_monitor(uptimerobot, key, value):
    for monitor in uptimerobot.monitors(name=key):
        assert value == monitor.get(key)


