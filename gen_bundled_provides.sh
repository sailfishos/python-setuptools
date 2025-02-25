#!/bin/sh
pip freeze --path setuptools/setuptools/_vendor|sed 's/\(.*\)==\(.*\)/Provides: bundled(python3dist(\1)) = \2/'
