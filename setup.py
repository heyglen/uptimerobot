# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'pandas',
    'ijson',
    'requests',
    'matplotlib',
    'colorlog',
    # TODO: put package requirements here
]

test_requirements = [
    'bumpversion',
    # TODO: put package test requirements here
]

setup(
    name='uptimerobot',
    version='0.1.0',
    description="uptimerobot python api",
    long_description=readme + '\n\n' + history,
    author="Glen Harmon",
    author_email='glencharmon@gmail.com',
    packages=find_packages(exclude=['contrib', u'docs', u'tests']),
    package_dir={'uptimerobot':
                 'uptimerobot'},
    entry_points={
        'console_scripts': [
            'uptimerobot=uptimerobot.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='uptimerobot',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
