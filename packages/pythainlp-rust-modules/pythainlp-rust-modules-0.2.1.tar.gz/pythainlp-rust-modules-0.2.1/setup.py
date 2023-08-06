from setuptools import setup
import os

VERSION = "0.2.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()

setup(
    name="pythainlp-rust-modules",
    description="pythainlp-rust-modules is now nlpo3",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["nlpo3"],  # new package name
    python_requires=">=3.6",
    license="Apache-2.0",
    url="https://github.com/PyThaiNLP/nlpo3/",
    classifiers=["Development Status :: 7 - Inactive"],
)
