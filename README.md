Displays the status of 8 of the tube lines, using the TFL API and the pimoroni Blinkt

[!(vine.gif)](https://vine.co/v/5q2vYDOtFiE)

## Pre-requisites

`pip install -r requirements.txt`

## Running

`python blinkt-tube-status.py`

## Notes

By default this will query the TFL API every 2 minutes

## Debian package

Included in the `Makefile` is an option to create a package so you can install/uninstall the script on your raspberry Pi. Please be aware that this has only be tested on my raspberry pi, so be careful.
