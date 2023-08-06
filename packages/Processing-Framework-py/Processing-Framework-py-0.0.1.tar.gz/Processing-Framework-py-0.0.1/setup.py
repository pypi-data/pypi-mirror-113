from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Makes it easier to use the processing-py module derived from processing.org.'
LONG_DESCRIPTION = 'A framework for the processing-py module that makes it easier to use and create processing.org projects. Similar to the processing.org application and the p5.js system.'

# Setting up
setup(
    name="Processing-Framework-py",
    version=VERSION,
    author="clutchkuda (Cameron Airlie)",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['processing-py', 'pynput'],
    keywords=['python', 'processing', 'p5', 'graphics', 'display'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)