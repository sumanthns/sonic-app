#!/bin/bash

echo running flake8....
flake8 .

echo ''
echo ''

echo running tests....
export ENV=test
nosetests $1
unset ENV
