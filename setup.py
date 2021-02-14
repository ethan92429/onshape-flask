"""
Onshape-Flask
------------

Adds support to authorize users with Onshape and make API requests with Flask.

"""
import os
import re
from setuptools import setup


def read(*fname):
    path = os.path.join(os.path.dirname(__file__), *fname)
    with open(path) as f:
        return f.read()


def get_version():
    for line in read('flask_onshape.py').splitlines():
        m = re.match(r"__version__\s*=\s'(.*)'", line)
        if m:
            return m.groups()[0].strip()
    raise Exception('Cannot find version')


setup(
    name='Onshape-Flask',
    version=get_version(),
    url='http://onshape.com/ethan92429/onshape-flask',
    license='MIT',
    author='Ethan Keller',
    author_email='ekeller@gmail.com',
    description='Onshape extension for Flask microframework',
    long_description=__doc__,
    py_modules=['flask_onshape'],
    test_suite='test_flask_onshape',
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'requests',
    ],
    tests_require=['mock'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
