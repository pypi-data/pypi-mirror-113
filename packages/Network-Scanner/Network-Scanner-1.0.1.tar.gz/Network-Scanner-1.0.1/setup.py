import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Network-Scanner",
    version="1.0.1",
    description="Python-based tool which helps to scan the network",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/adityakesarwani/Network-Scanner",
    author="Aditya Kesarwani",
    author_email="adkesarw@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["net_scan"],
    include_package_data=True,
    install_requires=['aiodns','aioping','async-timeout','asyncio','cffi','ipaddress','mypy','mypy-extensions','pycares','pycparser','toml','typing','typing-extensions'],
    entry_points={
        "console_scripts": [
            "net_scan=net_scan.__main__:main",
        ]
    },
)