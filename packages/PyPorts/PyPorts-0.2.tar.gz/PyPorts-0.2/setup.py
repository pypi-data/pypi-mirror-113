from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.2'
DESCRIPTION = 'quick way to integrate a port scanner'
LONG_DESCRIPTION = 'quick and easy way integrate a basic port scanner in one line of code'
project_urls = {
  'Github': 'https://github.com/Basic-SkriptKiddie/PyPorts',
}
# Setting up
setup(
    name="PyPorts",
    version=VERSION,
    author="Basic-ScriptKiddie",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'port', 'scanner', 'port scaner', 'ip', 'sockets'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)