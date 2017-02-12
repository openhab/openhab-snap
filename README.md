# openHAB-snap

openHAB packaged as a snap for Ubuntu core. It consists of:
  - java runtime
  - openHAB run time

## How to install

This openHAB snap is available in the Ubuntu store for release series 16 (e.g. Ubuntu 16.04). Install via:

$ sudo snap install openhab

At the moment i386, arm64 architectures are using openjdk java runtime, and amd64, armhf architectures are using zulu java runtime.
https://www.azul.com/


## How to use

After install, assuming you and the device on which it was installed are on the same network, you should be able to reach the openHAB interface by visiting `<device address>`:8080 in your browser.
Port on which web interface is exposed can be configured. For more help run $ openhab.help

For more information about openHAB refer to http://www.openhab.org
