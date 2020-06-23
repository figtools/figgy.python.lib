import re
from setuptools import setup, find_packages

FIGGY_WEBSITE = "https://www.figgy.dev"
VERSION = '0.0.4'
SHORT_DESCRIPTION = "Python library that supports Python development while using the Figgy config management " \
                    f"framework: {FIGGY_WEBSITE}"

LONG_DESCRIPTION = """
# figgy
Cloud native config management.

For details on Figgy check out the [Figgy Blog](https://www.figgy.devl) or [Figgy Docs](https:/www.figgy.dev/docs/)

To see a live example of how you can use this library, check the reference github repo: https://github.com/mancej/figgy.python-reference

"""

setup(
    name="figgy-lib",
    packages=find_packages("."),
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Jordan Mance",
    author_email="jordan@figgy.dev",
    url=FIGGY_WEBSITE,
    python_requires='>=3.6',
    install_requires=[
        "boto3>=1.13.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation",
    ]
)
