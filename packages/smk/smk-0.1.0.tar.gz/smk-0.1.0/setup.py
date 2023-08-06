#!/usr/bin/env python
# package: gpf-python
# package-note: This file is part of the Python General Package Format library
# package-url: github.com/ultralightweight/gpf
# licence: MIT <https://opensource.org/licenses/MIT>
# author: Daniel Kovacs <mondomhogynincsen@gmail.com>
# file: gpf-python/setup.py
# file-version: 2.3
#


# ---------------------------------------------------------------------------------------
# configuration
# ---------------------------------------------------------------------------------------

NAME = "smk"
MODULE_NAME = "smk"
VERSION = "0.1.0"
DESCRIPTION = """Software Manufacturing Kit"""
AUTHOR = "Daniel Kovacs"
AUTHOR_EMAIL = "mondomhogynincsen@gmail.com"
MAINTAINER = "Daniel Kovacs"
MAINTAINER_EMAIL = "mondomhogynincsen@gmail.com"
SCM_URL= "https://github.com/ultralightweight/smk"
KEYWORDS = []
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries",
]
LICENCE="License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"


# ---------------------------------------------------------------------------------------
# imports
# ---------------------------------------------------------------------------------------

import codecs
import os
import re

from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements, InstallRequirement
    from pip._internal.req.constructors import install_req_from_parsed_requirement
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

# ---------------------------------------------------------------------------------------
# _read()
# ---------------------------------------------------------------------------------------

def _read(*parts):
    with codecs.open(os.path.join(HOME, *parts), "rb", "utf-8") as f:
        return f.read()



# ---------------------------------------------------------------------------------------
# install_requirements
# ---------------------------------------------------------------------------------------

def install_requirements(parsed_requirement):
    if isinstance(parsed_requirement, InstallRequirement):
        return parsed_requirement
    return install_req_from_parsed_requirement(parsed_requirement)


# ---------------------------------------------------------------------------------------
# get_requirements
# ---------------------------------------------------------------------------------------

def get_requirements():
    packages, dependencies = [], []
    for ir in parse_requirements(os.path.join( HOME, 'requirements.txt' ), session=False):
        ir = install_requirements(ir)
        if ir.link:
            dependencies.append(ir.link.url)
            continue
        packages.append(str(ir.req))
    return packages, dependencies


# ---------------------------------------------------------------------------------------
# internal variables
# ---------------------------------------------------------------------------------------

HOME = os.path.abspath(os.path.dirname(__file__))
PACKAGES = find_packages(where='src')
INSTALL_REQUIRES, DEPENDENCY_LINKS = get_requirements()


# ---------------------------------------------------------------------------------------
# setup()
# ---------------------------------------------------------------------------------------

if __name__ == "__main__":
    setup(
        name=NAME,
        description=DESCRIPTION,
        license=LICENCE,
        url=SCM_URL,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        keywords=KEYWORDS,
        long_description=_read("README.md"),
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        dependency_links=DEPENDENCY_LINKS,
        setup_requires=[
        ],
        tests_require=[
            'pytest',
        ],
        entry_points = {
            'console_scripts': [
                  '{0} = {1}.cli:main'.format(NAME, MODULE_NAME)
            ],
        },
    )
