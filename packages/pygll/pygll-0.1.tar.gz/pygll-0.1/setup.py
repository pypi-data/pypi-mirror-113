#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Setup script for the LivingLogic Pygments style

import os, re

try:
	import setuptools as tools
except ImportError:
	from distutils import core as tools


DESCRIPTION = "Pygments syntax highlighting styles for dark and light backgrounds"

try:
	LONG_DESCRIPTION = open("README.rst", "r", encoding="utf-8").read().strip()
except IOError:
	LONG_DESCRIPTION = None

CLASSIFIERS = """
Development Status :: 4 - Beta
Environment :: Plugins
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Software Development :: Documentation
Topic :: Text Processing :: Filters
Topic :: Utilities
Topic :: Software Development :: Libraries :: Python Modules
"""

KEYWORDS = "syntax highlighting, pygments style"

# Get rid of text roles PyPI doesn't know about
DESCRIPTION = re.subn(":[a-z]+:`~?([-a-zA-Z0-9_./]+)`", "``\\1``", DESCRIPTION)[0]

# Expand tabs (so they won't show up as 8 spaces in the Windows installer)
DESCRIPTION = DESCRIPTION.expandtabs(2)

args = dict(
	name="pygll",
	version="0.1",
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	author="Walter Doerwald",
	author_email="walter@livinglogic.de",
	url="https://github.com/LivingLogic/LivingLogic.Python.PygLL",
	download_url="https://pypi.org/project/pygll/#files",
	license="MIT",
	classifiers=sorted({c for c in CLASSIFIERS.strip().splitlines() if c.strip() and not c.strip().startswith("#")}),
	keywords=KEYWORDS,
	py_modules=["pygll"],
	package_dir={"": "src"},
	entry_points={
		"pygments.styles": [
			"livinglogic-light = pygll:LivingLogicLightStyle",
			"livinglogic-dark  = pygll:LivingLogicDarkStyle",
		],
	},
	install_requires=[
		"pygments >= 2.0",
	],
)

if __name__ == "__main__":
	tools.setup(**args)
