# -*- coding: utf-8 -*-

import logging
import pathlib

from mock import Mock
import pytest

from uptimerobot import UpTimeRobot
logger = logging.getLogger(__name__)

log_file_name_pytest = 'test_run_log.log'


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


def get_sample(name):
    sample_output = None
    if not name.endswith('.json'):
        name = '{}.json'.format(name)
    with (get_project_root() / 'tests' / 'samples' / name).open() as f:
        sample_output = f.read()
    return sample_output


def get_project_root():
    root_directory = pathlib.Path(__file__).parent.parent
    logger.debug('Project root directory: {}'.format(root_directory))
    return root_directory


def pytest_configure(config):
    log_names = [
        'requests',
        'tests',
    ]
    if config.getoption('debug'):
        file_path = get_project_root() / log_file_name_pytest
        handler = logging.FileHandler(file_path, mode='a')
        formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)

        for log_name in log_names:
            log = logging.getLogger(log_name)
            log.setLevel(logging.DEBUG)
            log.handlers = list()
            log.addHandler(handler)

        logger.debug('Debug messaging enabled')
    else:
        for log_name in log_names:
            log = logging.getLogger(log_name)
            log.setLevel(logging.NOTSET)
            log.handlers = [NullHandler()]


def pytest_terminal_summary(terminalreporter, exitstatus):
    file_path = get_project_root() / log_file_name_pytest
    if file_path.is_file():
        with open(file_path) as file_handle:
            output = file_handle.read()
        file_path.unlink()
        if output.strip():
            terminalreporter.write_sep('=', 'test logs')
            for line in output.splitlines():
                terminalreporter.write_line(line)


@pytest.fixture
def mock_response(monkeypatch):
    response = Mock('response')
    response.headers = {
        'content-type': 'application/json',
        'status': 200,
    }
    return response


@pytest.fixture
def http_monitor(monkeypatch, mock_response):
    mock_response.text = get_sample('http_monitor')

    def mock_response_fn(*args, **kwargs):
        return mock_response

    monkeypatch.setattr("requests.sessions.Session.get", mock_response_fn)


@pytest.fixture
def list_monitors(monkeypatch, mock_response):
    mock_response.text = get_sample('list_monitors')

    def mock_response_fn(*args, **kwargs):
        return mock_response
    monkeypatch.setattr("requests.sessions.Session.get", mock_response_fn)


@pytest.fixture
def uptimerobot():
    return UpTimeRobot(api_key='dummy_key')


# def pytest_sessionfinish(session, exitstatus):
#     update_readme_coverage()


# def update_readme_coverage():
#     coverage_percent = int(coverage.Coverage().report())
#     root_directory = pathlib.Path(__file__).parent.parent
#     readme = root_directory / 'README.md'
#     if readme.is_file():
#         new_output = list()
#         for line in readme.read_text().splitlines():
#             if line.strip().startswith('![Coverage]'):
#                 new_output.append(
#                     '![Coverage](https://img.shields.io/badge/coverage-{}-{}.svg)'.format(
#                         coverage_percent,
#                         'green',
#                     )
#                 )
#             else:
#                 new_output.append(line)
#         readme.write_text('\n'.join(new_output))
