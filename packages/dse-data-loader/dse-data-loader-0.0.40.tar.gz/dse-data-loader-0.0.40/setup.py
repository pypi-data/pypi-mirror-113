from setuptools import setup
import os

VERSION = "0.0.40"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="dse-data-loader",
    description="dse-data-loader is now stocksurferbd",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["stocksurferbd"],
    classifiers=["Development Status :: 7 - Inactive"],
)
