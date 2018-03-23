#!/bin/sh

find . -type f -name "*.py" | xargs autopep8 -i
