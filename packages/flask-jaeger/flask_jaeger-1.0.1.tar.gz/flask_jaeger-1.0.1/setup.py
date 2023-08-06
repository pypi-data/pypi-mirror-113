# -*- coding: utf8 -*-

from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()


def read():
    with open("./requirements.txt", "r") as f:
        return f.readlines()


setup(
    name='flask_jaeger',
    version='1.0.1',
    packages=['flask_jaeger', ],
    url='',
    license='',
    author='yuzhang',
    author_email='geasyheart@163.com',
    description='flask jaeger',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=read()
)
