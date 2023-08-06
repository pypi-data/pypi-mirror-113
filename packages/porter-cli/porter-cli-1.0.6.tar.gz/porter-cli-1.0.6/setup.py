from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]
setup (
 name = 'porter-cli',
 description = 'A simple command line app for managing and deploying taps projects',
 version = '1.0.6',
 packages = find_packages(), # list of all packages
 install_requires = install_requires,
 python_requires='>=3.8', # any python greater than 2.7
 entry_points='''
        [console_scripts]
        porter=cli:cli_main
    ''',
 author="Carlos Alexis Gomez Ruiz",
 keyword="portercli",
 long_description=README,
 long_description_content_type="text/x-rst",
 license='Proprietary License',
 url='https://github.com/portermetrics/porter_cli',
 download_url='https://github.com/portermetrics/porter_cli/archive/1.0.0.tar.gz',
  dependency_links=dependency_links,
  author_email='alexis@portermetrics.com',
  classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.8",
    ]
)