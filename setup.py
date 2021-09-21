import setuptools


NAME = "eat"
DESCRIPTION = "Edge Api Tool"
URL = "https://github.com/tmanfree/EAT"
EMAIL = "tmanfree@hotmail.com"
AUTHOR = "Thomas Mandzie"
VERSION = "0.0.1"


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.24.0'
            ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
        'eat = EAT.eat:eat',
        ],
    }
)