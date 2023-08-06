# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    description = long_description.split('\n', 1)[0]

# This call to setup() does all the work
setup(
    name="generic-service-bus-cqrs",
    version="0.1.2",
    description="Generic Service Bus Implementing CQRS Pattern",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Manuel Rodriguez",
    author_email="rdgztorres19@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["generic_service_bus_cqrs"],
    include_package_data=True,
    install_requires=["redis"]
)