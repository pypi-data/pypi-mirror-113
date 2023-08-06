from setuptools import setup
from pathlib import Path

readme = Path("README.rst").read_text(encoding="utf-8")

setup(
    name = 'DatExtractor',
    version = '1.0',
    description = 'This package lets the users to extract date by passing the text which contains the date. This package identifies the date and extracts it.',
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Sri Phani Subramanyam",
    author_email="subbu27498@gmail.com",
    py_modules = ["date_extractor"],
    package_dir = {'':'src'},
    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ]


)