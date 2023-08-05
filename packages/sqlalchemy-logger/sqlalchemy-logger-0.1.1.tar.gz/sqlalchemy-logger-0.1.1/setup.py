from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="sqlalchemy-logger",
    version="0.1.1",
    description="Logging library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Maryia Afanasyeva",
    author_email="example@email.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["sqlalchemy_logger"],
    include_package_data=True,
    install_requires=["SQLAlchemy"]
)
