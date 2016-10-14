# Snappy openHAB


OpenHAB server packaged as a snap. It consists of:
  - java runtime
  - openhab 2.0-beta

## How to install

This openHAB snap is available in the store for release series 16 (e.g. Ubuntu 16.04). Install via:

$ sudo snap install openhab

x86 amd64 and arm64 architectures are using openjdk java runtime, armhf architecture is using zulu java runtime
At the moment openHAB snap in Snappy store is offline version, aim is to provide online distribution version

## How to use

After install, assuming you and the device on which it was installed are on the same network, you should be able to reach the openHAB interface by visiting `<device address>`:8080 in your browser.

For more information about openHAB refer to https://github.com/openhab/openhab

## Known issues

 - $ openhab.console, openhab.stop does not work
 - some bindings are not working properly
