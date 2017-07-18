from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flask-request-args-parser',
    version='1.1.0',
    description='flask.request\'s args parser',
    long_description=long_description,
    url='https://github.com/mitinarseny/flask-request-args-parser',
    author='Arseny Mitin',
    author_email='mitinarseny@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='flask request args flask-restful parse reqparse requestparser',
    packages=find_packages(exclude=['flask', 'werkzeug']),
    install_requires=['flask', 'werkzeug'],
)
