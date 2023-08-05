#!/usr/bin/env python

from pathlib import Path
from setuptools import setup

def find_stubs(dir: str):
    return [str(p.relative_to(dir)) for p in Path(dir).rglob('*.pyi')]

setup(
    name='cryptography-347-stubs',
    description='Stubs for cryptography v3.4.7',
    url='https://github.com/benesch/cryptography-347-stubs.git',
    version='1.0.0',
    author='Nikhil Benesch',
    author_email='nikhil.benesch@gmail.com',
    packages=['cryptography-stubs'],
    package_data = {
        'cryptography-stubs': find_stubs('cryptography-stubs'),
    },
)
